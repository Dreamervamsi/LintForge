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
    ref_analysis_res = subprocess.run(
            ["ruff", "check", "."],
            cwd=str(refracted),
            capture_output = True,
            text=True
    )
    org_analysis_res = subprocess.run(
        ["ruff","check","."],
        cwd=str(original),
        capture_output=True,
        text=True
    )

    if org_analysis_res.returncode!=0 or ref_analysis_res.returncode!=0:
        print("Linting failed")
        raise typer.Exit(code=1)
    
    # Behavioural Test
    org_test = subprocess.run(
        ["pytest","."],
        cwd=str(original),
        capture_output=True,
        text=True
    )
    
    ref_test = subprocess.run(
        ["pytest","."],
        cwd=str(refracted),
        capture_output=True,
        text=True
    )
    
    if org_test.returncode!=0 or ref_test.returncode!=0:
        print("Testing failed")
        raise typer.Exit(code=1)
    
    print("Original codebase testing result:")
    print(org_test.stdout)
    
    print("Refracted codebase testing result:")
    print(ref_test.stdout)
