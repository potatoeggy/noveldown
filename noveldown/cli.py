#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer

from . import __version_str__, api, sources

app = typer.Typer()


@app.command()
def get(novel_id: str, path: Path = Path(".")) -> None:
    """
    Download a novel.
    """
    typer.echo(f"Searching for {novel_id}...")
    try:
        novel = api.query(novel_id)
    except ValueError as err:
        typer.secho("Invalid ID.", fg=typer.colors.RED)
        raise typer.Exit(1) from err

    typer.secho("Found novel:", fg=typer.colors.GREEN)
    typer.echo(novel)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        is_eager=True,
        help="Display the current version of noveldown",
    ),
    supported_ids: Optional[bool] = typer.Option(
        None,
        "--supported-ids",
        is_eager=True,
        help="Output a list of IDs supported by noveldown",
    ),
) -> None:

    if version:
        typer.echo(f"noveldown {__version_str__}")
        raise typer.Exit()

    if supported_ids:
        typer.echo("Story title: Story ID")
        for source in sources.get_all_classes():
            typer.echo(f"{source.title}: {source.id}")
        raise typer.Exit()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
