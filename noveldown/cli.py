#!/usr/bin/env python3

from typing import Optional

import typer

from . import __version_str__, api, sources

app = typer.Typer()


@app.command()
def download(novel_id: str) -> None:
    pass


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
        for source in sources.get_all_classes():
            typer.echo(f"{source.id}: {source.title}")
        raise typer.Exit()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
