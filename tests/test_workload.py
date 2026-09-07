from lintforge.workload import Workload


def test_workload_creation():
    """Test that Workload can be created with valid parameters."""
    def dummy_operation(arr, target):
        return -1
    
    def dummy_generator(size):
        return list(range(size))
    
    workload = Workload(
        operation=dummy_operation,
        operation_name="test",
        input_generator=dummy_generator,
        sizes=[10, 100],
        iterations=10
    )
    
    assert workload.operation_name == "test"
    assert workload.sizes == [10, 100]
    assert workload.iterations == 10


def test_workload_run():
    """Test that Workload.run() executes and returns results."""
    def dummy_operation(arr, target):
        return -1
    
    def dummy_generator(size):
        return list(range(size))
    
    workload = Workload(
        operation=dummy_operation,
        operation_name="test",
        input_generator=dummy_generator,
        sizes=[10],
        iterations=5
    )
    
    results = workload.run()
    
    assert 10 in results
    assert "avg_time" in results[10]
    assert "min_time" in results[10]
    assert "max_time" in results[10]
    assert results[10]["iterations"] == 5
