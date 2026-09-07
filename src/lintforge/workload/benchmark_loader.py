import yaml
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class BenchmarkConfig:
    """Benchmark configuration loaded from YAML file."""
    name: str
    module: str
    function: str
    input_generator: str
    sizes: list[int]
    iterations: int
    description: str


class BenchmarkLoader:
    """Load benchmark configurations from YAML files."""
    
    def __init__(self, benchmark_dir: Path):
      
        self.benchmark_dir = benchmark_dir
    
    def load_config(self, config_file: str) -> BenchmarkConfig:
        config_path = self.benchmark_dir / config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"Benchmark config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return BenchmarkConfig(
            name=data['name'],
            module=data['module'],
            function=data['function'],
            input_generator=data['input_generator'],
            sizes=data['sizes'],
            iterations=data['iterations'],
            description=data.get('description', '')
        )
    
    def load_all_configs(self) -> Dict[str, BenchmarkConfig]:
        configs = {}
        
        for config_file in self.benchmark_dir.glob("*.yaml"):
            config = self.load_config(config_file.name)
            configs[config.name] = config
        
        return configs
