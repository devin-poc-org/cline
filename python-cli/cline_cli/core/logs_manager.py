"""Log management functionality."""

import os
import glob
from datetime import datetime, timedelta
from typing import List, Tuple
from cline_cli.utils.display import Display


class LogsManager:
    """Manages Cline log files."""
    
    def __init__(self):
        """Initialize logs manager."""
        self.config_path = os.path.expanduser('~/.cline')
        self.logs_dir = os.path.join(self.config_path, 'logs')
    
    def get_logs_path(self) -> str:
        """Get the logs directory path."""
        return self.logs_dir
    
    def list_logs(self):
        """List all log files."""
        if not os.path.exists(self.logs_dir):
            print("No log files found.")
            print(f"Log files will be created in: {self.logs_dir}")
            return
        
        log_files = self._get_log_files()
        
        if not log_files:
            print("No log files found.")
            print(f"Log files will be created in: {self.logs_dir}")
            return
        
        display = Display()
        display.show_log_files(log_files)
    
    def clean_logs(self, older_than: int, delete_all: bool, dry_run: bool):
        """Clean old log files.
        
        Args:
            older_than: Delete logs older than N days
            delete_all: Delete all log files
            dry_run: Show what would be deleted without deleting
        """
        if not os.path.exists(self.logs_dir):
            print("No log files to delete.")
            return
        
        log_files = self._get_log_files()
        
        if not log_files:
            print("No log files to delete.")
            return
        
        if delete_all:
            to_delete = log_files
        else:
            cutoff = datetime.now() - timedelta(days=older_than)
            to_delete = [f for f in log_files if f['created'] < cutoff]
        
        if not to_delete:
            if delete_all:
                print("No log files to delete.")
            else:
                print(f"No log files older than {older_than} days found.")
            return
        
        total_size = sum(f['size'] for f in to_delete)
        
        if dry_run:
            print("The following log files will be deleted:\n")
            display = Display()
            display.show_log_files(to_delete, mark_for_deletion=True)
            
            file_word = "files" if len(to_delete) != 1 else "file"
            print(f"\nSummary: {len(to_delete)} {file_word} will be deleted ({self._format_size(total_size)} freed)")
            print("\nRun without --dry-run to actually delete these files.")
            return
        
        count = 0
        bytes_freed = 0
        
        for log_file in to_delete:
            try:
                os.remove(log_file['path'])
                count += 1
                bytes_freed += log_file['size']
            except Exception as e:
                print(f"Failed to delete {log_file['name']}: {e}")
        
        file_word = "files" if count != 1 else "file"
        print(f"Deleted {count} log {file_word} ({self._format_size(bytes_freed)} freed)")
    
    def _get_log_files(self) -> List[dict]:
        """Get list of log files with metadata."""
        log_files = []
        
        pattern = os.path.join(self.logs_dir, '*.log')
        for filepath in glob.glob(pattern):
            try:
                stat = os.stat(filepath)
                created = datetime.fromtimestamp(stat.st_mtime)
                
                log_files.append({
                    'name': os.path.basename(filepath),
                    'path': filepath,
                    'size': stat.st_size,
                    'created': created
                })
            except Exception:
                continue
        
        log_files.sort(key=lambda x: x['created'], reverse=True)
        
        return log_files
    
    def _format_size(self, bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"
