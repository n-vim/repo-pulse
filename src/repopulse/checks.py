"""Built-in repository health checks."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, List

from repopulse.config import RepoPulseConfig
from repopulse.models import CheckDefinition, CheckResult, CheckStatus, RepositoryProfile
from repopulse.utils import (
    CHANGELOG_NAMES,
    CONTRIBUTING_NAMES,
    LICENSE_NAMES,
    README_NAMES,
    SECURITY_NAMES,
    find_secret_like_files,
    has_any_file,
    has_any_path,
    iter_repository_files,
    read_text_safely,
)

CheckFunction = Callable[[Path, RepositoryProfile, RepoPulseConfig], CheckResult]


CHECK_DEFINITIONS = [
    CheckDefinition("readme", "README quality", "Documentation", 15, "Checks README presence and useful content length."),
    CheckDefinition("license", "License", "Open Source", 10, "Checks whether a license file exists."),
    CheckDefinition("gitignore", "Git ignore rules", "Repository", 8, "Checks whether .gitignore exists."),
    CheckDefinition("tests", "Tests", "Quality", 12, "Checks whether a test structure exists."),
    CheckDefinition("packaging", "Project packaging", "Build", 10, "Checks whether common packaging files are present."),
    CheckDefinition("source-layout", "Source layout", "Structure", 8, "Checks whether source code is organized clearly."),
    CheckDefinition("ci", "Continuous integration", "Automation", 8, "Checks whether GitHub Actions or other CI config exists."),
    CheckDefinition("docs", "Documentation folder", "Documentation", 6, "Checks whether extra documentation exists."),
    CheckDefinition("changelog", "Changelog", "Release", 5, "Checks whether release history documentation exists."),
    CheckDefinition("contributing", "Contributing guide", "Community", 5, "Checks whether contribution instructions exist."),
    CheckDefinition("security", "Security policy", "Security", 5, "Checks whether SECURITY.md exists."),
    CheckDefinition("dependencies", "Dependency files", "Build", 5, "Checks whether dependency files are present."),
    CheckDefinition("docker", "Docker support", "Deployment", 3, "Checks whether Docker files exist."),
    CheckDefinition("secrets", "Secret file safety", "Security", 10, "Looks for common secret-like files."),
]


def _result(
    code: str,
    status: CheckStatus,
    points: int,
    message: str,
    recommendation: str | None = None,
    **details: object,
) -> CheckResult:
    definition = next(item for item in CHECK_DEFINITIONS if item.code == code)
    return CheckResult(
        code=definition.code,
        name=definition.name,
        category=definition.category,
        status=status,
        points=max(0, min(points, definition.max_points)),
        max_points=definition.max_points,
        message=message,
        recommendation=recommendation,
        details=details,
    )


def check_readme(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    readme = has_any_file(root, README_NAMES)
    if not readme:
        return _result(
            "readme",
            CheckStatus.FAIL,
            0,
            "README file is missing.",
            "Add a clear README with overview, installation, usage, features, and license information.",
        )

    content = read_text_safely(readme)
    length = len(content.strip())
    headings = content.count("#")
    has_usage = "usage" in content.lower() or "quick start" in content.lower()

    if length >= config.min_readme_chars and headings >= 3 and has_usage:
        return _result(
            "readme",
            CheckStatus.PASS,
            15,
            f"{readme.name} is present and detailed.",
            None,
            file=readme.name,
            characters=length,
        )

    return _result(
        "readme",
        CheckStatus.WARN,
        8,
        f"{readme.name} exists but could be more useful.",
        "Improve the README with clearer sections for overview, installation, usage, examples, and contribution notes.",
        file=readme.name,
        characters=length,
        headings=headings,
    )


def check_license(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    license_file = has_any_file(root, LICENSE_NAMES)
    if license_file:
        return _result("license", CheckStatus.PASS, 10, f"License file found: {license_file.name}.", file=license_file.name)
    return _result(
        "license",
        CheckStatus.FAIL,
        0,
        "No license file found.",
        "Add a LICENSE file so users know how they can use the project.",
    )


def check_gitignore(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    gitignore = root / ".gitignore"
    if gitignore.is_file():
        content = read_text_safely(gitignore).lower()
        useful_patterns = ["__pycache__", ".venv", "dist", "build", ".env"]
        found = [pattern for pattern in useful_patterns if pattern in content]
        if len(found) >= 3:
            return _result("gitignore", CheckStatus.PASS, 8, ".gitignore is present with useful rules.", patterns=found)
        return _result(
            "gitignore",
            CheckStatus.WARN,
            4,
            ".gitignore exists but looks minimal.",
            "Add common Python, environment, build, and editor ignore patterns.",
            patterns=found,
        )
    return _result(
        "gitignore",
        CheckStatus.FAIL,
        0,
        ".gitignore is missing.",
        "Add a .gitignore file to avoid committing cache, virtualenv, build, and local files.",
    )


def check_tests(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        test_files = list(tests_dir.rglob("test_*.py")) + list(tests_dir.rglob("*_test.py"))
        if test_files:
            return _result("tests", CheckStatus.PASS, 12, f"Tests found in tests directory ({len(test_files)} files).", files=len(test_files))
        return _result(
            "tests",
            CheckStatus.WARN,
            6,
            "tests directory exists but no Python test files were found.",
            "Add test files such as tests/test_scanner.py or tests/test_cli.py.",
        )
    return _result(
        "tests",
        CheckStatus.FAIL,
        0,
        "No tests directory found.",
        "Add a tests directory with at least a few basic tests.",
    )


def check_packaging(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    files = ["pyproject.toml", "setup.cfg", "setup.py", "package.json", "Cargo.toml", "go.mod"]
    found = has_any_file(root, files)
    if found:
        return _result("packaging", CheckStatus.PASS, 10, f"Project packaging file found: {found.name}.", file=found.name)
    return _result(
        "packaging",
        CheckStatus.WARN,
        3,
        "No common project packaging file found.",
        "Add pyproject.toml for Python projects or the equivalent package file for your stack.",
    )


def check_source_layout(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    if (root / "src").is_dir():
        source_files = list((root / "src").rglob("*.py"))
        if source_files:
            return _result("source-layout", CheckStatus.PASS, 8, "src layout found with Python source files.", files=len(source_files))
        return _result("source-layout", CheckStatus.WARN, 5, "src directory exists but contains no Python files.")

    python_files = [path for path in root.glob("*.py") if path.name != "setup.py"]
    if python_files:
        return _result(
            "source-layout",
            CheckStatus.WARN,
            5,
            "Python files found at repository root.",
            "For larger projects, consider using a src/ package layout.",
            files=[path.name for path in python_files],
        )

    return _result(
        "source-layout",
        CheckStatus.WARN,
        2,
        "No clear source code layout detected.",
        "Add source code under src/ or a clearly named application package.",
    )


def check_ci(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    ci_paths = [
        root / ".github" / "workflows",
        root / ".gitlab-ci.yml",
        root / ".circleci",
        root / "azure-pipelines.yml",
    ]
    if any(path.exists() for path in ci_paths):
        return _result("ci", CheckStatus.PASS, 8, "CI configuration found.")
    return _result(
        "ci",
        CheckStatus.WARN,
        2,
        "No CI configuration found.",
        "Add a GitHub Actions workflow to run tests and linting automatically.",
    )


def check_docs(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    docs = has_any_path(root, ["docs", "documentation"])
    if docs and docs.is_dir():
        return _result("docs", CheckStatus.PASS, 6, f"Documentation directory found: {docs.name}.", directory=docs.name)
    return _result(
        "docs",
        CheckStatus.WARN,
        2,
        "No docs directory found.",
        "Add a docs directory when the project needs guides, examples, or architecture notes.",
    )


def check_changelog(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    changelog = has_any_file(root, CHANGELOG_NAMES)
    if changelog:
        return _result("changelog", CheckStatus.PASS, 5, f"Changelog found: {changelog.name}.", file=changelog.name)
    return _result(
        "changelog",
        CheckStatus.WARN,
        1,
        "No changelog found.",
        "Add CHANGELOG.md before publishing releases.",
    )


def check_contributing(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    contributing = has_any_file(root, CONTRIBUTING_NAMES)
    if contributing:
        return _result("contributing", CheckStatus.PASS, 5, f"Contributing guide found: {contributing.name}.", file=contributing.name)
    return _result(
        "contributing",
        CheckStatus.WARN,
        1,
        "No contributing guide found.",
        "Add CONTRIBUTING.md to explain setup, tests, and pull request expectations.",
    )


def check_security(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    security = has_any_file(root, SECURITY_NAMES)
    if security:
        return _result("security", CheckStatus.PASS, 5, f"Security policy found: {security.name}.", file=security.name)
    return _result(
        "security",
        CheckStatus.WARN,
        1,
        "No security policy found.",
        "Add SECURITY.md to explain how vulnerabilities should be reported.",
    )


def check_dependencies(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    dependency_files = [
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "poetry.lock",
        "uv.lock",
        "Pipfile",
        "package.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "package-lock.json",
    ]
    found = [name for name in dependency_files if (root / name).is_file()]
    if found:
        return _result("dependencies", CheckStatus.PASS, 5, "Dependency files found.", files=found)
    return _result(
        "dependencies",
        CheckStatus.WARN,
        1,
        "No dependency file found.",
        "Add dependency metadata such as pyproject.toml or requirements.txt.",
    )


def check_docker(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    dockerfile = root / "Dockerfile"
    compose = root / "docker-compose.yml"
    if dockerfile.is_file() or compose.is_file():
        return _result("docker", CheckStatus.PASS, 3, "Docker support found.")
    return _result(
        "docker",
        CheckStatus.WARN,
        1,
        "No Docker files found.",
        "Add Dockerfile only if containerized development or deployment is useful for this project.",
    )


def check_secrets(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> CheckResult:
    matches = find_secret_like_files(root, config.ignore)
    if not matches:
        return _result("secrets", CheckStatus.PASS, 10, "No common secret-like files found.")
    return _result(
        "secrets",
        CheckStatus.FAIL,
        0,
        "Potential secret-like files found.",
        "Remove secret files from the repository and rotate any exposed credentials.",
        files=matches,
    )


CHECKS: List[CheckFunction] = [
    check_readme,
    check_license,
    check_gitignore,
    check_tests,
    check_packaging,
    check_source_layout,
    check_ci,
    check_docs,
    check_changelog,
    check_contributing,
    check_security,
    check_dependencies,
    check_docker,
    check_secrets,
]


def run_checks(root: Path, profile: RepositoryProfile, config: RepoPulseConfig) -> List[CheckResult]:
    """Run all built-in checks against a repository."""

    return [check(root, profile, config) for check in CHECKS]


def list_check_definitions() -> List[CheckDefinition]:
    """Return metadata for all built-in checks."""

    return list(CHECK_DEFINITIONS)
