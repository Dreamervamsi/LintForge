from dataclasses import dataclass
from typing import Any, Callable, List
import time


@dataclass
class Workload:
    """Workload configuration for performance benchmarking."""
    
    operation: Callable  # The function to benchmark
    operation_name: str  # Name of the operation (e.g., "linear_search", "binary_search")
    input_generator: Callable[[int], Any]  # Function that generates input based on size
    sizes: List[int]  # List of input sizes to test
    iterations: int  # Number of iterations per size
    
    def run(self) -> dict:
        """Run the workload and return performance results."""
        results = {}
        
        for size in self.sizes:
            input_data = self.input_generator(size)
            times = []
            
            for _ in range(self.iterations):
                start_time = time.perf_counter()
                self.operation(input_data, size // 2)  # Search for middle element
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
