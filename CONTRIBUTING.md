# Contributing to AurantisSync

Thank you for your interest in contributing to AurantisSync! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/JoaoSantosCodes/AurantisSync/issues)
2. If not, create a new issue using the [Bug Report template](https://github.com/JoaoSantosCodes/AurantisSync/issues/new?template=bug_report.md)
3. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature is already requested in [Issues](https://github.com/JoaoSantosCodes/AurantisSync/issues)
2. If not, create a new issue using the [Feature Request template](https://github.com/JoaoSantosCodes/AurantisSync/issues/new?template=feature_request.md)
3. Describe:
   - What you want to achieve
   - Why it would be useful
   - How it should work

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test your changes: `python test_mvp.py`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to your branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- Git
- FFmpeg

### Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AurantisSync.git
   cd AurantisSync
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Test the setup:
   ```bash
   python test_mvp.py
   ```

### Development Environment

We recommend using VS Code with the following extensions:
- Python
- Pylance
- Black Formatter
- Flake8
- MyPy Type Checker

## 📝 Code Style

### Python Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused

### Example

```python
def export_srt(lines: List[Line], path: str) -> None:
    """
    Exporta para formato SRT (legendas).
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            # Implementation here
            pass
    except Exception as e:
        raise ExportError(f"Erro ao exportar SRT: {e}")
```

### Formatting

We use Black for code formatting:

```bash
black aurantis_sync_mvp.py
```

### Linting

We use Flake8 for linting:

```bash
flake8 aurantis_sync_mvp.py
```

## 🧪 Testing

### Running Tests

```bash
python test_mvp.py
```

### Writing Tests

When adding new features, please add tests:

```python
def test_export_srt():
    """Test SRT export functionality."""
    lines = [
        Line(start=0.0, end=5.0, text="Hello world"),
        Line(start=5.0, end=10.0, text="This is a test")
    ]
    
    # Test implementation
    assert True  # Replace with actual test
```

## 📚 Documentation

### Code Documentation

- Write clear docstrings for all functions and classes
- Use type hints
- Add comments for complex logic

### User Documentation

- Update README.md for new features
- Add examples to QUICKSTART.md
- Update CHANGELOG.md for releases

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes**: Run `python test_mvp.py`
2. **Check code style**: Run `black` and `flake8`
3. **Update documentation**: Update relevant docs
4. **Add tests**: Include tests for new features

### PR Template

Use the provided [Pull Request template](.github/pull_request_template.md) when creating PRs.

### Review Process

1. All PRs require review
2. Address feedback promptly
3. Keep PRs focused and small
4. Update documentation as needed

## 🏷️ Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Test on multiple platforms
- [ ] Create release tag
- [ ] Build and test executable

## 🐛 Bug Fixes

### Priority Levels

1. **Critical**: Security vulnerabilities, data loss
2. **High**: App crashes, major functionality broken
3. **Medium**: Minor bugs, UI issues
4. **Low**: Cosmetic issues, documentation

### Fixing Bugs

1. Reproduce the bug
2. Write a test that fails
3. Fix the bug
4. Ensure the test passes
5. Update documentation if needed

## 🎯 Feature Development

### Feature Planning

1. Create an issue for discussion
2. Get approval before starting work
3. Break large features into smaller PRs
4. Consider backward compatibility

### Implementation

1. Start with tests
2. Implement the feature
3. Update documentation
4. Add examples
5. Test thoroughly

## 📞 Communication

### Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code review, implementation discussion

### Guidelines

- Be respectful and constructive
- Use clear, descriptive titles
- Provide context and examples
- Respond to feedback promptly

## 📄 License

By contributing to AurantisSync, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md
- CHANGELOG.md
- Release notes

Thank you for contributing to AurantisSync! 🎉
