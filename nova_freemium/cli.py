"""Main CLI interface using Rich for beautiful output."""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from nova_freemium.scanner import ProjectScanner
from nova_freemium.scoring import ScoreCalculator
from nova_freemium.report import ReportGenerator

console = Console()


@click.group()
@click.version_option(version='1.0.0', prog_name='Nova')
def cli():
    """Nova - Code + SEO Health Scanner
    
    Illuminate your code and SEO risks. Fast. Clear. Actionable.
    """
    pass


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--json', 'output_json', is_flag=True, help='Export results as JSON')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--premium', is_flag=True, help='Enable premium features (requires license)')
def scan(project_path: str, output_json: bool, output: str, premium: bool):
    """Scan a project for SEO and complexity issues."""
    
    console.print(Panel.fit(
        "[bold cyan]Nova Scanner[/bold cyan]\n"
        "Analyzing your project...",
        border_style="cyan"
    ))
    
    # Scan project with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        
        scanner = ProjectScanner()
        results = scanner.scan_project(Path(project_path))
        
        # Premium features
        if premium:
            from nova_premium.license_manager import LicenseManager
            
            if not LicenseManager.check_license():
                console.print(LicenseManager.get_upgrade_message())
                console.print("\n[yellow]Continuing with freemium scan...[/yellow]\n")
            else:
                # Run premium SEO checks
                from nova_premium.advanced_seo import AdvancedSEOScanner
                from nova_shared.utils import get_project_files
                from nova_shared.language_detection import LanguageDetector
                
                console.print("[green]✓ Premium license validated[/green]")
                progress.update(task, description="Running premium SEO checks...")
                
                premium_scanner = AdvancedSEOScanner()
                premium_issues = []
                
                # Get web files for premium scanning
                web_files = [f for f in get_project_files(str(project_path), LanguageDetector.get_scannable_extensions()) 
                            if LanguageDetector.is_web_file(f)]
                
                for file_path in web_files:
                    from nova_shared.utils import read_file_safe
                    content = read_file_safe(file_path)
                    if not content:
                        continue
                    
                    # Premium checks
                    premium_issues.extend(premium_scanner.check_duplicate_meta_tags(content, file_path))
                    premium_issues.extend(premium_scanner.check_broken_links(content, file_path))
                    premium_issues.extend(premium_scanner.detect_structured_data(content, file_path))
                
                # Project-level checks
                premium_issues.extend(premium_scanner.validate_sitemap(Path(project_path)))
                premium_issues.extend(premium_scanner.validate_robots_txt(Path(project_path)))
                
                # Add premium issues to results
                results['premium_seo_issues'] = [
                    {
                        'file_path': issue.file_path,
                        'issue_type': issue.issue_type,
                        'severity': issue.severity,
                        'message': issue.message,
                        'line_number': issue.line_number,
                        'details': issue.details
                    }
                    for issue in premium_issues
                ]
        
        progress.update(task, completed=True)
    
    # Calculate scores
    calculator = ScoreCalculator()
    seo_score = calculator.calculate_seo_score(
        results['seo_issues'],
        results['files_scanned']
    )
    complexity_score = calculator.calculate_complexity_score(
        results['complexity_issues'],
        results['files_scanned'],
        advanced_metrics=results.get('advanced_metrics')
    )
    overall_score = calculator.calculate_overall_score(seo_score, complexity_score)
    
    scores = {
        'seo_score': seo_score,
        'complexity_score': complexity_score,
        'overall_score': overall_score,
        'seo_grade': calculator.get_grade(seo_score),
        'complexity_grade': calculator.get_grade(complexity_score),
        'overall_grade': calculator.get_grade(overall_score)
    }
    
    # Display results
    console.print()
    _display_scores(seo_score, complexity_score, overall_score)
    console.print()
    _display_summary(results)
    console.print()
    _display_issues(results)
    
    # Export if requested
    if output_json:
        output_path = output or 'nova_report.json'
        report_gen = ReportGenerator()
        report_gen.generate_json(results, scores, output_path)
        console.print(f"\n[green]✓[/green] Report saved to [cyan]{output_path}[/cyan]")


def _display_scores(seo_score: int, complexity_score: int, overall_score: int):
    """Display score table."""
    calculator = ScoreCalculator()
    
    table = Table(title="Health Scores", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right")
    table.add_column("Grade", justify="center")
    
    # SEO score
    seo_color = calculator.get_score_color(seo_score)
    table.add_row(
        "SEO Health",
        f"[{seo_color}]{seo_score}/100[/{seo_color}]",
        f"[{seo_color}]{calculator.get_grade(seo_score)}[/{seo_color}]"
    )
    
    # Complexity score
    complexity_color = calculator.get_score_color(complexity_score)
    table.add_row(
        "Code Complexity",
        f"[{complexity_color}]{complexity_score}/100[/{complexity_color}]",
        f"[{complexity_color}]{calculator.get_grade(complexity_score)}[/{complexity_color}]"
    )
    
    # Overall score
    overall_color = calculator.get_score_color(overall_score)
    table.add_row(
        "[bold]Overall Health[/bold]",
        f"[bold {overall_color}]{overall_score}/100[/bold {overall_color}]",
        f"[bold {overall_color}]{calculator.get_grade(overall_score)}[/bold {overall_color}]"
    )
    
    console.print(table)


def _display_summary(results: dict):
    """Display scan summary."""
    total_issues = len(results['seo_issues']) + len(results['complexity_issues'])
    
    summary_text = (
        f"[cyan]Files Scanned:[/cyan] {results['files_scanned']}\n"
        f"[cyan]Total Issues:[/cyan] {total_issues}\n"
        f"[cyan]Scan Time:[/cyan] {results['scan_time']}s"
    )
    
    console.print(Panel(summary_text, title="Scan Summary", border_style="blue"))


def _display_issues(results: dict):
    """Display issues found."""
    seo_issues = results['seo_issues']
    complexity_issues = results['complexity_issues']
    
    # Display SEO issues
    if seo_issues:
        console.print("[bold yellow]SEO Issues:[/bold yellow]")
        seo_table = Table(show_header=True, header_style="bold yellow")
        seo_table.add_column("File", style="cyan", no_wrap=False)
        seo_table.add_column("Issue", style="white")
        seo_table.add_column("Severity", justify="center")
        
        for issue in seo_issues[:10]:  # Show first 10
            severity = issue['severity']
            severity_color = 'red' if severity == 'critical' else 'yellow' if severity == 'warning' else 'blue'
            
            seo_table.add_row(
                Path(issue['file_path']).name,
                issue['message'],
                f"[{severity_color}]{severity}[/{severity_color}]"
            )
        
        console.print(seo_table)
        
        if len(seo_issues) > 10:
            console.print(f"[dim]... and {len(seo_issues) - 10} more SEO issues[/dim]")
        console.print()
    
    # Display complexity issues
    if complexity_issues:
        console.print("[bold magenta]Complexity Issues:[/bold magenta]")
        complexity_table = Table(show_header=True, header_style="bold magenta")
        complexity_table.add_column("File", style="cyan", no_wrap=False)
        complexity_table.add_column("Issue", style="white")
        complexity_table.add_column("Line", justify="right")
        complexity_table.add_column("Severity", justify="center")
        
        for issue in complexity_issues[:10]:  # Show first 10
            severity = issue['severity']
            severity_color = 'red' if severity == 'critical' else 'yellow' if severity == 'warning' else 'blue'
            
            complexity_table.add_row(
                Path(issue['file_path']).name,
                issue['message'],
                str(issue.get('line_number', '-')),
                f"[{severity_color}]{severity}[/{severity_color}]"
            )
        
        console.print(complexity_table)
        
        if len(complexity_issues) > 10:
            console.print(f"[dim]... and {len(complexity_issues) - 10} more complexity issues[/dim]")
    
    # If no issues
    if not seo_issues and not complexity_issues:
        console.print("[bold green]✓ No issues found! Your project looks great![/bold green]")


if __name__ == '__main__':
    cli()
