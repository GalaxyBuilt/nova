# Nova – Code & SEO Health Scanner

**Illuminate your code and SEO risks. Fast. Clear. Actionable.**

Nova is a modular, pip-installable tool for developers that scans your project folder in under a minute. It detects SEO issues, code complexity hotspots, and gives actionable recommendations. Perfect for Python, JavaScript, TypeScript, React, Next.js, and Node.js projects.

---

## Features

### Freemium (Free)
- Scan project folders and files (`.py`, `.js`, `.ts`, `.jsx`, `.tsx`)  
- Detect basic SEO issues: missing title, meta description, canonical, simple Open Graph tags  
- Basic complexity metrics: function length, file length, nested loops  
- Generates **SEO Score** and **Complexity Score** (0–100)  
- Export results as JSON  
- Fully functional CLI with color-coded output

### Premium (Optional Upgrade)
- Advanced SEO checks: duplicate meta tags, broken internal links, sitemap/robots validation  
- Structured data / schema detection & AI-assisted fixes (Article, Product, FAQ)  
- Advanced complexity radar: cyclomatic complexity, coupling, file churn, hotspots  
- HTML reports with visual highlights  
- Interactive AI assistant in CLI for actionable suggestions and auto-fixes  
- Optional GitHub Actions / CI integration for scanning PRs  
- Historical trends and multi-project comparisons  

---

## Installation

### Freemium Version
```bash
pip install nova-scanner
```

### Premium Version
```bash
pip install nova-scanner[premium]
```

Set your license key as an environment variable:
```bash
# Windows (PowerShell)
$env:NOVA_LICENSE_KEY="your-license-key-here"

# macOS/Linux
export NOVA_LICENSE_KEY="your-license-key-here"
```

For AI features, also set your AI API key:
```bash
# For Claude (recommended)
export ANTHROPIC_API_KEY="your-anthropic-key"

# Or for OpenAI
export OPENAI_API_KEY="your-openai-key"
```

---

## Quickstart

Scan your project folder:

```bash
nova scan <project-folder>
```

Export a JSON report:

```bash
nova scan <project-folder> --json
```

Specify output file:

```bash
nova scan <project-folder> --json --output report.json
```

Premium users can generate HTML reports and use AI assistance:

```bash
# Generate HTML report
nova scan <project-folder> --html

# Enable AI suggestions
nova scan <project-folder> --ai

# Combine features
nova scan <project-folder> --html --ai --output my-report.html
```

---

## Premium Upgrade

Unlock the full power of Nova with **Nova Premium**:

* AI-assisted fixes for SEO & structured data
* Advanced code complexity analysis (cyclomatic complexity, coupling detection)
* Interactive CLI suggestions with auto-fix capabilities
* Beautiful HTML reporting with visual danger zones
* GitHub Actions integration for automated PR scanning
* Historical trends and multi-project comparisons

> **Upgrade to Nova Premium for $10/month**
> 
> Visit [https://nova-scanner.dev/premium](https://nova-scanner.dev/premium) to get your license key.

---

## CLI Overview

| Command              | Description                     | Availability |
| -------------------- | ------------------------------- | ------------ |
| `nova scan <folder>` | Run a full project scan         | Free         |
| `--json`             | Export JSON report              | Free         |
| `--output <path>`    | Specify output file path        | Free         |
| `--html`             | Export HTML report              | Premium      |
| `--ai`               | Enable AI suggestions           | Premium      |

### Output Color Coding

* 🔴 **Red** = Critical issues (missing title tags, high complexity)
* 🟡 **Yellow** = Warnings (missing meta descriptions, moderate complexity)
* 🟢 **Green** = OK / Passing

### Score Grading

- **90-100**: Grade A (Excellent)
- **80-89**: Grade B (Good)
- **70-79**: Grade C (Fair)
- **60-69**: Grade D (Needs Improvement)
- **0-59**: Grade F (Critical Issues)

---

## Supported Languages & Frameworks

### Languages
* Python (`.py`)
* JavaScript (`.js`)
* TypeScript (`.ts`)
* JSX (`.jsx`)
* TSX (`.tsx`)
* HTML (`.html`)
* CSS/SCSS (`.css`, `.scss`)

### Frameworks Detected
* React
* Next.js
* Django
* Flask
* Node.js

---

## Development Setup

### Clone the Repository

```bash
git clone https://github.com/GalaxyBuilt/nova.git
cd nova
```

### Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
# Install in development mode
pip install -e .

# Install with premium dependencies
pip install -e .[premium]

# Install development dependencies
pip install -e .[dev]
```

### Run Tests

```bash
pytest

# With coverage
pytest --cov=nova_freemium --cov=nova_premium --cov=nova_shared
```

### Project Structure

```
nova/
├── nova_shared/          # Shared utilities
│   ├── utils.py
│   └── language_detection.py
├── nova_freemium/        # Free version modules
│   ├── cli.py
│   ├── scanner.py
│   ├── scoring.py
│   └── report.py
├── nova_premium/         # Premium modules
│   ├── __init__.py       # License gating
│   ├── advanced_scanner.py
│   ├── ai_assistant.py
│   ├── html_report.py
│   └── integrations.py
├── tests/                # Test suite
├── examples/             # Sample projects
├── TASKS.md              # Development checklist
├── IMPLEMENTATION_PLAN.md # Detailed technical plan
├── pyproject.toml        # Package configuration
└── README.md
```

---

## Example Output

### Terminal Output (Freemium)

```
╭─────────────────────────────╮
│ Nova Scanner                │
│ Analyzing your project...   │
╰─────────────────────────────╯

Health Scores
┏━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Metric          ┃ Score ┃ Grade ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ SEO Health      │ 85/100│   B   │
│ Code Complexity │ 78/100│   C   │
│ Overall Health  │ 82/100│   B   │
└─────────────────┴───────┴───────┘

✓ Report saved to nova_report.json
```

### JSON Report Structure

```json
{
  "timestamp": "2026-02-09T07:43:00",
  "version": "1.0.0",
  "results": {
    "seo_issues": [
      {
        "file_path": "index.html",
        "issue_type": "missing_meta_description",
        "severity": "warning",
        "message": "Missing meta description tag"
      }
    ],
    "complexity_issues": [
      {
        "file_path": "app.py",
        "issue_type": "long_function",
        "severity": "warning",
        "message": "Function 'process_data' has 85 lines",
        "line_number": 42,
        "metric_value": 85
      }
    ],
    "files_scanned": 47,
    "scan_time": 2.3
  }
}
```

---

## Contributing

Nova is open-source! We welcome contributions from the community.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Write unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## Roadmap

### Phase 1 ✅ (Current)
- [x] Basic SEO scanning
- [x] Code complexity metrics
- [x] CLI with Rich output
- [x] JSON reports

### Phase 2 🚧 (In Progress)
- [ ] Advanced complexity metrics (cyclomatic, coupling)
- [ ] Danger zone visualization
- [ ] Premium module setup

### Phase 3 📋 (Planned)
- [ ] AI assistant integration
- [ ] HTML reports
- [ ] Multi-language support enhancements

### Phase 4 🔮 (Future)
- [ ] GitHub Actions integration
- [ ] Historical trends
- [ ] Multi-project comparisons
- [ ] Browser extension

---

## License

MIT License – see [LICENSE](LICENSE) file.

Copyright (c) 2026 GalaxyBuilt

---

## Support

- **Documentation**: [https://github.com/GalaxyBuilt/nova](https://github.com/GalaxyBuilt/nova)
- **Issues**: [https://github.com/GalaxyBuilt/nova/issues](https://github.com/GalaxyBuilt/nova/issues)
- **Email**: [galaxy@txchyon.com](mailto:galaxy@txchyon.com)

---

## Badges

![PyPI version](https://img.shields.io/pypi/v/nova-scanner)
![Python versions](https://img.shields.io/pypi/pyversions/nova-scanner)
![License](https://img.shields.io/github/license/GalaxyBuilt/nova)
![Build Status](https://img.shields.io/github/actions/workflow/status/GalaxyBuilt/nova/ci.yml)
![Coverage](https://img.shields.io/codecov/c/github/GalaxyBuilt/nova)

---

## A Message from the Developer

Hey there! 👋

I'm **@GalaxyBuilt**, and I built Nova because I've been there—deep in the flow of building something amazing, shipping features, solving complex problems... and then realizing I completely forgot about SEO until it was time to promote.

As developers, we focus on making things work, making them fast, making them elegant. But SEO? That often becomes an afterthought. And when we finally remember, it's a scramble to audit everything, fix meta tags, optimize structure, and hope we didn't miss anything critical.

**Nova exists to solve that problem.**

I wanted to create a tool that fits naturally into a developer's workflow—something you can run in seconds, get clear actionable insights, and move on. No complicated dashboards, no endless configurations. Just scan, see what needs fixing, and get back to building.

Whether you're working on a side project, building for a client, or shipping a SaaS product, Nova has your back. It's the tool I wish I had on every project.

If Nova helps you ship better projects, consider following [@GalaxyBuilt](https://github.com/GalaxyBuilt) to support my work. Got questions, feedback, or just want to chat? Reach me at **galaxy@txchyon.com**—I'd love to hear from you.

Keep building amazing things. 🚀

— **GalaxyBuilt**

---

**Built with ❤️ by [@GalaxyBuilt](https://github.com/GalaxyBuilt)**
