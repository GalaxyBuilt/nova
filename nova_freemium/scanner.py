"""Core scanning engine for SEO and complexity analysis."""
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class SEOIssue:
    """Represents an SEO issue found in a file."""
    file_path: str
    issue_type: str
    severity: str  # 'critical', 'warning', 'info'
    message: str
    line_number: Optional[int] = None


@dataclass
class ComplexityIssue:
    """Represents a complexity issue found in code."""
    file_path: str
    issue_type: str
    severity: str
    message: str
    line_number: Optional[int] = None
    metric_value: Optional[float] = None


class SEOScanner:
    """Scan files for SEO issues."""
    
    def scan_file(self, file_path: Path, content: str) -> List[SEOIssue]:
        """
        Scan a single file for SEO issues.
        
        Args:
            file_path: Path to file
            content: File content
        
        Returns:
            List of SEO issues found
        """
        issues = []
        
        # Check for missing title tag
        if not self._has_title_tag(content):
            issues.append(SEOIssue(
                file_path=str(file_path),
                issue_type='missing_title',
                severity='critical',
                message='Missing <title> tag'
            ))
        
        # Check for missing meta description
        if not self._has_meta_description(content):
            issues.append(SEOIssue(
                file_path=str(file_path),
                issue_type='missing_meta_description',
                severity='warning',
                message='Missing meta description tag'
            ))
        
        # Check for missing canonical
        if not self._has_canonical(content):
            issues.append(SEOIssue(
                file_path=str(file_path),
                issue_type='missing_canonical',
                severity='info',
                message='Missing canonical link (recommended for SEO)'
            ))
        
        # Check for Open Graph tags
        og_issues = self._check_og_tags(content, file_path)
        issues.extend(og_issues)
        
        return issues
    
    def _has_title_tag(self, content: str) -> bool:
        """Check if content has a title tag."""
        return bool(re.search(r'<title[^>]*>.*?</title>', content, re.IGNORECASE | re.DOTALL))
    
    def _has_meta_description(self, content: str) -> bool:
        """Check if content has meta description."""
        pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\'][^"\']+["\'][^>]*>'
        return bool(re.search(pattern, content, re.IGNORECASE))
    
    def _has_canonical(self, content: str) -> bool:
        """Check if content has canonical link."""
        pattern = r'<link[^>]*rel=["\']canonical["\'][^>]*>'
        return bool(re.search(pattern, content, re.IGNORECASE))
    
    def _check_og_tags(self, content: str, file_path: Path) -> List[SEOIssue]:
        """Check for Open Graph tags."""
        issues = []
        
        og_tags = {
            'og:title': 'Open Graph title',
            'og:description': 'Open Graph description',
            'og:image': 'Open Graph image',
            'og:url': 'Open Graph URL'
        }
        
        for tag, description in og_tags.items():
            pattern = f'<meta[^>]*property=["\']?{tag}["\']?[^>]*>'
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append(SEOIssue(
                    file_path=str(file_path),
                    issue_type=f'missing_{tag.replace(":", "_")}',
                    severity='info',
                    message=f'Missing {description} (recommended for social sharing)'
                ))
        
        return issues


class ComplexityScanner:
    """Scan code files for complexity issues."""
    
    def scan_file(self, file_path: Path, content: str, language: str) -> List[ComplexityIssue]:
        """
        Scan a single file for complexity issues.
        
        Args:
            file_path: Path to file
            content: File content
            language: Programming language
        
        Returns:
            List of complexity issues found
        """
        issues = []
        
        # Check file length
        file_length_issue = self._check_file_length(content, file_path)
        if file_length_issue:
            issues.append(file_length_issue)
        
        # Check function length (language-specific)
        if language == 'python':
            function_issues = self._check_python_function_length(content, file_path)
            issues.extend(function_issues)
            
            # Check nested loops
            nested_loop_issues = self._check_python_nested_loops(content, file_path)
            issues.extend(nested_loop_issues)
        elif language in ['javascript', 'typescript']:
            function_issues = self._check_js_function_length(content, file_path)
            issues.extend(function_issues)
        
        return issues
    
    def _check_file_length(self, content: str, file_path: Path) -> Optional[ComplexityIssue]:
        """Check if file is too long."""
        lines = content.count('\n') + 1
        
        if lines > 500:
            return ComplexityIssue(
                file_path=str(file_path),
                issue_type='long_file',
                severity='warning',
                message=f'File has {lines} lines (recommended: < 500)',
                metric_value=lines
            )
        
        return None
    
    def _check_python_function_length(self, content: str, file_path: Path) -> List[ComplexityIssue]:
        """Check for overly long Python functions."""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Calculate function length
                    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                        func_length = node.end_lineno - node.lineno + 1
                        
                        if func_length > 50:
                            issues.append(ComplexityIssue(
                                file_path=str(file_path),
                                issue_type='long_function',
                                severity='warning',
                                message=f'Function "{node.name}" has {func_length} lines (recommended: < 50)',
                                line_number=node.lineno,
                                metric_value=func_length
                            ))
        except SyntaxError:
            # Skip files with syntax errors
            pass
        
        return issues
    
    def _check_python_nested_loops(self, content: str, file_path: Path) -> List[ComplexityIssue]:
        """Check for deeply nested loops in Python."""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            def check_nesting(node, depth=0):
                if isinstance(node, (ast.For, ast.While)):
                    depth += 1
                    if depth > 3:
                        issues.append(ComplexityIssue(
                            file_path=str(file_path),
                            issue_type='nested_loops',
                            severity='warning',
                            message=f'Deeply nested loops (depth: {depth}) - consider refactoring',
                            line_number=node.lineno,
                            metric_value=depth
                        ))
                
                for child in ast.iter_child_nodes(node):
                    check_nesting(child, depth)
            
            check_nesting(tree)
        except SyntaxError:
            pass
        
        return issues
    
    def _check_js_function_length(self, content: str, file_path: Path) -> List[ComplexityIssue]:
        """Check for overly long JavaScript/TypeScript functions."""
        issues = []
        
        # Simple regex-based detection for JS functions
        # Matches: function name() { ... }, const name = () => { ... }
        function_pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)\s*\{'
        
        lines = content.split('\n')
        in_function = False
        function_start = 0
        function_name = ''
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            if not in_function:
                match = re.search(function_pattern, line)
                if match:
                    in_function = True
                    function_start = i
                    function_name = match.group(1) or match.group(2) or 'anonymous'
                    brace_count = line.count('{') - line.count('}')
            else:
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    func_length = i - function_start + 1
                    if func_length > 50:
                        issues.append(ComplexityIssue(
                            file_path=str(file_path),
                            issue_type='long_function',
                            severity='warning',
                            message=f'Function "{function_name}" has {func_length} lines (recommended: < 50)',
                            line_number=function_start,
                            metric_value=func_length
                        ))
                    in_function = False
        
        return issues


class ProjectScanner:
    """Main scanner orchestrator."""
    
    def __init__(self):
        self.seo_scanner = SEOScanner()
        self.complexity_scanner = ComplexityScanner()
    
    def scan_project(self, project_path: Path, include_advanced: bool = True) -> Dict:
        """
        Scan entire project and return results.
        
        Args:
            project_path: Root path of project
            include_advanced: Include Phase 2 advanced metrics (cyclomatic complexity, coupling)
        
        Returns:
            Dict with scan results
        """
        from nova_shared.utils import get_project_files
        from nova_shared.language_detection import LanguageDetector
        
        start_time = time.time()
        
        # Get all scannable files
        extensions = LanguageDetector.get_scannable_extensions()
        files = get_project_files(str(project_path), extensions)
        
        seo_issues = []
        complexity_issues = []
        files_scanned = 0
        
        # Phase 2: Advanced metrics
        cyclomatic_results = []
        coupling_metrics = {}
        
        for file_path in files:
            from nova_shared.utils import read_file_safe
            
            content = read_file_safe(file_path)
            if not content:
                continue
            
            files_scanned += 1
            language = LanguageDetector.detect_language(file_path)
            
            # Scan for SEO issues (only web files)
            if LanguageDetector.is_web_file(file_path):
                file_seo_issues = self.seo_scanner.scan_file(file_path, content)
                seo_issues.extend(file_seo_issues)
            
            # Scan for complexity issues (code files)
            if language:
                file_complexity_issues = self.complexity_scanner.scan_file(
                    file_path, content, language
                )
                complexity_issues.extend(file_complexity_issues)
                
                # Phase 2: Cyclomatic complexity for Python files
                if include_advanced and language == 'python':
                    from nova_freemium.advanced_complexity import AdvancedComplexityAnalyzer
                    
                    analyzer = AdvancedComplexityAnalyzer()
                    file_cyclomatic = analyzer.calculate_cyclomatic_complexity_python(content, file_path)
                    
                    # Add high complexity functions as issues
                    high_complexity = analyzer.get_high_complexity_functions(file_cyclomatic, threshold=10)
                    for func in high_complexity:
                        complexity_issues.append({
                            'file_path': str(file_path),
                            'issue_type': 'high_cyclomatic_complexity',
                            'severity': 'warning',
                            'message': f'Function "{func.function_name}" has cyclomatic complexity of {func.complexity} (recommended: < 10)',
                            'line_number': func.line_number,
                            'metric_value': func.complexity
                        })
                    
                    cyclomatic_results.extend(file_cyclomatic)
        
        # Phase 2: Coupling analysis
        if include_advanced:
            from nova_freemium.advanced_complexity import AdvancedComplexityAnalyzer
            
            analyzer = AdvancedComplexityAnalyzer()
            coupling_metrics = analyzer.analyze_coupling(project_path)
            
            # Add highly coupled modules as issues
            highly_coupled = analyzer.get_highly_coupled_modules(coupling_metrics, instability_threshold=0.7)
            for file_path, metrics in highly_coupled.items():
                complexity_issues.append({
                    'file_path': file_path,
                    'issue_type': 'high_coupling',
                    'severity': 'info',
                    'message': f'Module has high coupling (instability: {metrics["instability"]}, total coupling: {metrics["total_coupling"]})',
                    'line_number': None,
                    'metric_value': metrics['instability']
                })
        
        scan_time = time.time() - start_time
        
        # Calculate average cyclomatic complexity
        avg_cyclomatic = 0
        if cyclomatic_results:
            avg_cyclomatic = sum(r.complexity for r in cyclomatic_results) / len(cyclomatic_results)
        
        # Calculate average coupling
        avg_coupling = 0
        if coupling_metrics:
            avg_coupling = sum(m['instability'] for m in coupling_metrics.values()) / len(coupling_metrics)
        
        return {
            'seo_issues': [asdict(issue) if hasattr(issue, '__dataclass_fields__') else issue for issue in seo_issues],
            'complexity_issues': [asdict(issue) if hasattr(issue, '__dataclass_fields__') else issue for issue in complexity_issues],
            'files_scanned': files_scanned,
            'scan_time': round(scan_time, 2),
            'project_path': str(project_path),
            'advanced_metrics': {
                'avg_cyclomatic_complexity': round(avg_cyclomatic, 2),
                'avg_coupling': round(avg_coupling, 2),
                'total_functions_analyzed': len(cyclomatic_results),
                'total_modules_analyzed': len(coupling_metrics)
            } if include_advanced else None
        }
