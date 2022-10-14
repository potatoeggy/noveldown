#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer

from . import __version_str__, api, sources

app = typer.Typer()


def version_callback(val: bool | None) -> None:
    if val:
        typer.echo(f"noveldown {__version_str__}")
        raise typer.Exit()


def supported_ids_callback(val: bool | None) -> None:
    if val:
        typer.secho(
            "Story title: Story ID (case-insensitive)", fg=typer.colors.BRIGHT_BLUE
        )
        for source in sources.get_all_classes():
            typer.echo(
                f"{source.title}: {source.id} (aliases: {', '.join(source.aliases) or 'none'})"
            )
        raise typer.Exit()


@app.command(no_args_is_help=True)
def get(
    novel_id: str,
    path: Path = typer.Argument(Path.cwd(), help="The path to download to"),
    start: int | None = None,
    end: int | None = None,
    version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None,
        "--version",
        "-v",
        is_eager=True,
        callback=version_callback,
        help="Display the current version of noveldown",
    ),
    supported_ids: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None,
        "--supported-ids",
        "-s",
        is_eager=True,
        callback=supported_ids_callback,
        help="Output a list of IDs supported by noveldown",
    ),
) -> None:
    """
    Download a novel.
    """
    typer.echo(f"Searching for '{novel_id}'...")
    try:
        novel = api.query(novel_id)
    except ValueError as err:
        typer.secho("Invalid ID.", fg=typer.colors.RED)
        raise typer.Exit(1) from err

    typer.secho("Found novel:", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(novel)

    start = start or 0
    end = end or len(novel.chapters_flattened)
    novel.set_chapter_range(start=start, end=end)

    typer.secho("Downloading...", fg=typer.colors.BRIGHT_GREEN)
    with typer.progressbar(
        api.prefetch_book(novel),
        length=end - start,
        show_eta=True,
    ) as progress:
        for title in progress:
            progress.label = title

    typer.secho("Converting to EPUB...", fg=typer.colors.BRIGHT_GREEN)
    with typer.progressbar(
        api.download_progress(novel, path),
        length=end - start,
        show_eta=True,
    ) as progress:
        for title in progress:
            progress.label = title

    typer.secho(
        f"Successfully downloaded {novel.title} to {path / novel.title}.epub.",
        fg=typer.colors.BRIGHT_GREEN,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
