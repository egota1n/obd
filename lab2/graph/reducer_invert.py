#!/usr/bin/env python3
import sys

current_child = None
parent_count = 0

for line in sys.stdin:
    line = line.strip()
    try:
        child, parent = line.split("\t", 1)
    except ValueError:
        continue

    if current_child == child:
        parent_count += 1
    else:
        if current_child is not None:
            print(f"{current_child}\t{parent_count}")
        current_child = child
        parent_count = 1

if current_child is not None:
    print(f"{current_child}\t{parent_count}")