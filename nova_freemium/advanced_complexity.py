"""Advanced complexity analysis module for Phase 2."""
import ast
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CyclomaticComplexity:
    """Cyclomatic complexity metrics for a function."""
    function_name: str
    complexity: int
    line_number: int


class AdvancedComplexityAnalyzer:
    """Advanced complexity analysis including cyclomatic complexity and coupling."""
    
    def calculate_cyclomatic_complexity_python(self, content: str, file_path: Path) -> List[CyclomaticComplexity]:
        """
        Calculate cyclomatic complexity for Python functions.
        
        Cyclomatic complexity = edges - nodes + 2 (for connected components)
        Simplified: count decision points + 1
        
        Args:
            content: File content
            file_path: Path to file
        
        Returns:
            List of cyclomatic complexity metrics
        """
        results = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_function_complexity(node)
                    
                    results.append(CyclomaticComplexity(
                        function_name=node.name,
                        complexity=complexity,
                        line_number=node.lineno
                    ))
        except SyntaxError:
            pass
        
        return results
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """
        Calculate complexity for a single function.
        
        Decision points that increase complexity:
        - if, elif
        - for, while
        - and, or (boolean operators)
        - except handlers
        - with statements
        - comprehensions
        """
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            # Conditional statements
            if isinstance(node, ast.If):
                complexity += 1
            # Loops
            elif isinstance(node, (ast.For, ast.While)):
                complexity += 1
            # Boolean operators
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            # Exception handlers
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            # Comprehensions
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                complexity += 1
            # With statements
            elif isinstance(node, ast.With):
                complexity += 1
        
        return complexity
    
    def analyze_coupling(self, project_path: Path) -> Dict[str, Dict]:
        """
        Analyze coupling between modules.
        
        Coupling metrics:
        - Afferent coupling (Ca): Number of modules that depend on this module
        - Efferent coupling (Ce): Number of modules this module depends on
        - Instability (I): Ce / (Ca + Ce) - ranges from 0 (stable) to 1 (unstable)
        
        Args:
            project_path: Root path of project
        
        Returns:
            Dict mapping file paths to coupling metrics
        """
        from nova_shared.utils import get_project_files
        
        # Get all Python files
        python_files = get_project_files(str(project_path), ['.py'])
        
        # Track imports
        import_graph = {}  # file -> list of imported files
        
        for file_path in python_files:
            imports = self._extract_imports(file_path)
            import_graph[str(file_path)] = imports
        
        # Calculate coupling metrics
        coupling_metrics = {}
        
        for file_path in python_files:
            file_str = str(file_path)
            
            # Efferent coupling: modules this file imports
            efferent = len(import_graph.get(file_str, []))
            
            # Afferent coupling: modules that import this file
            afferent = sum(
                1 for imports in import_graph.values()
                if file_str in imports or file_path.stem in imports
            )
            
            # Instability
            total = afferent + efferent
            instability = efferent / total if total > 0 else 0
            
            coupling_metrics[file_str] = {
                'afferent': afferent,
                'efferent': efferent,
                'instability': round(instability, 2),
                'total_coupling': total
            }
        
        return coupling_metrics
    
    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract import statements from a Python file."""
        from nova_shared.utils import read_file_safe
        
        imports = []
        content = read_file_safe(file_path)
        
        if not content:
            return imports
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except SyntaxError:
            pass
        
        return imports
    
    def get_high_complexity_functions(
        self,
        complexity_results: List[CyclomaticComplexity],
        threshold: int = 10
    ) -> List[CyclomaticComplexity]:
        """
        Filter functions with complexity above threshold.
        
        Args:
            complexity_results: List of complexity metrics
            threshold: Complexity threshold (default: 10)
        
        Returns:
            List of high-complexity functions
        """
        return [
            result for result in complexity_results
            if result.complexity > threshold
        ]
    
    def get_highly_coupled_modules(
        self,
        coupling_metrics: Dict[str, Dict],
        instability_threshold: float = 0.7
    ) -> Dict[str, Dict]:
        """
        Filter modules with high coupling/instability.
        
        Args:
            coupling_metrics: Coupling metrics dict
            instability_threshold: Instability threshold (default: 0.7)
        
        Returns:
            Dict of highly coupled modules
        """
        return {
            file_path: metrics
            for file_path, metrics in coupling_metrics.items()
            if metrics['instability'] > instability_threshold
        }
