from .utils.cli_utils import get_folder_option, run_ruff_check, run_pytest, parse_pytest_output, display_results, console
from .workload import Workload, DecisionEngine, Decision
import typer
import sys
import importlib.util
from pathlib import Path
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

app = typer.Typer(help="LintForge - AI code refactoring validation tool")

@app.callback()
def main():
    """LintForge - AI code refactoring validation tool"""
    pass

def load_module_from_src(directory: Path, module_name: str):
    """Load a Python module from the src directory of a project."""
    src_dir = directory / "src"
    module_path = src_dir / f"{module_name.replace('.', '/')}.py"
    
    if not module_path.exists():
        return None
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        return None
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def generate_sorted_array(size: int):
    """Generate a sorted array of given size."""
    return list(range(size))

@app.command()
def benchmark(
    original: get_folder_option("--original", "Original codebase without any modifications"),
    refracted: get_folder_option("--refracted", "Refracted codebase by AI"),
    sizes: str = typer.Option("100,1000,10000", help="Comma-separated list of input sizes"),
    iterations: int = typer.Option(100, help="Number of iterations per size")
):
    """Run performance benchmark comparing original and refracted code."""
    if original is None or refracted is None:
        console.print("[bold red]Error: Both --original and --refracted must be specified[/bold red]")
        raise typer.Exit(code=1)
    
    size_list = [int(s.strip()) for s in sizes.split(",")]
    
    console.print("[bold cyan]Running performance benchmark...[/bold cyan]")
    console.print()
    
    # Load modules
    orig_module = load_module_from_src(original, "original.search.linear_search")
    ref_module = load_module_from_src(refracted, "refracted.binary_search")
    
    if orig_module is None:
        console.print("[bold red]Error: Could not load original module[/bold red]")
        raise typer.Exit(code=1)
    
    if ref_module is None:
        console.print("[bold red]Error: Could not load refracted module[/bold red]")
        raise typer.Exit(code=1)
    
    # Create workloads
    orig_workload = Workload(
        operation=orig_module.linear_search,
        operation_name="linear_search",
        input_generator=generate_sorted_array,
        sizes=size_list,
        iterations=iterations
    )
    
    ref_workload = Workload(
        operation=ref_module.binary_search,
        operation_name="binary_search",
        input_generator=generate_sorted_array,
        sizes=size_list,
        iterations=iterations
    )
    
    # Run benchmarks
    orig_results = orig_workload.run()
    ref_results = ref_workload.run()
    
    # Compare results
    engine = DecisionEngine()
    comparison = engine.compare(orig_results, ref_results)
    
    # Display results
    display_benchmark_results(comparison, orig_results, ref_results)

def display_benchmark_results(comparison, orig_results, ref_results):
    """Display benchmark results using rich formatting."""
    title = Text("Performance Benchmark", style="bold blue")
    panel = Panel(title, box=box.DOUBLE, padding=(1, 2))
    console.print(panel)
    console.print()
    
    # Decision panel
    decision_color = {
        Decision.ACCEPT: "green",
        Decision.REJECT: "red",
        Decision.REVIEW: "yellow"
    }
    
    decision_text = Text(f"Decision: {comparison['decision'].value}", style=f"bold {decision_color[comparison['decision']]}")
    decision_panel = Panel(decision_text, box=box.ROUNDED)
    console.print(decision_panel)
    console.print()
    
    # Detailed results table
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Size", style="cyan", width=10)
    table.add_column("Original (s)", style="green", width=15)
    table.add_column("Refracted (s)", style="green", width=15)
    table.add_column("Speedup", style="yellow", width=10)
    table.add_column("Decision", style="cyan", width=10)
    
    for detail in comparison["details"]:
        size = detail["size"]
        orig_time = f"{detail['original_avg']:.6f}"
        ref_time = f"{detail['refracted_avg']:.6f}"
        speedup = f"{detail['speedup']:.2f}x"
        decision = detail["decision"].value
        decision_style = decision_color[detail["decision"]]
        
        table.add_row(str(size), orig_time, ref_time, speedup, f"[{decision_style}]{decision}[/{decision_style}]")
    
    console.print(table)
    console.print()
    
    # Exit with appropriate code
    if comparison["decision"] == Decision.REJECT:
        raise typer.Exit(code=1)
    elif comparison["decision"] == Decision.REVIEW:
        raise typer.Exit(code=2)

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
