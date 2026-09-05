from refracted.binary_search import binary_search


def test_binary_search_found():
    """Test binary_search when target is found in sorted array."""
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 57]
    assert binary_search(arr, 23) == 5
    assert binary_search(arr, 2) == 0
    assert binary_search(arr, 57) == 8

def test_binary_search_not_found():
    """Test binary_search when target is not found in sorted array."""
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 57]
    assert binary_search(arr, 1) == -1
    assert binary_search(arr, 100) == -1
    assert binary_search(arr, 0) == -1


def test_binary_search_empty_array():
    """Test binary_search with empty array."""
    assert binary_search([], 5) == -1


def test_binary_search_single_element():
    """Test binary_search with single element array."""
    assert binary_search([5], 5) == 0
    assert binary_search([5], 3) == -1


def test_binary_search_first_element():
    """Test binary_search finding first element."""
    arr = [10, 20, 30, 40]
    assert binary_search(arr, 10) == 0


def test_binary_search_last_element():
    """Test binary_search finding last element."""
    arr = [10, 20, 30, 40]
    assert binary_search(arr, 40) == 3


def test_binary_search_middle_element():
    """Test binary_search finding middle element."""
    arr = [10, 20, 30, 40, 50]
    assert binary_search(arr, 30) == 2


def test_binary_search_duplicates():
    """Test binary_search with duplicate elements (should return one of the indices)."""
    arr = [5, 10, 10, 15, 20]
    result = binary_search(arr, 10)
    assert result in [1, 2]  # Could return either index of the duplicate


def test_binary_search_even_length():
    """Test binary_search with even length array."""
    arr = [1, 2, 3, 4]
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 4) == 3
    assert binary_search(arr, 2) == 1
    assert binary_search(arr, 3) == 2


def test_binary_search_odd_length():
    """Test binary_search with odd length array."""
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 3) == 2
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 5) == 4


def test_binary_search_negative_numbers():
    """Test binary_search with negative numbers."""
    arr = [-10, -5, 0, 5, 10]
    assert binary_search(arr, -5) == 1
    assert binary_search(arr, 0) == 2
    assert binary_search(arr, 10) == 4
