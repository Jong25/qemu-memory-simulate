import sys
import os

target="/sys/kernel/debug/tracing/set_ftrace_filter"

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

wlines = [f"*{line[:-1]}*" for line in lines]

os.system(f"echo '' > {target}")
for func in wlines:
    os.system(f"echo {func} >> {target}")
