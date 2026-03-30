#!/usr/bin/env python3
"""Generate mash_triangle PHYLIP reference files for Galaxy tool tests.
Usage: python convert_triangle.py <raw_input> <output> <mode> [--relaxed] [--diagonal] --name-map '<json>'
Modes: square, lower_triangle, upper_triangle
"""
import json
import sys

# Parse args
input_file = sys.argv[1]
output_file = sys.argv[2]
mode = sys.argv[3]
relaxed = '--relaxed' in sys.argv
diagonal = '--diagonal' in sys.argv

name_map = {}
for i, arg in enumerate(sys.argv):
    if arg == '--name-map' and i + 1 < len(sys.argv):
        name_map = json.loads(sys.argv[i + 1])

with open(input_file) as f:
    lines = f.read().strip().split('\n')

n = int(lines[0].strip())
raw_names = []
matrix = [[0.0] * n for _ in range(n)]

for i in range(n):
    parts = lines[i + 1].split('\t')
    raw_name = parts[0]
    raw_names.append(name_map.get(raw_name, raw_name))
    for j in range(len(parts) - 1):
        val = float(parts[j + 1])
        matrix[i][j] = val
        matrix[j][i] = val

if relaxed:
    max_len = max(len(nm) for nm in raw_names)
    pad = max(max_len, 10)
    names = [nm.ljust(pad) for nm in raw_names]
else:
    names = [nm[:10].ljust(10) for nm in raw_names]

fmt = [['%.6f' % matrix[i][j] for j in range(n)] for i in range(n)]
col_w = [max(len(fmt[i][j]) for i in range(n)) for j in range(n)]

with open(output_file, 'w') as f:
    f.write('%d\n' % n)
    for i in range(n):
        if mode == 'square':
            parts = [fmt[i][j].rjust(col_w[j]) for j in range(n)]
        elif mode == 'lower_triangle':
            end = i + 1 if diagonal else i
            parts = [fmt[i][j].rjust(col_w[j]) for j in range(end)]
        elif mode == 'upper_triangle':
            start = i if diagonal else i + 1
            parts = []
            for j in range(n):
                if j < start:
                    parts.append(' ' * col_w[j])
                else:
                    parts.append(fmt[i][j].rjust(col_w[j]))

        if not parts or all(p.isspace() for p in parts):
            f.write('%s\n' % names[i].rstrip())
        elif relaxed:
            f.write('%s %s\n' % (names[i], ' '.join(parts)))
        else:
            f.write('%s%s\n' % (names[i], ' '.join(parts)))
