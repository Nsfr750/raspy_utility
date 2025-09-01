# Contributing to Raspberry Pi GPIO Control Center

Thank you for considering contributing to the Raspberry Pi GPIO Control Center! We appreciate your time and effort to help improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Commit Message Guidelines](#commit-message-guidelines)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report any unacceptable behavior to [nsfr750@yandex.com](mailto:nsfr750@yandex.com).

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/Nsfr750/raspy-utility/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/Nsfr750/raspy-utility/issues/new/choose). Be sure to include:
  - A clear and descriptive title
  - A detailed description of the behavior you're experiencing
  - Steps to reproduce the issue
  - Expected vs. actual behavior
  - Screenshots or screen recordings if applicable
  - Your operating system and Python version

### Suggesting Enhancements

- Use GitHub Issues to submit enhancement suggestions
- Clearly describe the feature/enhancement and why it would be useful
- Include any relevant code or mockups if applicable
- Consider whether your enhancement would be better as a separate project or plugin

### Pull Requests

1. Fork the repository and create your branch from `main`
2. Install the development dependencies: `pip install -r requirements-dev.txt`
3. Make your changes, following the code style guidelines
4. Add tests for your changes if applicable
5. Ensure all tests pass
6. Update the documentation as needed
7. Submit a pull request with a clear description of your changes

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) A Raspberry Pi for hardware testing

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/raspy-utility.git
   cd raspy-utility
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\\venv\\Scripts\\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # For development:
   pip install -r requirements-dev.txt
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_module.py

# Run with coverage report
pytest --cov=raspy_utility tests/
```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use type hints for all functions and methods
- Document all public APIs with docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep lines under 100 characters when possible
- Use `black` for code formatting (included in development dependencies)

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `perf:` A code change that improves performance
- `test:` Adding missing or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools and libraries

Example commit message:
```
feat: add dark mode support

- Add theme switching functionality
- Update UI components for dark theme
- Add theme preference to user settings

Closes #123
```

## License

By contributing, you agree that your contributions will be licensed under the [GNU General Public License v3.0](LICENSE).
