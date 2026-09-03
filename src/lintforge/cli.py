import typer
import subprocess

app = typer.Typer(help="LintForge - AI code refactoring validation tool")

@app.callback()
def main():
    """LintForge - AI code refactoring validation tool"""
    pass

@app.command()
def check(
    original: typer.FileText = typer.Option(..., "--original", help="Original file without any modifications"),
    refracted: typer.FileText = typer.Option(..., "--refracted", help="Refracted code by AI")
):
    if original is None or refracted is None:
        print("[bold red] Error : [/bold red] :smiley:")
        raise typer.Exit(code=1)

    # Static Analysis
    ruff_analysis_res = subprocess.run(
            ["ruff", "check", "--stdin-filename", "original.py", "-"],
            input = original.read(),
            capture_output = True,
            text=True
    )
    if ruff_analysis_res.returncode!=0 :
        print("Linting failed")
        raise typer.Exit(code=1)
    
