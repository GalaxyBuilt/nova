"""Advanced SEO scanner for premium features."""
import re
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


@dataclass
class AdvancedSEOIssue:
    """Advanced SEO issue found in premium scanning."""
    file_path: str
    issue_type: str
    severity: str
    message: str
    line_number: int = None
    details: Dict = None


class AdvancedSEOScanner:
    """Premium SEO scanner with advanced checks."""
    
    def __init__(self):
        self.checked_urls = set()
    
    def check_duplicate_meta_tags(self, content: str, file_path: Path) -> List[AdvancedSEOIssue]:
        """
        Check for duplicate meta tags.
        
        Args:
            content: File content
            file_path: Path to file
        
        Returns:
            List of issues found
        """
        issues = []
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for duplicate meta descriptions
        meta_descriptions = soup.find_all('meta', attrs={'name': 'description'})
        if len(meta_descriptions) > 1:
            issues.append(AdvancedSEOIssue(
                file_path=str(file_path),
                issue_type='duplicate_meta_description',
                severity='warning',
                message=f'Found {len(meta_descriptions)} meta description tags (should have only 1)'
            ))
        
        # Check for duplicate titles
        titles = soup.find_all('title')
        if len(titles) > 1:
            issues.append(AdvancedSEOIssue(
                file_path=str(file_path),
                issue_type='duplicate_title',
                severity='critical',
                message=f'Found {len(titles)} title tags (should have only 1)'
            ))
        
        # Check for duplicate canonical links
        canonicals = soup.find_all('link', attrs={'rel': 'canonical'})
        if len(canonicals) > 1:
            issues.append(AdvancedSEOIssue(
                file_path=str(file_path),
                issue_type='duplicate_canonical',
                severity='warning',
                message=f'Found {len(canonicals)} canonical links (should have only 1)'
            ))
        
        return issues
    
    def check_broken_links(self, content: str, file_path: Path, check_external: bool = False) -> List[AdvancedSEOIssue]:
        """
        Check for broken internal and external links.
        
        Args:
            content: File content
            file_path: Path to file
            check_external: Whether to check external URLs (slower)
        
        Returns:
            List of issues found
        """
        issues = []
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Skip anchors and javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Check internal links
            if href.startswith('/') or not href.startswith('http'):
                # Resolve relative path
                if href.startswith('/'):
                    # Absolute path from root
                    target_path = file_path.parent / href.lstrip('/')
                else:
                    # Relative path
                    target_path = file_path.parent / href
                
                if not target_path.exists():
                    issues.append(AdvancedSEOIssue(
                        file_path=str(file_path),
                        issue_type='broken_internal_link',
                        severity='warning',
                        message=f'Broken internal link: {href}',
                        details={'target': str(target_path)}
                    ))
            
            # Check external links (if enabled)
            elif check_external and href not in self.checked_urls:
                self.checked_urls.add(href)
                try:
                    response = requests.head(href, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        issues.append(AdvancedSEOIssue(
                            file_path=str(file_path),
                            issue_type='broken_external_link',
                            severity='warning',
                            message=f'Broken external link: {href} (status: {response.status_code})'
                        ))
                except requests.RequestException:
                    # Skip unreachable URLs (might be temporary)
                    pass
        
        return issues
    
    def validate_sitemap(self, project_path: Path) -> List[AdvancedSEOIssue]:
        """
        Validate sitemap.xml if it exists.
        
        Args:
            project_path: Root path of project
        
        Returns:
            List of issues found
        """
        issues = []
        sitemap_path = project_path / 'sitemap.xml'
        
        if not sitemap_path.exists():
            issues.append(AdvancedSEOIssue(
                file_path=str(project_path),
                issue_type='missing_sitemap',
                severity='info',
                message='No sitemap.xml found (recommended for SEO)'
            ))
            return issues
        
        # Parse sitemap
        try:
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'xml')
            
            # Check for required elements
            urls = soup.find_all('url')
            if not urls:
                issues.append(AdvancedSEOIssue(
                    file_path=str(sitemap_path),
                    issue_type='empty_sitemap',
                    severity='warning',
                    message='Sitemap exists but contains no URLs'
                ))
            
            # Validate URL structure
            for url in urls:
                loc = url.find('loc')
                if not loc:
                    issues.append(AdvancedSEOIssue(
                        file_path=str(sitemap_path),
                        issue_type='invalid_sitemap_entry',
                        severity='warning',
                        message='Sitemap entry missing <loc> element'
                    ))
        
        except Exception as e:
            issues.append(AdvancedSEOIssue(
                file_path=str(sitemap_path),
                issue_type='invalid_sitemap',
                severity='warning',
                message=f'Invalid sitemap.xml: {str(e)}'
            ))
        
        return issues
    
    def validate_robots_txt(self, project_path: Path) -> List[AdvancedSEOIssue]:
        """
        Validate robots.txt if it exists.
        
        Args:
            project_path: Root path of project
        
        Returns:
            List of issues found
        """
        issues = []
        robots_path = project_path / 'robots.txt'
        
        if not robots_path.exists():
            issues.append(AdvancedSEOIssue(
                file_path=str(project_path),
                issue_type='missing_robots_txt',
                severity='info',
                message='No robots.txt found (recommended for SEO)'
            ))
            return issues
        
        # Parse robots.txt
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common issues
            if 'Disallow: /' in content and 'Allow:' not in content:
                issues.append(AdvancedSEOIssue(
                    file_path=str(robots_path),
                    issue_type='robots_blocks_all',
                    severity='critical',
                    message='robots.txt blocks all crawlers (Disallow: /)'
                ))
            
            # Check for sitemap reference
            if 'Sitemap:' not in content:
                issues.append(AdvancedSEOIssue(
                    file_path=str(robots_path),
                    issue_type='robots_missing_sitemap',
                    severity='info',
                    message='robots.txt missing Sitemap reference'
                ))
        
        except Exception as e:
            issues.append(AdvancedSEOIssue(
                file_path=str(robots_path),
                issue_type='invalid_robots_txt',
                severity='warning',
                message=f'Invalid robots.txt: {str(e)}'
            ))
        
        return issues
    
    def detect_structured_data(self, content: str, file_path: Path) -> List[AdvancedSEOIssue]:
        """
        Detect and validate structured data (JSON-LD, microdata).
        
        Args:
            content: File content
            file_path: Path to file
        
        Returns:
            List of issues found
        """
        issues = []
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        
        # Check for microdata
        microdata_items = soup.find_all(attrs={'itemscope': True})
        
        if not json_ld_scripts and not microdata_items:
            issues.append(AdvancedSEOIssue(
                file_path=str(file_path),
                issue_type='missing_structured_data',
                severity='info',
                message='No structured data found (JSON-LD or microdata recommended for rich snippets)'
            ))
        
        return issues
