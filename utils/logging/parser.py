"""
JSON Log Parser

Provides efficient parsing of JSON log files with streaming capability.
Supports both JSON format and Django's text format.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generator, Iterator, Optional, Union


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Django text log format: [LEVEL][YYYY-MM-DD HH:MM:SS,mmm][module.py:line] message
DJANGO_LOG_PATTERN = re.compile(
    r"\[(?P<level>[A-Z]+)\]\[(?P<timestamp>\d{4}-\d{2}-\d{2}[ ,]\d{2}:\d{2}:\d{2}[,.]\d{3})\]\[(?P<location>[^\]]+)\](?P<message>.*)"
)


@dataclass
class ParsedLogEntry:
    """Parsed log entry dataclass"""

    timestamp: datetime
    level: LogLevel
    logger: str
    message: str
    module: str
    function: str
    line: int
    process_id: int
    thread_id: int
    trace_id: str
    request_id: str
    user_id: Optional[int]
    extra: Dict[str, Any] = field(default_factory=dict)
    raw_line: str = ""
    file_path: Path = None

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], raw_line: str = "", file_path: Path = None
    ) -> "ParsedLogEntry":
        """Create ParsedLogEntry from dictionary"""
        return cls(
            timestamp=cls._parse_timestamp(data.get("timestamp")),
            level=LogLevel(data.get("level", "INFO").upper()),
            logger=data.get("logger", ""),
            message=data.get("message", ""),
            module=data.get("module", ""),
            function=data.get("function", ""),
            line=data.get("line", 0),
            process_id=data.get("process_id", 0),
            thread_id=data.get("thread_id", 0),
            trace_id=data.get("trace_id", "-"),
            request_id=data.get("request_id", "-"),
            user_id=data.get("user_id"),
            extra=data.get("extra", {}),
            raw_line=raw_line,
            file_path=file_path,
        )

    @staticmethod
    def _parse_timestamp(ts: str) -> datetime:
        """Parse ISO timestamp"""
        if not ts:
            return datetime.now()
        try:
            # Handle format: 2026-02-04T03:19:04.563Z
            if ts.endswith("Z"):
                ts = ts[:-1] + "+00:00"
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.now()


class LogParser:
    """Efficient JSON log file parser"""

    LOG_FILES = {
        "app": Path("/home/ubuntu/liang_ba/logs/app.log"),
        "error": Path("/home/ubuntu/liang_ba/logs/error.log"),
        "security": Path("/home/ubuntu/liang_ba/logs/security.log"),
        "performance": Path("/home/ubuntu/liang_ba/logs/performance.log"),
        "django": Path("/home/ubuntu/liang_ba/logs/django.log"),
    }

    def __init__(self, file_path: Union[Path, str], reverse: bool = True):
        self.file_path = Path(file_path) if isinstance(file_path, str) else file_path
        self.reverse = reverse

    def parse(self, offset: int = 0, limit: int = 1000) -> Iterator[ParsedLogEntry]:
        """
        Parse log file with offset and limit

        Supports both:
        - JSON format: {"timestamp": "...", "level": "INFO", ...}
        - Django text format: [LEVEL][YYYY-MM-DD HH:MM:SS,mmm][module.py:line] message

        Args:
            offset: Number of lines to skip from end (for reverse reading)
            limit: Maximum number of entries to return
        """
        # Ensure offset and limit are integers
        offset = int(offset)
        limit = int(limit)

        if not self.file_path.exists():
            return

        lines = self._read_lines(offset, limit)

        for line in lines:
            if not line.strip():
                continue

            # Try JSON format first
            try:
                data = json.loads(line)
                yield ParsedLogEntry.from_dict(data, line, self.file_path)
                continue
            except json.JSONDecodeError:
                pass

            # Try Django text format
            parsed = self._parse_django_text_format(line)
            if parsed:
                yield parsed

    def _parse_django_text_format(self, line: str) -> Optional[ParsedLogEntry]:
        """
        Parse Django's text log format: [LEVEL][YYYY-MM-DD HH:MM:SS,mmm][module.py:line] message

        Returns ParsedLogEntry or None if parsing fails.
        """
        match = DJANGO_LOG_PATTERN.match(line)
        if not match:
            return None

        groups = match.groupdict()

        # Parse timestamp (handle both comma and dot separators)
        timestamp_str = groups.get("timestamp", "").replace(",", ".")
        timestamp = self._parse_django_timestamp(timestamp_str)

        # Parse level
        level_str = groups.get("level", "INFO").upper()
        try:
            level = LogLevel(level_str)
        except ValueError:
            level = LogLevel.INFO

        # Parse location [module.py:line]
        location = groups.get("location", "")
        module = ""
        function = ""
        line_num = 0
        if ":" in location:
            parts = location.rsplit(":", 1)
            module = parts[0]
            try:
                line_num = int(parts[1])
            except ValueError:
                pass
            if "." in module:
                module = module.rsplit(".", 1)[-1]

        message = groups.get("message", "").strip()

        return ParsedLogEntry(
            timestamp=timestamp,
            level=level,
            logger="django",
            message=message,
            module=module,
            function=function,
            line=line_num,
            process_id=0,
            thread_id=0,
            trace_id="-",
            request_id="-",
            user_id=None,
            extra={},
            raw_line=line,
            file_path=self.file_path,
        )

    def _parse_django_timestamp(self, ts: str) -> datetime:
        """Parse Django timestamp format: YYYY-MM-DD HH:MM:SS.mmm"""
        if not ts:
            return datetime.now()
        try:
            # Format: 2026-02-04 15:30:57.817
            dt = datetime.strptime(ts[:23], "%Y-%m-%d %H:%M:%S.%f")
            return dt
        except ValueError:
            return datetime.now()

    def _read_lines(self, offset: int, limit: int) -> Generator[str, None, None]:
        """Read lines efficiently from end of file"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            f.seek(0, 2)
            file_size = f.tell()

            if file_size == 0:
                return

            position = file_size
            lines_read = 0
            lines_buffer = []

            while position > 0 and lines_read < offset + limit:
                chunk_size = min(8192, position)
                position -= chunk_size
                f.seek(position)
                chunk = f.read(chunk_size)

                chunk_lines = chunk.split("\n")

                if lines_buffer:
                    lines_buffer[0] = chunk_lines[-1] + lines_buffer[0]
                else:
                    if chunk_lines[-1]:
                        lines_buffer.append(chunk_lines[-1])

                for i in range(len(chunk_lines) - 2, -1, -1):
                    lines_buffer.append(chunk_lines[i])

                lines_read += len(chunk_lines)

            if lines_buffer and not lines_buffer[-1].strip():
                lines_buffer.pop()

            result = lines_buffer[-limit:] if self.reverse else lines_buffer[:limit]

            if self.reverse:
                result = list(reversed(result))

            for line in result:
                yield line

    def parse_all(self) -> Generator[ParsedLogEntry, None, None]:
        """Parse entire log file"""
        return self.parse(offset=0, limit=float("inf"))

    @classmethod
    def get_log_file(cls, log_type: str) -> Path:
        """Get path to log file by type"""
        return cls.LOG_FILES.get(log_type, cls.LOG_FILES["app"])

    @classmethod
    def list_available_logs(cls) -> Dict[str, Path]:
        """List all available log files"""
        return {name: path for name, path in cls.LOG_FILES.items() if path.exists()}
