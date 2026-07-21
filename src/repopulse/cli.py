"""Command-line interface for RepoPulse."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from repopulse import __version__
from repopulse.checks import list_check_definitions
from repopulse.config import write_default_config
from repopulse.reports import render_terminal, to_json, to_markdown, write_report
from repopulse.scanner import ScanError, scan_repository

app = typer.Typer(
    name="repopulse",
    help="Scan repositories and generate clean project health reports.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def scan(
    path: Path = typer.Argument(Path("."), help="Repository path to scan."),
    format: str = typer.Option(
        "terminal",
        "--format",
        "-f",
        help="Report format: terminal, markdown, or json.",
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Write report to a file."),
    fail_under: Optional[int] = typer.Option(
        None,
        "--fail-under",
        help="Exit with status 1 when the score is below this value.",
    ),
) -> None:
    """Scan a repository and show a health report."""

    fmt = format.lower().strip()
    if fmt not in {"terminal", "markdown", "json"}:
        raise typer.BadParameter("format must be one of: terminal, markdown, json")

    try:
        report = scan_repository(path)
    except ScanError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if output:
        if fmt == "terminal":
            fmt = "markdown"
        write_report(report, str(output), fmt)
        console.print(f"[green]Report written:[/green] {output}")
    elif fmt == "markdown":
        console.print(to_markdown(report))
    elif fmt == "json":
        console.print(to_json(report))
    else:
        render_terminal(report, console)

    threshold = fail_under
    if threshold is not None and report.score < threshold:
        console.print(f"[red]Score {report.score}/100 is below required threshold {threshold}.[/red]")
        raise typer.Exit(code=1)


@app.command("checks")
def checks_command() -> None:
    """List all built-in repository checks."""

    table = Table(show_header=True, header_style="bold")
    table.add_column("Code")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Points", justify="right")
    table.add_column("Description")

    for definition in list_check_definitions():
        table.add_row(
            definition.code,
            definition.name,
            definition.category,
            str(definition.max_points),
            definition.description,
        )

    console.print(table)


@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="Repository path."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing config file."),
) -> None:
    """Create a default .repopulse.yaml config file."""

    root = path.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        console.print(f"[red]Error:[/red] path is not a directory: {root}")
        raise typer.Exit(code=2)

    try:
        target = write_default_config(root, overwrite=force)
    except FileExistsError as exc:
        console.print(f"[yellow]Config already exists:[/yellow] {exc.filename}")
        console.print("Use --force to overwrite it.")
        raise typer.Exit(code=1) from exc

    console.print(f"[green]Created config:[/green] {target}")


@app.command()
def version() -> None:
    """Show RepoPulse version."""

    console.print(f"RepoPulse {__version__}")


if __name__ == "__main__":
    app()
