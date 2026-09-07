import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Workload:
    """Workload configuration for performance benchmarking."""
    
    operation: Callable 
    operation_name: str
    input_generator: Callable[[int], Any]
    sizes: list[int]
    iterations: int
    
    def run(self) -> dict:
        results = {}
        
        for size in self.sizes:
            input_data = self.input_generator(size)
            times = []
            
            for _ in range(self.iterations):
                start_time = time.perf_counter()
                self.operation(input_data, size // 2)
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            results[size] = {
                "avg_time": avg_time,
                "min_time": min(times),
                "max_time": max(times),
                "iterations": self.iterations
            }
        
        return results
