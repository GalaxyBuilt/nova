# Nova Implementation Plan

## Quick Reference

This document provides the technical blueprint for building Nova across 8 phases. See `TASKS.md` for the detailed checklist.

---

## Architecture

```
Nova CLI
├── Freemium Scanner (Basic SEO + Complexity)
├── Premium Scanner (Advanced + AI)
├── Shared Utilities (File ops, language detection)
├── Scoring Engine (0-100 scores)
└── Reports (JSON, HTML)
```

---

## Phase 1: Freemium Core

### Modules to Build

1. **`nova_shared/utils.py`** - File operations, path handling, ignore patterns
2. **`nova_shared/language_detection.py`** - Detect Python, JS, TS, JSX, TSX, frameworks
3. **`nova_freemium/scanner.py`** - SEO & complexity scanning engine
4. **`nova_freemium/scoring.py`** - Calculate 0-100 scores with severity weights
5. **`nova_freemium/cli.py`** - CLI with Rich output, `nova scan <folder>`
6. **`nova_freemium/report.py`** - JSON export

### SEO Checks (Freemium)
- Missing `<title>` tag
- Missing meta description
- Missing canonical link
- Basic Open Graph tags

### Complexity Checks (Freemium)
- Function length (> 50 lines)
- File length (> 500 lines)
- Nested loops (> 3 levels)

### Scoring Formula
```python
# Start at 100, deduct based on severity
SEVERITY_WEIGHTS = {'critical': 10, 'warning': 5, 'info': 1}
score = max(0, 100 - (total_deduction / files_scanned) * 10)
overall = seo_score * 0.6 + complexity_score * 0.4
```

---

## Phase 2: Advanced Complexity

### New Metrics
- **Cyclomatic Complexity**: AST parsing (Python), esprima (JS/TS)
- **Coupling Detection**: Track imports/dependencies
- **Churn Detection**: Git history analysis (optional)

### Enhanced Scoring
```python
base_score = 100
if cyclomatic_avg > 10:
    base_score -= (cyclomatic_avg - 10) * 2
if coupling_score > 0.7:
    base_score -= (coupling_score - 0.7) * 50
```

---

## Phase 3: Premium Gating

### License Manager (`nova_premium/__init__.py`)
```python
class LicenseManager:
    @staticmethod
    def check_license() -> bool:
        key = os.getenv('NOVA_LICENSE_KEY')
        return _validate_key(key)  # JWT or API validation
```

### Advanced SEO Checks (Premium)
- Duplicate meta tags
- Broken links (internal/external)
- sitemap.xml validation
- robots.txt validation
- Structured data (JSON-LD, microdata)

---

## Phase 4: AI Assistant

### Integration (`nova_premium/ai_assistant.py`)
```python
class AIAssistant:
    def get_seo_suggestions(file_path, content, issues):
        # Call Anthropic/OpenAI API
        # Return suggestions + auto-fixes
    
    def apply_auto_fix(file_path, fix):
        # Apply suggested fix with user confirmation
```

### CLI Usage
```bash
nova scan <folder> --ai  # Premium only
```

---

## Phase 5: HTML Reports

### Template (`nova_premium/html_report.py`)
- Dark theme with gradients
- Color-coded issues (red=critical, yellow=warning, blue=info)
- Score cards with visual indicators
- Responsive design

---

## Phase 6: Multi-Language Support

### Framework Detection
```python
FRAMEWORK_MARKERS = {
    'next.js': ['next.config.js'],
    'react': ['package.json'],  # Check dependencies
    'django': ['manage.py'],
    'flask': ['app.py']
}
```

### Plugin System
- Allow custom rules
- Extensible file type support
- Document plugin API

---

## Phase 7: PyPI Packaging

### `pyproject.toml`
```toml
[project]
name = "nova-scanner"
version = "1.0.0"
dependencies = ["click>=8.0", "rich>=13.0", "beautifulsoup4>=4.11"]

[project.optional-dependencies]
premium = ["anthropic>=0.18", "jinja2>=3.1"]

[project.scripts]
nova = "nova_freemium.cli:cli"
```

### Installation
```bash
pip install nova-scanner          # Freemium
pip install nova-scanner[premium] # Premium
```

---

## Phase 8: Enhancements

- GitHub Actions integration
- Google PageSpeed Insights API
- Historical trends tracking
- Multi-project comparisons
- Performance optimization (parallel processing, caching)

---

## Git Setup

```bash
cd Nova
git init
git config user.name "galaxybuilt"
git config user.email "exoticdevlabs@gmail.com"
git remote add origin https://github.com/GalaxyBuilt/nova.git
```

---

## Dependencies

### Freemium
- `click` - CLI framework
- `rich` - Terminal formatting
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests

### Premium
- `anthropic` or `openai` - AI assistant
- `jinja2` - HTML templates
- `pytest` - Testing (dev)

---

## Testing Strategy

### Unit Tests
- Test each scanner function independently
- Mock file system operations
- Test scoring algorithms with known inputs

### Integration Tests
- Test full CLI commands
- Verify JSON/HTML output format
- Test premium gating

### Target: >80% code coverage

---

## Next Steps

1. ✅ Review this plan
2. Begin Phase 1 implementation
3. Create project structure
4. Implement shared utilities
5. Build freemium scanner
6. Test on sample projects
