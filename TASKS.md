# Nova - Code + SEO Health Scanner - Development Tasks

## Planning & Setup
- [x] Create project documentation (README, TASKS, IMPLEMENTATION_PLAN)
- [x] Define project structure and architecture
- [x] Review and approve implementation plan
- [ ] Set up GitHub repository

## Phase 1 – Freemium CLI & Basic SEO/Complexity Scanner
- [x] Project initialization and folder structure
  - [x] Create Nova project directory
  - [x] Set up virtual environment
  - [ ] Initialize git repository
  - [x] Create basic folder structure (nova_freemium, nova_premium, nova_shared)
- [x] Core shared utilities
  - [x] Implement `nova_shared/utils.py` (file operations, path handling)
  - [x] Implement `nova_shared/language_detection.py` (file type detection)
- [x] Freemium scanner module
  - [x] Create `nova_freemium/scanner.py` (file scanning, SEO checks, complexity metrics)
  - [x] Implement basic SEO detection (title, meta description, canonical, OG tags)
  - [x] Implement basic complexity metrics (function length, file length, nested loops)
- [x] Scoring system
  - [x] Create `nova_freemium/scoring.py` (SEO and complexity score calculation)
  - [x] Implement 0-100 scoring algorithms
- [x] CLI interface
  - [x] Create `nova_freemium/cli.py` (main CLI entry point)
  - [x] Implement `nova scan <folder>` command
  - [x] Add `--json` export option
  - [x] Integrate Rich library for color-coded output
- [x] Report generation
  - [x] Create `nova_freemium/report.py` (JSON export functionality)
- [ ] Testing Phase 1
  - [ ] Test scanner on sample projects
  - [ ] Verify JSON output format
  - [ ] Test CLI commands and options

## Phase 2 – Complexity Radar Enhancements
- [ ] Advanced complexity metrics
  - [ ] Implement cyclomatic complexity calculation
  - [ ] Add coupling detection between files
  - [ ] Implement churn detection (high edits/lines ratio)
- [ ] Update scoring system
  - [ ] Enhance complexity score formulas with new metrics
  - [ ] Add weighting for different complexity factors
- [ ] CLI visualization improvements
  - [ ] Add color-coded terminal tables for danger zones
  - [ ] Implement visual indicators for high-risk areas
- [ ] Testing Phase 2
  - [ ] Validate advanced metrics accuracy
  - [ ] Test danger zone highlighting

## Phase 3 – Premium Module Setup & Gating
- [ ] Premium module structure
  - [ ] Create `nova_premium/` directory
  - [ ] Implement `nova_premium/__init__.py` with license checking
  - [ ] Create `nova_premium/advanced_scanner.py`
  - [ ] Create `nova_premium/integrations.py`
- [ ] License/API key system
  - [ ] Implement `license_check(key)` function
  - [ ] Add environment variable support for API keys
  - [ ] Create premium feature gating mechanism
- [ ] Advanced SEO checks (premium)
  - [ ] Duplicate meta tags detection
  - [ ] Broken links checker
  - [ ] sitemap.xml validation
  - [ ] robots.txt validation
  - [ ] Structured data detection
- [ ] CLI premium options
  - [ ] Add `--html` flag (premium)
  - [ ] Add `--ai` flag (premium)
  - [ ] Implement friendly upgrade messages for freemium users
- [ ] Testing Phase 3
  - [ ] Test license validation
  - [ ] Verify premium feature gating
  - [ ] Test advanced SEO checks

## Phase 4 – AI Assistant Integration
- [ ] AI assistant module
  - [ ] Create `nova_premium/ai_assistant.py`
  - [ ] Implement OpenAI/Claude API integration
  - [ ] Create context preparation for AI requests
- [ ] AI-powered suggestions
  - [ ] SEO fix suggestions
  - [ ] Code improvement recommendations
  - [ ] Auto-fix functionality with user confirmation
- [ ] CLI integration
  - [ ] Implement `nova scan <folder> --ai` command
  - [ ] Add interactive prompts for AI suggestions
  - [ ] Update reports to include AI recommendations
- [ ] Testing Phase 4
  - [ ] Test AI API integration
  - [ ] Validate suggestion quality
  - [ ] Test auto-fix functionality

## Phase 5 – HTML Reports & Visualization
- [ ] HTML report generation
  - [ ] Create `nova_premium/html_report.py`
  - [ ] Design HTML template with color-coded highlights
  - [ ] Implement overview page with all scores
  - [ ] Add SEO issues visualization
  - [ ] Add complexity danger zones visualization
- [ ] CLI integration
  - [ ] Implement `--html` output option
  - [ ] Add HTML file export functionality
- [ ] Testing Phase 5
  - [ ] Test HTML report generation
  - [ ] Verify visual presentation
  - [ ] Test on different browsers

## Phase 6 – Multi-language Support & Extensibility
- [ ] Language detection enhancements
  - [ ] Expand `language_detection.py` for Python, JS, TS, JSX, TSX
  - [ ] Add React and Next.js project detection
  - [ ] Implement framework-specific checks
- [ ] File type-specific analysis
  - [ ] Apply appropriate checks per file type
  - [ ] Update both freemium and premium scanners
- [ ] Plugin system design
  - [ ] Create plugin architecture
  - [ ] Allow custom rules and file types
  - [ ] Document plugin API
- [ ] Testing Phase 6
  - [ ] Test multi-language projects
  - [ ] Validate framework detection
  - [ ] Test plugin system

## Phase 7 – PyPI Packaging & Distribution
- [ ] Package configuration
  - [ ] Create `setup.py` or `pyproject.toml`
  - [ ] Define dependencies (freemium vs premium)
  - [ ] Configure entry points for CLI
  - [ ] Add package metadata
- [ ] Documentation
  - [ ] Create comprehensive README.md
  - [ ] Add installation instructions
  - [ ] Document freemium vs premium features
  - [ ] Add usage examples
  - [ ] Create badges for SEO/Complexity scores
- [ ] PyPI preparation
  - [ ] Test package installation locally
  - [ ] Create distribution files
  - [ ] Prepare for PyPI upload
- [ ] GitHub repository setup
  - [ ] Push to https://github.com/GalaxyBuilt/nova
  - [ ] Configure git with username and email
  - [ ] Add LICENSE file
  - [ ] Add CONTRIBUTING.md
  - [ ] Set up GitHub Actions for CI

## Phase 8 – Optional Enhancements
- [ ] CI/CD integration
  - [ ] Create GitHub Actions workflow for PR scanning
  - [ ] Add automated testing
- [ ] External API integrations
  - [ ] Google PageSpeed Insights integration
  - [ ] Ahrefs API integration (optional)
  - [ ] SEMrush API integration (optional)
- [ ] Advanced features
  - [ ] Historical trends tracking
  - [ ] Multi-project comparison reports
  - [ ] First-run interactive setup wizard
- [ ] Performance optimization
  - [ ] Optimize scanning speed
  - [ ] Add caching mechanisms
  - [ ] Implement parallel processing

## Git & Deployment
- [ ] Initialize git repository
- [ ] Configure git user (galaxybuilt, exoticdevlabs@gmail.com)
- [ ] Create .gitignore file
- [ ] Initial commit
- [ ] Push to GitHub remote
- [ ] Set up branch protection rules
