# Nova Scanner - Quick Start Guide

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install click rich beautifulsoup4 requests
```

## Usage

```bash
# Basic scan
python -m nova_freemium.cli scan <project_folder>

# Export to JSON
python -m nova_freemium.cli scan <project_folder> --json --output report.json
```

## What's Been Built

### ✅ Phase 1 - Freemium Core (COMPLETE)
- **Shared Utilities**: File operations, language detection (Python, JS, TS, React, etc.)
- **SEO Scanner**: Detects missing title, meta description, canonical, OG tags
- **Complexity Scanner**: Checks file length, function length, nested loops
- **Scoring System**: 0-100 scores with letter grades (A-F)
- **CLI**: Beautiful Rich-powered terminal output with color-coded results
- **JSON Reports**: Export scan results with timestamps and summaries

### ✅ Phase 2 - Advanced Complexity (COMPLETE)
- **Cyclomatic Complexity**: AST-based analysis for Python functions
- **Coupling Detection**: Afferent/Efferent coupling and instability metrics
- **Enhanced Scoring**: Deductions for high complexity and coupling
- **Advanced Metrics**: Average cyclomatic complexity and coupling in reports

## Project Structure

```
Nova/
├── nova_shared/
│   ├── __init__.py
│   ├── utils.py                    # File operations, ignore patterns
│   └── language_detection.py       # Language & framework detection
├── nova_freemium/
│   ├── __init__.py
│   ├── scanner.py                  # Core SEO & complexity scanning
│   ├── advanced_complexity.py      # Phase 2: Cyclomatic & coupling
│   ├── scoring.py                  # Score calculation (0-100)
│   ├── report.py                   # JSON report generation
│   └── cli.py                      # Rich CLI interface
├── pyproject.toml                  # Package configuration
├── LICENSE                         # MIT License
├── .gitignore                      # Python gitignore
├── README.md                       # Full documentation
├── TASKS.md                        # Development checklist
└── IMPLEMENTATION_PLAN.md          # Technical blueprint
```

## Next Steps

### Phase 3 - Premium Features
- License/API key gating
- Advanced SEO checks (broken links, sitemap validation)
- Structured data detection

### Phase 4 - AI Integration
- Anthropic Claude / OpenAI integration
- AI-powered fix suggestions
- Auto-fix functionality

### Phase 5 - HTML Reports
- Visual HTML reports with charts
- Color-coded issue highlighting

### Phase 6-8
- Multi-language support expansion
- PyPI packaging
- GitHub deployment

## Testing

To test the scanner on a sample project:

```bash
# Test on Nova itself
python -m nova_freemium.cli scan . --json --output nova_self_scan.json
```

## Notes

- The import errors in the IDE are expected until dependencies are installed
- The scanner is fully functional for Phase 1 & 2 features
- Phase 3+ features will be gated behind premium licensing

---

**Built by @GalaxyBuilt** | galaxy@txchyon.com
