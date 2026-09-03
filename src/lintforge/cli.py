from pathlib import Path
from typing import Annotated
import typer
import subprocess

app = typer.Typer(help="LintForge - AI code refactoring validation tool")

@app.callback()
def main():
    """LintForge - AI code refactoring validation tool"""
    pass
def get_folder_option(option:str, description:str):
    return Annotated[
        Path,
        typer.Option(
            option,
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help=description
        )
    ]
@app.command()
def check(
    original: get_folder_option("--original", "Original codebase without any modifications"),
    refracted: get_folder_option("--refracted", "Refracted codebase by AI")
):
    if original is None or refracted is None:
        print("[bold red] Error : [/bold red] :smiley:")
        raise typer.Exit(code=1)

    # Static Analysis
    ruff_analysis_res = subprocess.run(
            ["ruff", "check", "."],
            cwd=str(original),
            capture_output = True,
            text=True
    )
    if ruff_analysis_res.returncode!=0 :
        print("Linting failed")
        raise typer.Exit(code=1)
    print('[bold magenta]Linting Success[/bold magenta]')
