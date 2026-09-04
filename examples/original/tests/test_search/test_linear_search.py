from original.search.linear_search import linear_search


def test_linear_search_found():
    """Test linear_search when target is found in array."""
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 57]
    assert linear_search(arr, 23) == 5
    assert linear_search(arr, 2) == 0
    assert linear_search(arr, 57) == 8


def test_linear_search_not_found():
    """Test linear_search when target is not found in array."""
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 57]
    assert linear_search(arr, 1) == -1
    assert linear_search(arr, 100) == -1
    assert linear_search(arr, 0) == -1


def test_linear_search_empty_array():
    """Test linear_search with empty array."""
    assert linear_search([], 5) == -1


def test_linear_search_single_element():
    """Test linear_search with single element array."""
    assert linear_search([5], 5) == 0
    assert linear_search([5], 3) == -1


def test_linear_search_first_element():
    """Test linear_search finding first element."""
    arr = [10, 20, 30, 40]
    assert linear_search(arr, 10) == 0


def test_linear_search_last_element():
    """Test linear_search finding last element."""
    arr = [10, 20, 30, 40]
    assert linear_search(arr, 40) == 3


def test_linear_search_duplicates():
    """Test linear_search with duplicate elements (should return first occurrence)."""
    arr = [5, 10, 5, 15, 5]
    assert linear_search(arr, 5) == 0
