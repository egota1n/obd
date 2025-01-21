#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    if len(parts) < 2:
        continue
    
    parent, child = parts[0], parts[1]
    print(f"{child}\t{parent}")