import random
import time
from concurrent.futures import ProcessPoolExecutor

def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergeSort(arr[:mid])
    right = mergeSort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def parallelMergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2

    with ProcessPoolExecutor() as executor:
        leftFuture = executor.submit(mergeSort, arr[:mid])
        rightFuture = executor.submit(mergeSort, arr[mid:])
        left = leftFuture.result()
        right = rightFuture.result()

    return merge(left, right)

def measureTime(func, *args):
    startTime = time.time()
    result = func(*args)
    endTime = time.time()
    return result, endTime - startTime

arraySize = 700_000
arr = [random.randint(0, 100_000) for _ in range(arraySize)]

sortedSeq, timeSeq = measureTime(mergeSort, arr)
print("Количество элементов:", arraySize)
print(f"Последовательная сортировка: {timeSeq:.4f} секунд")

sortedPar, timePar = measureTime(parallelMergeSort, arr)
print(f"Параллельная сортировка: {timePar:.4f} секунд")