# Contributing

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Basic understanding of CSV data analysis

### Quick Setup

See [Developer Guide](docs/developer-guide.md#setup) for detailed setup instructions.

## Contribution Guidelines

### Types of Contributions

- Bug fixes
- Feature additions
- Performance improvements
- Documentation updates

### Workflow

1. Fork the repository
2. Create feature branch from `master`
3. Make changes following project standards
4. Run tests: `pytest`
5. Run code quality checks: `pre-commit run --all-files`
6. Submit pull request using [Pull Request Template](.github/pull_request_template.md)

### Commit Messages

Use conventional commit format:
```
type(scope): description

Examples:
feat(stats): add correlation analysis
fix(cli): handle missing file error
docs(api): update analyze function
```

## Development Standards

### Code Quality

All contributions must pass:
- Black code formatting
- isort import sorting
- MyPy type checking
- flake8 linting
- Pre-commit hooks

See [Developer Guide](docs/developer-guide.md#code-quality) for detailed commands.

### Testing

- All tests must pass: `pytest`
- Add tests for new functionality
- Maintain or improve code coverage

## Community Standards

- Professional tone in all communications
- Respectful interaction with maintainers and contributors
- Follow project coding standards and conventions
- Provide clear descriptions in issues and pull requests

## Issue Reporting

Use the appropriate GitHub issue template:
- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) - Report bugs and issues
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) - Suggest new features

## Resources

### Documentation
- [Documentation Index](docs/index.md) - Complete documentation overview
- [Developer Guide](docs/developer-guide.md) - Development workflow and architecture
- [User Guide](docs/user-guide.md) - Installation and usage
- [API Reference](docs/api-reference.md) - Python API documentation
- [Configuration](docs/configuration.md) - Settings and environment variables
- [Troubleshooting](docs/troubleshooting.md) - Problem-solving guide
- [Architecture Diagrams](docs/diagrams.md) - Visual system architecture

### Templates
- [Pull Request Template](.github/pull_request_template.md) - PR submission guide
- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) - Report bugs and issues
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) - Suggest new features


---

Version: 2.0.0 | Status: Beta | Python: 3.8-3.13

Copyright 2025 dhaneshbb | License: MIT | Homepage: https://github.com/dhaneshbb/autocsv-profiler
