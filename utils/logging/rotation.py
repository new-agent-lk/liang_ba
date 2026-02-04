"""
Log Rotation Manager

Handles log file rotation with configurable policies.
"""
import os
import glob
import shutil
import gzip
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import logging


class RotationStrategy(Enum):
    SIZE = 'size'
    TIME = 'time'
    COUNT = 'count'


@dataclass
class RotationPolicy:
    """Configuration for log rotation"""
    max_size_mb: int = 10
    max_files: int = 10
    max_age_days: int = 30
    compress_old: bool = True
    strategy: RotationStrategy = RotationStrategy.SIZE


@dataclass
class LogFileInfo:
    """Information about a log file"""
    path: Path
    size_bytes: int
    modified: datetime
    is_compressed: bool = False
    rotation_count: int = 0


class LogRotationManager:
    """
    Manages log file rotation with multiple strategies

    Features:
    - Size-based rotation
    - Time-based rotation
    - Count-based cleanup
    - Automatic compression of old logs
    """

    def __init__(self, logs_dir: Path = None):
        self.logs_dir = logs_dir or Path('/home/ubuntu/liang_ba/logs')
        self.logger = logging.getLogger('app.admin.logs.rotation')
        self.policies: Dict[str, RotationPolicy] = {
            'app': RotationPolicy(max_size_mb=10, max_files=10, max_age_days=30),
            'error': RotationPolicy(max_size_mb=10, max_files=20, max_age_days=60),
            'security': RotationPolicy(max_size_mb=10, max_files=30, max_age_days=90),
            'performance': RotationPolicy(max_size_mb=10, max_files=10, max_age_days=30),
            'django': RotationPolicy(max_size_mb=10, max_files=5, max_age_days=14),
        }

    def check_and_rotate(self, log_type: str) -> Dict[str, Any]:
        """
        Check if rotation needed and perform rotation

        Returns:
            Dictionary with rotation results
        """
        policy = self.policies.get(log_type)
        log_file = self.logs_dir / f"{log_type}.log"

        if not log_file.exists():
            return {'rotated': False, 'reason': 'file_not_found'}

        file_size_mb = log_file.stat().st_size / (1024 * 1024)

        if file_size_mb < policy.max_size_mb:
            return {'rotated': False, 'reason': 'size_below_threshold', 'current_mb': file_size_mb}

        # Perform rotation
        result = self._rotate_by_size(log_file, policy)

        # Cleanup old files
        cleanup_result = self._cleanup_old_files(log_type, policy)
        result['cleanup'] = cleanup_result

        return result

    def _rotate_by_size(self, log_file: Path, policy: RotationPolicy) -> Dict[str, Any]:
        """Rotate log file by size"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rotated_name = f"{log_file.stem}_{timestamp}.log"
        rotated_path = self.logs_dir / rotated_name

        # Rename current log file
        try:
            log_file.rename(rotated_path)
            self.logger.info(f"Rotated {log_file} to {rotated_path}")
        except OSError as e:
            self.logger.error(f"Failed to rotate {log_file}: {e}")
            return {'rotated': False, 'error': str(e)}

        # Create new empty log file
        log_file.touch()

        result = {
            'rotated': True,
            'old_file': str(rotated_path),
            'new_file': str(log_file),
        }

        # Compress if configured
        if policy.compress_old:
            compressed = self._compress_file(rotated_path)
            result['compressed'] = compressed

        return result

    def _compress_file(self, file_path: Path) -> bool:
        """Gzip compress a file"""
        compressed_path = Path(str(file_path) + '.gz')
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            file_path.unlink()  # Remove original
            return True
        except Exception as e:
            self.logger.error(f"Failed to compress {file_path}: {e}")
            return False

    def _cleanup_old_files(self, log_type: str, policy: RotationPolicy) -> Dict[str, Any]:
        """Remove old log files based on policy"""
        # Match both patterns:
        # 1. django.log.1, django.log.2 (Python logging style)
        # 2. django_YYYYMMDD_HHMMSS.log (our rotation style)
        patterns = [
            self.logs_dir / f"{log_type}.log.*",      # django.log.1, django.log.2, etc.
            self.logs_dir / f"{log_type}_*.log*",      # django_20260204.log, django_20260204.log.gz
        ]
        files = []
        for pattern in patterns:
            for f in glob.glob(str(pattern)):
                path = Path(f)
                # Exclude current log file
                if path.name == f"{log_type}.log":
                    continue
                files.append(LogFileInfo(
                    path,
                    path.stat().st_size,
                    datetime.fromtimestamp(path.stat().st_mtime)
                ))

        # Sort by modification time (newest first)
        files = sorted(files, key=lambda x: x.modified, reverse=True)

        deleted = []
        kept = []

        now = datetime.now()

        for f in files:
            # Check age
            age_days = (now - f.modified).days
            should_delete = False
            reason = ''

            if age_days > policy.max_age_days:
                should_delete = True
                reason = f'age_{age_days}_days'
            elif len([x for x in kept if not x.is_compressed]) > policy.max_files:
                should_delete = True
                reason = 'count_exceeded'

            if should_delete:
                try:
                    f.path.unlink()
                    deleted.append({'path': str(f.path), 'reason': reason})
                except Exception as e:
                    self.logger.error(f"Failed to delete {f.path}: {e}")
            else:
                kept.append(f)

        return {
            'deleted_count': len(deleted),
            'deleted_files': deleted,
            'remaining_count': len(kept),
        }

    def get_rotation_status(self, log_type: str) -> Dict[str, Any]:
        """Get current rotation status for a log type"""
        policy = self.policies.get(log_type)
        log_file = self.logs_dir / f"{log_type}.log"

        status = {
            'log_type': log_type,
            'policy': {
                'max_size_mb': policy.max_size_mb,
                'max_files': policy.max_files,
                'max_age_days': policy.max_age_days,
                'compress_old': policy.compress_old,
            },
        }

        if not log_file.exists():
            status['current_size_mb'] = 0
            status['exists'] = False
            return status

        status['exists'] = True
        status['current_size_mb'] = round(log_file.stat().st_size / (1024 * 1024), 2)
        status['last_modified'] = datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()

        # Get archived files - match both patterns:
        # 1. django.log.1, django.log.2 (Python logging style)
        # 2. django_YYYYMMDD_HHMMSS.log (our rotation style)
        patterns = [
            self.logs_dir / f"{log_type}.log.*",      # django.log.1, django.log.2, etc.
            self.logs_dir / f"{log_type}_*.log*",      # django_20260204.log, django_20260204.log.gz
        ]
        archived = []
        for pattern in patterns:
            for f in glob.glob(str(pattern)):
                path = Path(f)
                # Exclude current log file
                if path.name == f"{log_type}.log":
                    continue
                archived.append(LogFileInfo(
                    path,
                    path.stat().st_size,
                    datetime.fromtimestamp(path.stat().st_mtime)
                ))

        status['archived_files_count'] = len(archived)
        status['archived_files'] = [
            {
                'name': f.path.name,
                'size_mb': round(f.size_bytes / (1024 * 1024), 2),
                'modified': f.modified.isoformat(),
                'is_compressed': f.is_compressed,
            }
            for f in archived[:10]  # Last 10
        ]

        return status

    def update_policy(self, log_type: str, policy: RotationPolicy) -> None:
        """Update rotation policy for a log type"""
        self.policies[log_type] = policy
        self.logger.info(f"Updated rotation policy for {log_type}: {policy}")

    def manual_rotate(self, log_type: str) -> Dict[str, Any]:
        """Force manual rotation of a log file"""
        return self.check_and_rotate(log_type)


# Singleton
_rotation_manager: Optional[LogRotationManager] = None


def get_rotation_manager() -> LogRotationManager:
    """Get singleton rotation manager instance"""
    global _rotation_manager
    if _rotation_manager is None:
        _rotation_manager = LogRotationManager()
    return _rotation_manager
