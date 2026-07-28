<div align="center">

# RepoPulse

**A Python CLI that scans repositories and generates clean project health reports.**

RepoPulse helps developers review a project folder, find missing repository essentials, and generate readable health reports in the terminal, Markdown, or JSON.

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Typer-0E7C86?style=flat)
![Terminal](https://img.shields.io/badge/Terminal-Rich-4B8BBE?style=flat)
![Config](https://img.shields.io/badge/Config-YAML-yellow?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## Overview

RepoPulse is a command-line repository health checker built with Python.

It scans a project folder and checks whether the repository has the important files, structure, documentation, and configuration that make a project look clean, maintainable, and ready for GitHub.

It is useful when starting a new project, reviewing an existing repository, preparing a project for open source, or improving the overall quality of a GitHub repo.

---

## Why RepoPulse?

A good repository is more than just source code.

A professional project usually needs:

- A clear README
- A license
- A clean folder structure
- Tests
- Dependency files
- CI workflow
- Security notes
- Contribution guidelines
- Useful documentation
- No obvious secrets or junk files

RepoPulse checks these things and gives you a simple report with a score, passed checks, warnings, and suggestions.

---

## Features

- Scan any local project folder
- Generate a repository health score
- Detect important missing files
- Check README, license, tests, docs, CI, security, and packaging setup
- Show clean terminal output using Rich
- Export reports as Markdown
- Export reports as JSON
- Support project configuration through `.repopulse.yaml`
- Works offline on local repositories
- Simple CLI powered by Typer
- Useful for Python projects and general GitHub repositories

---

## What RepoPulse Checks

RepoPulse can inspect a repository for common quality signals, including:

| Area | What it checks |
| --- | --- |
| Documentation | README, docs folder, useful project information |
| Licensing | License file availability |
| Testing | Test folder or test files |
| Packaging | Python package metadata and dependency files |
| GitHub setup | GitHub Actions workflow and repository files |
| Security | Security policy and possible secret files |
| Contribution | Contributing guide and project guidelines |
| Cleanliness | Cache files, build folders, and unnecessary junk |
| Structure | Source folders, config files, and maintainable layout |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/n-vim/repo-pulse.git
cd repo-pulse
```

Install it locally:

```bash
python -m pip install -e .
```

For development setup:

```bash
python -m pip install -e ".[dev]"
```

Check that the CLI is working:

```bash
repopulse --help
```

You can also use:

```bash
repo-pulse --help
```

---

## Quick Start

Scan the current repository:

```bash
repopulse scan .
```

Scan another project folder:

```bash
repopulse scan ../my-project
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

## Example Terminal Output

```text
RepoPulse Report

Project: repo-pulse
Score: 86/100
Status: Good

Passed
- README.md found
- LICENSE found
- pyproject.toml found
- tests folder found
- GitHub Actions workflow found

Warnings
- SECURITY.md is missing
- CONTRIBUTING.md is missing
- docs folder is missing

Suggestions
- Add a security policy for responsible disclosure
- Add contributing guidelines for open-source contributors
- Add more documentation for advanced usage
```

---

## Commands

| Command | Description |
| --- | --- |
| `repopulse scan .` | Scan the current repository |
| `repopulse scan path/to/project` | Scan a specific project folder |
| `repopulse scan . --format markdown` | Print a Markdown report |
| `repopulse scan . --format json` | Print a JSON report |
| `repopulse scan . --output REPORT.md` | Save the report to a file |
| `repopulse init` | Create a default `.repopulse.yaml` config file |
| `repopulse --help` | Show CLI help |

---

## Report Formats

RepoPulse supports multiple output formats.

### Terminal

Best for quick local checks:

```bash
repopulse scan .
```

### Markdown

Best for saving a readable project report:

```bash
repopulse scan . --format markdown --output REPORT.md
```

### JSON

Best for automation or integration with other tools:

```bash
repopulse scan . --format json --output report.json
```

---

## Configuration

RepoPulse can use a `.repopulse.yaml` file to customize how a repository is checked.

Create a config file:

```bash
repopulse init
```

Example configuration:

```yaml
ignore:
  - .venv
  - __pycache__
  - .pytest_cache
  - dist
  - build

score:
  fail_below: 60
  warn_below: 80

checks:
  readme: true
  license: true
  tests: true
  ci: true
  security: true
  contributing: true
  packaging: true
  docs: true
```

This allows you to keep project checks consistent across repositories.

---

## Scoring

RepoPulse gives every scanned repository a score out of 100.

The score is based on important project-quality checks such as documentation, licensing, tests, packaging, CI, and maintainability.

A simple way to understand the score:

| Score | Meaning |
| --- | --- |
| `90 - 100` | Excellent repository health |
| `75 - 89` | Good project with minor improvements needed |
| `60 - 74` | Usable project but missing important items |
| `0 - 59` | Needs cleanup before it looks production-ready |

The score is not meant to be strict or perfect. It is a practical signal that helps you quickly see what can be improved.

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
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```

---

## Built With

| Tool | Purpose |
| --- | --- |
| Python | Main programming language |
| Typer | Command-line interface |
| Rich | Terminal formatting |
| PyYAML | YAML configuration support |
| Pytest | Testing |
| Ruff | Linting |
| Mypy | Type checking |
| Hatchling | Python package build backend |

---

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

---

## Example Workflow

A common workflow looks like this:

```bash
git clone https://github.com/n-vim/repo-pulse.git
cd repo-pulse
python -m pip install -e ".[dev]"
pytest
repopulse scan .
```

To create a shareable health report:

```bash
repopulse scan . --format markdown --output REPORT.md
```

---

## Good Use Cases

RepoPulse is useful for:

- Reviewing your own GitHub repositories
- Improving open-source project quality
- Checking projects before publishing them
- Auditing generated starter projects
- Creating repository health reports
- Finding missing files quickly
- Teaching beginners what a clean repository needs
- Keeping multiple projects consistent

---

## Roadmap

Planned improvements:

- More advanced README quality checks
- GitHub URL scanning
- Badge and metadata inspection
- Dependency risk hints
- Custom scoring profiles
- Ignore rules per check
- HTML report output
- Repository comparison mode
- GitHub Action integration
- More language-specific checks

---

## Contributing

Contributions are welcome.

You can contribute by:

- Improving checks
- Adding new report formats
- Fixing bugs
- Improving documentation
- Adding tests
- Suggesting new repository-quality rules

Before contributing, please keep the project simple, readable, and useful.

---

## Repository Description

Recommended GitHub description:

```text
A Python CLI that scans repositories and generates clean project health reports.
```

Recommended topics:

```text
python, cli, typer, repository, health-check, developer-tools, automation, code-quality, github
```

---

## Author

Created by **Nitish Vimal**.

GitHub: [n-vim](https://github.com/n-vim)

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**RepoPulse helps you understand, improve, and maintain cleaner repositories.**

</div>
