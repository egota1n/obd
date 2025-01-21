import multiprocessing
from collections import defaultdict
from functools import partial
import time


def mapper(chunk):
    wordCounts = defaultdict(int)
    for line in chunk:
        words = line.strip().split()
        for word in words:
            wordCounts[word.lower()] += 1
    return wordCounts


def reducer(mappedData):
    combinedCounts = defaultdict(int)
    for data in mappedData:
        for word, count in data.items():
            combinedCounts[word] += count
    return combinedCounts


def split_file(filename, num_chunks):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunkSize = len(lines) // num_chunks
    return [lines[i:i + chunkSize] for i in range(0, len(lines), chunkSize)]


def main(inputFile, numMappers, numReducers):
    startTime = time.time()
    
    chunks = split_file(inputFile, numMappers)

    with multiprocessing.Pool(numMappers) as pool:
        mapped_results = pool.map(mapper, chunks)

    combinedResult = reducer(mapped_results)

    sortedResult = sorted(combinedResult.items(), key=lambda x: x[1], reverse=True)
    
    endTime = time.time()
    
    for word, count in sortedResult:
        print(f"{word}: {count}")
    
    print(f"Время выполнения: {endTime - startTime:.4f} секунд")


inputFile = 'input.txt'
numMappers = 256
numReducers = 256

main(inputFile, numMappers, numReducers)