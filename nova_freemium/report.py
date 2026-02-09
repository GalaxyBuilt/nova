"""Report generation utilities."""
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


class ReportGenerator:
    """Generate reports in various formats."""
    
    def generate_json(self, results: Dict, scores: Dict, output_path: str):
        """
        Generate JSON report.
        
        Args:
            results: Scan results from ProjectScanner
            scores: Calculated scores
            output_path: Path to save report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'project_path': results.get('project_path', ''),
            'scan_time': results.get('scan_time', 0),
            'files_scanned': results.get('files_scanned', 0),
            'scores': scores,
            'seo_issues': results.get('seo_issues', []),
            'complexity_issues': results.get('complexity_issues', []),
            'summary': {
                'total_issues': len(results.get('seo_issues', [])) + len(results.get('complexity_issues', [])),
                'critical_issues': self._count_by_severity(results, 'critical'),
                'warnings': self._count_by_severity(results, 'warning'),
                'info': self._count_by_severity(results, 'info')
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
    
    def _count_by_severity(self, results: Dict, severity: str) -> int:
        """Count issues by severity level."""
        count = 0
        
        for issue in results.get('seo_issues', []):
            if issue.get('severity') == severity:
                count += 1
        
        for issue in results.get('complexity_issues', []):
            if issue.get('severity') == severity:
                count += 1
        
        return count
