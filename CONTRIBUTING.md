# Contributing to AI Terminal Client

Thank you for your interest in contributing to AI Terminal Client! This document provides comprehensive guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Be respectful, inclusive, and constructive. Harassment and abusive behavior are not tolerated.

## 🚀 Getting Started
- Fork the repo and clone your fork
- Create a virtual environment and install dependencies
- Run basic tests: `python test_basic.py`
- Configure pre-commit hooks (optional): `pre-commit install`

## 📋 Development Guidelines
- Follow PEP 8, use Black for formatting, Flake8 for linting
- Write docstrings and type hints
- Handle errors gracefully and validate inputs
- Keep functions small and focused

## 🧪 Testing
- Add unit tests for new features
- Test error paths and edge cases
- Mock external API calls in future test suite

## 📚 Documentation
- Update README.md for new user-facing features
- Update INSTALLATION.md for dependency changes
- Add usage examples where helpful

## 🔄 Pull Request Process
1. Create an issue or reference an existing one
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes with clear messages
4. Run formatters/linters/tests
5. Push branch and open a PR with a descriptive template

## 🏗️ Adding New AI Providers
- Add key pattern to `APIKeyDetector.PATTERNS`
- Implement `_provider_request` method in `AIClient`
- Add to `send_message` switch
- Update docs and tests

## 🔐 Security
- Never log API keys
- Do not include secrets in code or commits
- Store keys only in the local config file

## 🧭 Governance & Recognition
- Maintainers review PRs for quality, tests, docs, and safety
- Contributors are acknowledged in release notes

---

For full guidelines, architecture notes, and templates, see the extended version in the repository history or open a discussion to propose changes.
