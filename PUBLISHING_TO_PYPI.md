# Publishing Nova to PyPI

**Good news!** Your project is already configured for PyPI. Publishing is straightforward!

## Prerequisites

✅ You already have:
- `pyproject.toml` configured
- Package structure set up correctly
- README.md with comprehensive documentation
- MIT License

## Step-by-Step Guide

### 1. Create PyPI Account

1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create your account
3. Verify your email

### 2. Create API Token (Recommended)

Instead of using your password, use an API token for security:

1. Log into PyPI
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name it (e.g., "nova-scanner")
5. Scope: "Entire account" (or specific to nova-scanner after first upload)
6. **Save the token** - you'll only see it once!

### 3. Install Build Tools

```bash
# Activate your virtual environment first
.\venv\Scripts\activate

# Install build and upload tools
pip install build twine
```

### 4. Build Your Package

```bash
# Clean old builds (if any)
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build the package
python -m build
```

This creates two files in the `dist/` folder:
- `nova-scanner-1.0.0.tar.gz` (source distribution)
- `nova_scanner-1.0.0-py3-none-any.whl` (wheel distribution)

### 5. Test on TestPyPI (Optional but Recommended)

TestPyPI is a separate instance for testing:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ nova-scanner
```

### 6. Upload to Real PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

You'll be prompted for:
- **Username**: `__token__`
- **Password**: Your API token (including the `pyp-` prefix)

### 7. Verify Installation

```bash
# Install from PyPI
pip install nova-scanner

# Test it works
nova --help
```

## Configuration for API Token (Optional)

Create a `~/.pypirc` file to avoid entering credentials each time:

```ini
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-test-api-token-here
```

**Important**: Keep this file secure! Add it to `.gitignore` if in a project folder.

## Updating Your Package

When you release a new version:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"  # or 1.1.0, 2.0.0, etc.
   ```

2. **Rebuild and upload**:
   ```bash
   Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
   python -m build
   twine upload dist/*
   ```

## Version Numbering (Semantic Versioning)

- **1.0.0** → **1.0.1**: Bug fixes, small patches
- **1.0.0** → **1.1.0**: New features, backward compatible
- **1.0.0** → **2.0.0**: Breaking changes

## Pre-Release Checklist

Before publishing, verify:

- [ ] All tests pass (`pytest`)
- [ ] README is up to date
- [ ] Version number is correct in `pyproject.toml`
- [ ] LICENSE file exists
- [ ] `.gitignore` excludes `dist/`, `build/`, `*.egg-info`
- [ ] All dependencies are listed correctly
- [ ] Package installs locally: `pip install -e .`
- [ ] CLI works: `nova --help`

## Common Issues

### Issue: "File already exists"
**Solution**: You can't re-upload the same version. Increment the version number.

### Issue: "Invalid distribution"
**Solution**: Make sure you have `__init__.py` files in all package directories.

### Issue: "Module not found" after install
**Solution**: Check that `[project.scripts]` in `pyproject.toml` points to the correct module.

## What Happens After Publishing?

1. **Package is live** at `https://pypi.org/project/nova-scanner/`
2. **Anyone can install** with `pip install nova-scanner`
3. **PyPI shows your README** as the project description
4. **Download stats** are tracked automatically

## Badges for README

After publishing, update your README badges:

```markdown
![PyPI version](https://img.shields.io/pypi/v/nova-scanner)
![Python versions](https://img.shields.io/pypi/pyversions/nova-scanner)
![Downloads](https://img.shields.io/pypi/dm/nova-scanner)
![License](https://img.shields.io/pypi/l/nova-scanner)
```

## Resources

- [PyPI Official Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)

---

**That's it!** Publishing to PyPI is straightforward. Your package is already well-configured. 🚀
