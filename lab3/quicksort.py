import random
import time
from concurrent.futures import ProcessPoolExecutor

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def parallelQuicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    with ProcessPoolExecutor() as executor:
        leftSorted, rightSorted = executor.map(quicksort, [left, right])

    return leftSorted + middle + rightSorted

def measureTime(func, *args):
    startTime = time.time()
    result = func(*args)
    endTime = time.time()
    return result, endTime - startTime

arraySize = 700_000
arr = [random.randint(0, 100_000) for _ in range(arraySize)]

sortedSeq, timeSeq = measureTime(quicksort, arr)
print("Количество элементов:", arraySize)
print(f"Последовательная сортировка: {timeSeq:.4f} секунд")

sortedPar, timePar = measureTime(parallelQuicksort, arr)
print(f"Параллельная сортировка: {timePar:.4f} секунд")