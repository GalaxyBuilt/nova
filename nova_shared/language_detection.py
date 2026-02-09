"""Language and framework detection utilities."""
from pathlib import Path
from typing import Dict, Optional
import json


class LanguageDetector:
    """Detect programming language and framework from file extensions."""
    
    EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'react',
        '.ts': 'typescript',
        '.tsx': 'react-typescript',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.json': 'json',
        '.xml': 'xml',
        '.md': 'markdown',
        '.vue': 'vue',
        '.svelte': 'svelte'
    }
    
    FRAMEWORK_MARKERS = {
        'next.js': ['next.config.js', 'next.config.ts', 'next.config.mjs'],
        'react': ['package.json'],  # Check for react in dependencies
        'vue': ['vue.config.js', 'nuxt.config.js'],
        'django': ['manage.py', 'settings.py'],
        'flask': ['app.py', 'wsgi.py'],
        'fastapi': ['main.py'],  # Common FastAPI pattern
        'express': ['package.json'],  # Check for express in dependencies
        'angular': ['angular.json'],
        'svelte': ['svelte.config.js']
    }
    
    @staticmethod
    def detect_language(file_path: Path) -> Optional[str]:
        """
        Detect language from file extension.
        
        Args:
            file_path: Path to file
        
        Returns:
            Language name or None
        """
        suffix = file_path.suffix.lower()
        return LanguageDetector.EXTENSIONS.get(suffix)
    
    @staticmethod
    def detect_framework(project_path: Path) -> Optional[str]:
        """
        Detect framework by checking for config files.
        
        Args:
            project_path: Root path of project
        
        Returns:
            Framework name or None
        """
        project_path = Path(project_path)
        
        # Check for framework marker files
        for framework, markers in LanguageDetector.FRAMEWORK_MARKERS.items():
            for marker in markers:
                if (project_path / marker).exists():
                    # For package.json, check dependencies
                    if marker == 'package.json':
                        framework_name = LanguageDetector._check_package_json(
                            project_path / marker, 
                            framework
                        )
                        if framework_name:
                            return framework_name
                    else:
                        return framework
        
        return None
    
    @staticmethod
    def _check_package_json(package_path: Path, framework: str) -> Optional[str]:
        """
        Check package.json for specific framework dependencies.
        
        Args:
            package_path: Path to package.json
            framework: Framework to check for
        
        Returns:
            Framework name if found, None otherwise
        """
        try:
            with open(package_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            all_deps = {**dependencies, **dev_dependencies}
            
            # Check for framework-specific packages
            framework_packages = {
                'react': ['react', 'react-dom'],
                'express': ['express'],
                'vue': ['vue'],
                'angular': ['@angular/core']
            }
            
            if framework in framework_packages:
                for package in framework_packages[framework]:
                    if package in all_deps:
                        return framework
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def is_web_file(file_path: Path) -> bool:
        """
        Check if file is a web file (HTML, JSX, TSX).
        
        Args:
            file_path: Path to file
        
        Returns:
            True if web file, False otherwise
        """
        web_extensions = {'.html', '.htm', '.jsx', '.tsx', '.vue', '.svelte'}
        return file_path.suffix.lower() in web_extensions
    
    @staticmethod
    def is_code_file(file_path: Path) -> bool:
        """
        Check if file is a code file.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if code file, False otherwise
        """
        return file_path.suffix.lower() in LanguageDetector.EXTENSIONS
    
    @staticmethod
    def get_scannable_extensions() -> list:
        """
        Get list of all scannable file extensions.
        
        Returns:
            List of file extensions
        """
        return list(LanguageDetector.EXTENSIONS.keys())
