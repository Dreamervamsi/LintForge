from .utils.cli_utils import get_folder_option
import typer
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

app = typer.Typer(help="LintForge - AI code refactoring validation tool")
console = Console()

@app.callback()
def main():
    """LintForge - AI code refactoring validation tool"""
    pass

def run_ruff_check(directory):
    """Run ruff check and return result."""
    result = subprocess.run(
        ["ruff", "check", "."],
        cwd=str(directory),
        capture_output=True,
        text=True
    )
    return result

def run_pytest(directory):
    """Run pytest and return result."""
    result = subprocess.run(
        ["pytest", ".", "-v"],
        cwd=str(directory),
        capture_output=True,
        text=True
    )
    return result

def parse_pytest_output(output):
    """Parse pytest output to extract test count."""
    try:
        # Searching for patterns like "8 passed in 0.10s" or "8 passed"
        lines = output.split('\n')
        for line in lines:
            if 'passed' in line.lower():
                # Extract the number before "passed"
                parts = line.split()
                for i, part in enumerate(parts):
                    if 'passed' in part.lower():
                        try:
                            count = int(parts[i-1])
                            return count
                        except (ValueError, IndexError):
                            continue
        return 0
    except Exception:
        return 0

def display_results(original_results, refracted_results):
    title = Text("Lint Forge", style="bold blue")
    panel = Panel(title, box=box.DOUBLE, padding=(1, 2))
    console.print(panel)
    console.print()
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Original", style="green", width=20)
    table.add_column("Refracted", style="green", width=20)
    
    # Static Analysis Results
    org_ruff = "✓ PASS" if original_results['ruff'].returncode == 0 else "✗ FAIL"
    ref_ruff = "✓ PASS" if refracted_results['ruff'].returncode == 0 else "✗ FAIL"
    table.add_row("Ruff", org_ruff, ref_ruff)
    
    # Pytest Results
    org_tests = original_results['pytest_count']
    ref_tests = refracted_results['pytest_count']
    org_test_status = f"✓ {org_tests}/{org_tests}" if original_results['pytest'].returncode == 0 else f"✗ {org_tests} failed"
    ref_test_status = f"✓ {ref_tests}/{ref_tests}" if refracted_results['pytest'].returncode == 0 else f"✗ {ref_tests} failed"
    table.add_row("pytest", org_test_status, ref_test_status)
    
    console.print(table)
    console.print()
    
    # Display errors if any
    if original_results['ruff'].returncode != 0:
        console.print(Panel(original_results['ruff'].stdout, title="[bold red]Original Ruff Errors[/bold red]", box=box.ROUNDED))
    
    if refracted_results['ruff'].returncode != 0:
        console.print(Panel(refracted_results['ruff'].stdout, title="[bold red]Refracted Ruff Errors[/bold red]", box=box.ROUNDED))
    
    if original_results['pytest'].returncode != 0:
        console.print(Panel(original_results['pytest'].stdout, title="[bold red]Original Test Errors[/bold red]", box=box.ROUNDED))
    
    if refracted_results['pytest'].returncode != 0:
        console.print(Panel(refracted_results['pytest'].stdout, title="[bold red]Refracted Test Errors[/bold red]", box=box.ROUNDED))

@app.command()
def check(
    original: get_folder_option("--original", "Original codebase without any modifications"),
    refracted: get_folder_option("--refracted", "Refracted codebase by AI")
):
    if original is None or refracted is None:
        console.print("[bold red]Error: Both --original and --refracted must be specified[/bold red]")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Running LintForge analysis...[/bold cyan]")
    console.print()
    
    # Run all checks
    org_ruff = run_ruff_check(original)
    ref_ruff = run_ruff_check(refracted)
    
    org_pytest = run_pytest(original)
    ref_pytest = run_pytest(refracted)
    
    # Parse test counts
    org_test_count = parse_pytest_output(org_pytest.stdout)
    ref_test_count = parse_pytest_output(ref_pytest.stdout)
    
    # Prepare results
    original_results = {
        'ruff': org_ruff,
        'pytest': org_pytest,
        'pytest_count': org_test_count
    }
    
    refracted_results = {
        'ruff': ref_ruff,
        'pytest': ref_pytest,
        'pytest_count': ref_test_count
    }
    
    display_results(original_results, refracted_results)
    
    if (org_ruff.returncode != 0 or ref_ruff.returncode != 0 or 
        org_pytest.returncode != 0 or ref_pytest.returncode != 0):
        raise typer.Exit(code=1)
    
    console.print("[bold green]All checks passed successfully![/bold green]")
