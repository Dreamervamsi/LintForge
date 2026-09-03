def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i

    return -1


arr = [2, 5, 8, 12, 16, 23, 38, 45, 57]

print(linear_search(arr, 23))