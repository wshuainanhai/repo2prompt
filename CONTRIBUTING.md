# Contributing to repo2prompt

Thanks for your interest! This project aims to stay small, dependency-light,
and genuinely useful. Contributions are welcome.

## Getting started

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/repo2prompt.git
cd repo2prompt
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m pytest
```

## Guidelines

- Keep the dependency footprint small. New runtime dependencies need a strong
  reason.
- Add tests for new behavior under `tests/`.
- Run `python -m pytest` and make sure it passes before opening a PR.
- Follow the existing code style (PEP 8, type hints where reasonable).

## Reporting issues

Open an issue with: what you ran, the command, and the output/error. A minimal
reproduction repository helps a lot.

## Pull requests

1. Fork and create a feature branch.
2. Add tests.
3. Open a PR describing the motivation and the change.

By contributing, you agree your contributions are licensed under the MIT License.
