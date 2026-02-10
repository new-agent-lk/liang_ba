"""
Log Reader with Caching and Indexing

Provides cached, indexed log reading for high-performance admin viewing.
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .parser import LogParser, ParsedLogEntry


class CachedLogReader:
    """
    High-performance log reader with Redis caching and line indexing

    Features:
    - Redis cache for parsed entries
    - Line number indexing for fast seeking
    - Memory-mapped style access patterns
    """

    CACHE_PREFIX = "log_cache:"
    INDEX_PREFIX = "log_index:"

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._indexes: Dict[Path, Any] = {}
        self.logger = logging.getLogger("app.admin.logs.reader")

    def _get_cache_key(self, file_path: str, offset: int, limit: int) -> str:
        """Generate cache key"""
        return f"{self.CACHE_PREFIX}{hashlib.md5(file_path.encode()).hexdigest()}:{offset}:{limit}"

    def _get_index_key(self, file_path: str) -> str:
        """Generate index key"""
        return f"{self.INDEX_PREFIX}{hashlib.md5(file_path.encode()).hexdigest()}"

    def read_logs(
        self,
        log_type: str,
        offset: int = 0,
        limit: int = 100,
        level: Optional[str] = None,
        trace_id: Optional[str] = None,
        search: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Read and filter logs with pagination

        Args:
            log_type: Type of log (app, error, security, performance)
            offset: Line offset from end (for reverse reading)
            limit: Maximum entries to return
            level: Filter by log level
            trace_id: Filter by trace_id
            search: Full-text search in message
            start_time: Filter by start time
            end_time: Filter by end time

        Returns:
            Dictionary with entries, total count, and pagination info
        """
        file_path = LogParser.get_log_file(log_type)

        if not file_path.exists():
            return {
                "entries": [],
                "total": 0,
                "offset": offset,
                "limit": limit,
                "has_more": False,
            }

        # Try cache first
        cache_key = self._get_cache_key(str(file_path), offset, limit)
        if self.redis:
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    self.logger.debug(f"Cache hit for {cache_key}")
                    return json.loads(cached)
            except Exception as e:
                self.logger.warning(f"Redis cache read failed: {e}")

        # Parse logs
        parser = LogParser(file_path, reverse=True)
        entries = []
        skipped = 0

        for entry in parser.parse(offset=offset, limit=offset + limit):
            # Apply filters
            if level and entry.level.value != level.upper():
                continue

            if trace_id and entry.trace_id != trace_id:
                continue

            if search and search.lower() not in entry.message.lower():
                continue

            if start_time and entry.timestamp < start_time:
                continue

            if end_time and entry.timestamp > end_time:
                continue

            # Apply offset
            if skipped < offset:
                skipped += 1
                continue

            # Add to results
            entries.append(self._serialize_entry(entry))

            if len(entries) >= limit:
                break

        # Calculate total (approximation for performance)
        total = offset + skipped + len(entries)

        result = {
            "entries": entries,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": len(entries) == limit,
        }

        # Cache result
        if self.redis:
            try:
                self.redis.setex(cache_key, 300, json.dumps(result, default=str))  # 5 min cache
                self.logger.debug(f"Cached result for {cache_key}")
            except Exception as e:
                self.logger.warning(f"Redis cache write failed: {e}")

        return result

    def _serialize_entry(self, entry: ParsedLogEntry) -> Dict[str, Any]:
        """Serialize entry for JSON response"""
        return {
            "timestamp": entry.timestamp.isoformat(),
            "level": entry.level.value,
            "logger": entry.logger,
            "message": entry.message,
            "module": entry.module,
            "function": entry.function,
            "line": entry.line,
            "process_id": entry.process_id,
            "thread_id": entry.thread_id,
            "trace_id": entry.trace_id,
            "request_id": entry.request_id,
            "user_id": entry.user_id,
            "extra": entry.extra,
        }

    def get_log_stats(self, log_type: str) -> Dict[str, Any]:
        """Get statistics for a log file"""
        file_path = LogParser.get_log_file(log_type)

        if not file_path.exists():
            return {"error": "Log file not found"}

        stats = {
            "file_path": str(file_path),
            "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        }

        # Count entries by level
        level_counts = {}
        for entry in LogParser(file_path).parse_all():
            level = entry.level.value
            level_counts[level] = level_counts.get(level, 0) + 1

        stats["level_counts"] = level_counts
        stats["total_entries"] = sum(level_counts.values())

        return stats


# Singleton instance
_log_reader: Optional[CachedLogReader] = None


def get_log_reader() -> CachedLogReader:
    """Get singleton log reader instance"""
    global _log_reader
    if _log_reader is None:
        _log_reader = CachedLogReader()
    return _log_reader
