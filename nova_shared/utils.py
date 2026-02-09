"""Shared utility functions for file operations and path handling."""
import os
from pathlib import Path
from typing import List, Optional

def get_project_files(root_path: str, extensions: List[str]) -> List[Path]:
    """
    Recursively get all files with specified extensions.
    
    Args:
        root_path: Root directory to scan
        extensions: List of file extensions to include (e.g., ['.py', '.js'])
    
    Returns:
        List of Path objects for matching files
    """
    root = Path(root_path)
    files = []
    
    for item in root.rglob('*'):
        if item.is_file() and item.suffix in extensions:
            # Check if any parent directory should be ignored
            if not any(is_ignored_directory(parent.name) for parent in item.parents):
                files.append(item)
    
    return files


def read_file_safe(file_path: Path) -> Optional[str]:
    """
    Safely read file contents with encoding fallback.
    
    Args:
        file_path: Path to file
    
    Returns:
        File contents as string, or None if read fails
    """
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            # File might be binary or inaccessible
            return None
    
    return None


def is_ignored_directory(dir_name: str) -> bool:
    """
    Check if directory should be ignored (node_modules, .git, etc.).
    
    Args:
        dir_name: Directory name
    
    Returns:
        True if directory should be ignored
    """
    ignored = {
        'node_modules', '.git', '__pycache__', '.venv', 'venv',
        'dist', 'build', '.next', '.cache', 'coverage', '.pytest_cache',
        'htmlcov', '.tox', '.eggs', '*.egg-info', '.mypy_cache',
        '.idea', '.vscode', '__pypackages__', 'env', 'ENV'
    }
    return dir_name in ignored or dir_name.startswith('.')


def get_file_stats(file_path: Path) -> dict:
    """
    Get basic statistics about a file.
    
    Args:
        file_path: Path to file
    
    Returns:
        Dict with file statistics
    """
    try:
        stat = file_path.stat()
        content = read_file_safe(file_path)
        
        return {
            'size_bytes': stat.st_size,
            'line_count': content.count('\n') if content else 0,
            'modified_time': stat.st_mtime
        }
    except Exception:
        return {
            'size_bytes': 0,
            'line_count': 0,
            'modified_time': 0
        }
