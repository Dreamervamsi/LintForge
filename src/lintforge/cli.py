from .utils.cli_utils import get_folder_option, run_ruff_check, run_pytest, parse_pytest_output, display_results, console
from .workload import Workload, DecisionEngine, Decision, BenchmarkLoader, BenchmarkConfig
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
def analyze(
    original: get_folder_option("--original", "Original codebase without any modifications"),
    refracted: get_folder_option("--refracted", "Refracted codebase by AI"),
    original_config: str = typer.Option("original_linear_search.yaml", help="Benchmark config file for original"),
    refracted_config: str = typer.Option("refracted_binary_search.yaml", help="Benchmark config file for refracted")
):
    """Run complete analysis: static checks, tests, and performance benchmarking."""
    if original is None or refracted is None:
        console.print("[bold red]Error: Both --original and --refracted must be specified[/bold red]")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Running complete LintForge analysis...[/bold cyan]")
    console.print()
    
    # Run static checks and tests
    console.print("[cyan]Phase 1: Static Analysis & Testing[/cyan]")
    console.print()
    
    org_ruff = run_ruff_check(original)
    ref_ruff = run_ruff_check(refracted)
    
    org_pytest = run_pytest(original)
    ref_pytest = run_pytest(refracted)
    
    org_test_count = parse_pytest_output(org_pytest.stdout)
    ref_test_count = parse_pytest_output(ref_pytest.stdout)
    
    # Display check results
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
    
    # Check if static analysis passed
    if (org_ruff.returncode != 0 or ref_ruff.returncode != 0 or 
        org_pytest.returncode != 0 or ref_pytest.returncode != 0):
        console.print("[bold yellow]Static analysis or tests failed. Skipping performance benchmark.[/bold yellow]")
        raise typer.Exit(code=1)
    
    console.print("[bold green]✓ Static analysis and tests passed![/bold green]")
    console.print()
    
    # Run performance benchmarking
    console.print("[cyan]Phase 2: Performance Benchmarking[/cyan]")
    console.print()
    
    benchmark_dir = Path(__file__).parent.parent.parent / "benchmark"
    loader = BenchmarkLoader(benchmark_dir)
    
    try:
        orig_config = loader.load_config(original_config)
        ref_config = loader.load_config(refracted_config)
    except FileNotFoundError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1)
    
    orig_module = load_module_from_src(original, orig_config.module)
    ref_module = load_module_from_src(refracted, ref_config.module)
    
    if orig_module is None:
        console.print(f"[bold red]Error: Could not load original module: {orig_config.module}[/bold red]")
        raise typer.Exit(code=1)
    
    if ref_module is None:
        console.print(f"[bold red]Error: Could not load refracted module: {ref_config.module}[/bold red]")
        raise typer.Exit(code=1)
    
    orig_func = getattr(orig_module, orig_config.function)
    ref_func = getattr(ref_module, ref_config.function)
    input_gen = globals().get(orig_config.input_generator, generate_sorted_array)
    
    orig_workload = Workload(
        operation=orig_func,
        operation_name=orig_config.name,
        input_generator=input_gen,
        sizes=orig_config.sizes,
        iterations=orig_config.iterations
    )
    
    ref_workload = Workload(
        operation=ref_func,
        operation_name=ref_config.name,
        input_generator=input_gen,
        sizes=ref_config.sizes,
        iterations=ref_config.iterations
    )
    
    console.print(f"[cyan]Benchmarking {orig_config.name} vs {ref_config.name}...[/cyan]")
    console.print()
    
    orig_results = orig_workload.run()
    ref_results = ref_workload.run()
    
    engine = DecisionEngine()
    comparison = engine.compare(orig_results, ref_results)
    
    display_benchmark_results(comparison, orig_results, ref_results, orig_config, ref_config)
    
    # Final summary
    console.print()
    title = Text("Analysis Complete", style="bold green")
    panel = Panel(title, box=box.DOUBLE, padding=(1, 2))
    console.print(panel)

@app.command()
def benchmark(
    original: get_folder_option("--original", "Original codebase without any modifications"),
    refracted: get_folder_option("--refracted", "Refracted codebase by AI"),
    original_config: str = typer.Option("original_linear_search.yaml", help="Benchmark config file for original"),
    refracted_config: str = typer.Option("refracted_binary_search.yaml", help="Benchmark config file for refracted")
):
    if original is None or refracted is None:
        console.print("[bold red]Error: Both --original and --refracted must be specified[/bold red]")
        raise typer.Exit(code=1)
    
    console.print("[bold cyan]Running performance benchmark...[/bold cyan]")
    console.print()
    
    # Load benchmark configurations
    benchmark_dir = Path(__file__).parent.parent.parent / "benchmark"
    loader = BenchmarkLoader(benchmark_dir)
    
    try:
        orig_config = loader.load_config(original_config)
        ref_config = loader.load_config(refracted_config)
    except FileNotFoundError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1)
    
    # Load modules based on configs
    orig_module = load_module_from_src(original, orig_config.module)
    ref_module = load_module_from_src(refracted, ref_config.module)
    
    if orig_module is None:
        console.print(f"[bold red]Error: Could not load original module: {orig_config.module}[/bold red]")
        raise typer.Exit(code=1)
    
    if ref_module is None:
        console.print(f"[bold red]Error: Could not load refracted module: {ref_config.module}[/bold red]")
        raise typer.Exit(code=1)
    
    # Get functions from modules
    orig_func = getattr(orig_module, orig_config.function)
    ref_func = getattr(ref_module, ref_config.function)
    
    # Get input generator
    input_gen = globals().get(orig_config.input_generator, generate_sorted_array)
    
    # Create workloads from configs
    orig_workload = Workload(
        operation=orig_func,
        operation_name=orig_config.name,
        input_generator=input_gen,
        sizes=orig_config.sizes,
        iterations=orig_config.iterations
    )
    
    ref_workload = Workload(
        operation=ref_func,
        operation_name=ref_config.name,
        input_generator=input_gen,
        sizes=ref_config.sizes,
        iterations=ref_config.iterations
    )
    
    # Run benchmarks
    console.print(f"[cyan]Benchmarking {orig_config.name} vs {ref_config.name}...[/cyan]")
    console.print()
    
    orig_results = orig_workload.run()
    ref_results = ref_workload.run()
    
    # Compare results
    engine = DecisionEngine()
    comparison = engine.compare(orig_results, ref_results)
    
    # Display results
    display_benchmark_results(comparison, orig_results, ref_results, orig_config, ref_config)

def display_benchmark_results(comparison, orig_results, ref_results, orig_config, ref_config):
    """Display benchmark results using rich formatting."""
    title = Text("Performance Benchmark", style="bold blue")
    panel = Panel(title, box=box.DOUBLE, padding=(1, 2))
    console.print(panel)
    console.print()
    
    # Config info
    console.print(f"[cyan]Original:[/cyan] {orig_config.name} - {orig_config.description}")
    console.print(f"[cyan]Refracted:[/cyan] {ref_config.name} - {ref_config.description}")
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
