# Contributing to RepoPulse

Thank you for your interest in contributing to RepoPulse.

RepoPulse is a Python CLI tool that scans repositories and generates clean project health reports. The goal of this project is to stay simple, useful, readable, and easy to maintain.

Contributions are welcome, whether you are fixing a bug, improving documentation, adding tests, improving checks, or suggesting new features.

---

## Project Goals

RepoPulse is built around a few clear goals:

- Help developers understand repository health quickly
- Keep the CLI simple and practical
- Generate useful terminal, Markdown, and JSON reports
- Avoid unnecessary complexity
- Keep the codebase readable for beginners and contributors
- Support clean open-source project practices

Before contributing, please keep these goals in mind.

---

## Ways to Contribute

You can contribute by:

- Fixing bugs
- Improving existing checks
- Adding new repository health checks
- Improving report formatting
- Adding tests
- Improving documentation
- Refactoring code for readability
- Suggesting useful features
- Improving CLI messages and error handling

Small improvements are welcome. You do not need to make a large change to contribute.

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/n-vim/repo-pulse.git
cd repo-pulse
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Check that the CLI works:

```bash
repopulse --help
```

---

## Running the Project Locally

Scan the current repository:

```bash
repopulse scan .
```

Generate a Markdown report:

```bash
repopulse scan . --format markdown --output REPORT.md
```

Generate a JSON report:

```bash
repopulse scan . --format json --output report.json
```

---

## Running Tests

Run the test suite:

```bash
pytest
```

Run tests with more detailed output:

```bash
pytest -v
```

Please make sure tests pass before opening a pull request.

---

## Code Quality

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

The project should stay clean, typed where useful, and easy to read.

---

## Project Structure

```text
repo-pulse/
├── src/
│   └── repopulse/
│       ├── __init__.py
│       ├── cli.py
│       ├── checks.py
│       ├── config.py
│       ├── models.py
│       ├── reports.py
│       ├── scanner.py
│       ├── scoring.py
│       └── utils.py
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```

---

## Pull Request Guidelines

Before opening a pull request:

- Make sure your change has a clear purpose
- Keep the change focused
- Add or update tests when needed
- Update documentation if behavior changes
- Run tests locally
- Run linting locally
- Avoid unrelated formatting changes
- Keep the project simple and readable

A good pull request should explain what changed and why it was needed.

---

## Commit Message Style

Use clear and simple commit messages.

Good examples:

```text
Add markdown report export tests
Fix config loading for missing YAML file
Improve README health check messages
Add repository cleanup check
```

Avoid unclear messages like:

```text
update
fix
changes
final
```

---

## Adding a New Check

Repository checks should be practical and easy to understand.

When adding a new check:

1. Add the check logic in the appropriate module.
2. Return a clear result with a useful message.
3. Add tests for both passing and failing cases.
4. Make sure the check does not produce noisy or confusing warnings.
5. Update documentation if the new check affects user-facing behavior.

A good check should help users improve their repository, not just report problems.

---

## Adding a New Report Format

If you want to add a new output format:

1. Keep the output readable.
2. Make sure it includes the score, passed checks, warnings, and suggestions.
3. Add tests for the generated output.
4. Keep formatting logic separate from scanning logic.
5. Update the README with usage examples.

---

## Documentation Guidelines

Documentation should be:

- Clear
- Practical
- Beginner-friendly
- Direct
- Free from unnecessary buzzwords
- Easy to copy and use

Avoid writing documentation that sounds generated, vague, or overly promotional.

---

## Issue Guidelines

When opening an issue, please include:

- A clear title
- What you expected to happen
- What actually happened
- Steps to reproduce the issue
- Your operating system, if relevant
- Your Python version, if relevant
- Any error message or command output

For feature requests, explain the problem first, then describe the feature.

---

## Good First Contributions

Good beginner-friendly contributions include:

- Improving README wording
- Adding tests for existing checks
- Improving CLI help text
- Improving error messages
- Adding examples to documentation
- Fixing typos
- Improving Markdown or JSON report formatting

---

## What to Avoid

Please avoid:

- Large unrelated rewrites
- Adding heavy dependencies without a strong reason
- Making the CLI complicated
- Adding checks that are too opinionated
- Committing cache files or build files
- Including secrets, tokens, or personal data
- Changing project style without discussion

RepoPulse should stay lightweight and practical.

---

## License

By contributing to RepoPulse, you agree that your contributions will be licensed under the MIT License.

---

## Thank You

Every contribution helps improve RepoPulse.

Whether you fix a typo, improve a check, add a test, or suggest a feature, your help is appreciated.
