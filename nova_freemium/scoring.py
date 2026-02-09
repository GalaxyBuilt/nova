"""Scoring algorithms for SEO and complexity."""
from typing import List, Dict


class ScoreCalculator:
    """Calculate SEO and Complexity scores (0-100)."""
    
    # Severity weights
    SEVERITY_WEIGHTS = {
        'critical': 10,
        'warning': 5,
        'info': 1
    }
    
    @staticmethod
    def calculate_seo_score(issues: List[Dict], files_scanned: int) -> int:
        """
        Calculate SEO score based on issues found.
        
        Formula:
        - Start at 100
        - Deduct points based on severity and count
        - Normalize by number of files scanned
        
        Args:
            issues: List of SEO issues (as dicts)
            files_scanned: Number of files scanned
        
        Returns:
            Score from 0-100
        """
        if files_scanned == 0:
            return 100
        
        total_deduction = 0
        for issue in issues:
            severity = issue.get('severity', 'info')
            total_deduction += ScoreCalculator.SEVERITY_WEIGHTS.get(severity, 1)
        
        # Normalize deduction by files scanned
        normalized_deduction = (total_deduction / files_scanned) * 10
        score = max(0, 100 - normalized_deduction)
        
        return int(score)
    
    @staticmethod
    def calculate_complexity_score(issues: List[Dict], files_scanned: int, advanced_metrics: Dict = None) -> int:
        """
        Calculate complexity score based on issues found.
        
        Phase 2 Enhancement: Includes cyclomatic complexity and coupling metrics
        
        Args:
            issues: List of complexity issues (as dicts)
            files_scanned: Number of files scanned
            advanced_metrics: Optional dict with avg_cyclomatic_complexity and avg_coupling
        
        Returns:
            Score from 0-100
        """
        if files_scanned == 0:
            return 100
        
        base_score = 100
        
        # Deduct for issues
        total_deduction = 0
        for issue in issues:
            severity = issue.get('severity', 'info')
            total_deduction += ScoreCalculator.SEVERITY_WEIGHTS.get(severity, 1)
        
        # Normalize deduction by files scanned
        normalized_deduction = (total_deduction / files_scanned) * 10
        base_score -= normalized_deduction
        
        # Phase 2: Deduct for high cyclomatic complexity
        if advanced_metrics:
            avg_cyclomatic = advanced_metrics.get('avg_cyclomatic_complexity', 0)
            if avg_cyclomatic > 10:
                base_score -= (avg_cyclomatic - 10) * 2
            
            # Phase 2: Deduct for high coupling
            avg_coupling = advanced_metrics.get('avg_coupling', 0)
            if avg_coupling > 0.7:
                base_score -= (avg_coupling - 0.7) * 50
        
        score = max(0, min(100, base_score))
        return int(score)
    
    @staticmethod
    def calculate_overall_score(seo_score: int, complexity_score: int) -> int:
        """
        Calculate overall health score (weighted average).
        
        Args:
            seo_score: SEO score (0-100)
            complexity_score: Complexity score (0-100)
        
        Returns:
            Overall score (0-100)
        """
        # 60% SEO, 40% Complexity
        return int(seo_score * 0.6 + complexity_score * 0.4)
    
    @staticmethod
    def get_grade(score: int) -> str:
        """
        Convert score to letter grade.
        
        Args:
            score: Score (0-100)
        
        Returns:
            Letter grade (A-F)
        """
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def get_score_color(score: int) -> str:
        """
        Get color for score display (Rich color names).
        
        Args:
            score: Score (0-100)
        
        Returns:
            Rich color name
        """
        if score >= 90:
            return 'green'
        elif score >= 80:
            return 'cyan'
        elif score >= 70:
            return 'yellow'
        elif score >= 60:
            return 'orange'
        else:
            return 'red'
