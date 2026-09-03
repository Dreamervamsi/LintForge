from src.lintforge.orchestrator import greet
def test_a():
    assert greet("vamsi") == "krishna"

def test_b():
    assert greet("krishna") == "Hello krishna"