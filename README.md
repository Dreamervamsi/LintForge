# LintForge

LintForge is an AI code refactoring validation tool that helps you compare the performance and correctness of original code against AI-refactored versions. It provides automated testing, static analysis, and performance benchmarking to ensure your refactored code maintains quality and improves efficiency.

## Features

- **Static Analysis**: Run Ruff checks on both original and refracted codebases
- **Automated Testing**: Execute pytest test suites to verify correctness
- **Performance Benchmarking**: Compare execution times across different input sizes
- **Decision Engine**: Automatically decide whether to ACCEPT, REJECT, or REVIEW refactored code based on performance metrics
- **Rich Output**: Beautiful, structured terminal output using the Rich library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dreamervamsi/LintForge.git
cd LintForge
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

### Basic Check

Run static analysis and tests on both codebases:

```bash
lintforge check --original examples/original --refracted examples/refracted
```

### Performance Benchmarking

Compare performance between original and refracted implementations:

```bash
lintforge benchmark --original examples/original --refracted examples/refracted
``

You can specify custom benchmark configurations:

```bash
lintforge benchmark \
  --original examples/original \
  --refracted examples/refracted \
  --original-config original_linear_search.yaml \
  --refracted-config refracted_binary_search.yaml
```

## Benchmark Configuration

Benchmarks are configured using YAML files in the `benchmark/` directory. Each config specifies:

- **name**: Benchmark identifier
- **module**: Python module path to the function
- **function**: Function name to benchmark
- **input_generator**: Function to generate test inputs
- **sizes**: Array of input sizes to test
- **iterations**: Number of iterations per size
- **description**: Human-readable description

Example configuration:
```yaml
name: "binary_search"
module: "refracted.binary_search"
function: "binary_search"
input_generator: "generate_sorted_array"
sizes: [100, 1000, 10000, 100000]
iterations: 100
description: "Binary search benchmark for refracted implementation"
```

## Performance Metrics

The benchmarking system measures execution time across different input sizes and provides detailed metrics:

| Input Size | Original Time (s) | Refracted Time (s) | Speedup | Decision |
|------------|-------------------|-------------------|---------|----------|
| 100        | 0.000012          | 0.000008          | 1.50x   | ACCEPT   |
| 1,000      | 0.000120          | 0.000015          | 8.00x   | ACCEPT   |
| 10,000     | 0.001200          | 0.000018          | 66.67x  | ACCEPT   |
| 100,000    | 0.012000          | 0.000020          | 600.00x | ACCEPT   |

**Decision Criteria:**
- **ACCEPT**: Refracted code is ≥20% faster (speedup ≥ 1.2)
- **REJECT**: Refracted code is ≥20% slower (speedup ≤ 0.8)
- **REVIEW**: Performance difference is within ±20%

## Project Structure

```
LintForge/
├── benchmark/              # Benchmark configuration files
│   ├── original_linear_search.yaml
│   └── refracted_binary_search.yaml
├── examples/               # Example codebases
│   ├── original/           # Original implementation
│   └── refracted/          # AI-refactored implementation
├── src/
│   └── lintforge/
│       ├── cli.py          # Command-line interface
│       ├── utils/          # Utility functions
│       └── workload/        # Benchmarking and decision engine
│           ├── workload.py
│           ├── decision_engine.py
│           └── benchmark_loader.py
└── pyproject.toml          # Project configuration
```

## Tech Stack

- **Python 3.13+**: Core programming language
- **Typer**: Command-line interface framework
- **Rich**: Terminal output formatting
- **Ruff**: Fast Python linter
- **pytest**: Testing framework
- **PyYAML**: Configuration file parsing
- **psutil**: System and process utilities

## License

This project is licensed under the MIT License.