# made by Jong
# file tree
# root
# |- script (python scripts)
# |- bt (.bt files)
# \- log
# usage: $:/.../bt# python collect_region.py [-v|-a|-b]

import sys
import os
import re
from pprint import pprint

path = "../log/mem_region"

def process_file(fi):
    with open(fi, 'r') as f:
        lines = f.readlines()
    slot_lines = []
    count = 0
    for line in lines:
        if "destroy kvm" in line:
            break
        if "__mr" in line:
            count = 3
            continue
        if count > 0:
            slot_line = re.split(r'\t| ', line[:-1])
            slot_lines.append([w.strip() for w in slot_line if w])
        count -= 1
    result = []
    for i, l in enumerate(slot_lines):
        if i % 3:
            del l[:2]
            result[-1].append(l[1::2])
        else:
            result.append([l[1::2]])
    for i, ll in enumerate(result):
        for j, l in enumerate(ll):
            ll[j] = [int(x, 16) for x in l]

    return result

def show_distr(ref_list, base=False, verbose=False, split=1):
    offset_list = ref_list.copy()
    if base:
        base = offset_list[0][0]
    else:
        base = 0
    start = offset_list[0][0]
    end = offset_list[-1][0]
    if verbose:
    # print hist of addr distribution
        for i, item in enumerate(offset_list):
            print(("%12x - " + "@" * item[1]) % (item[0] - base))
    print(f"start: {hex(start)} end: {hex(end)} offset: {hex(end - start)}\n")

global_addr_list = []

#files = os.listdir(path)
files = [1]
args = sys.argv[1:]

isall = False
isbase = False
isverbose = False

if '-a' in args:
    isall = True
if '-b' in args:
    isbase = True
if '-v' in args:
    isverbose = True

for log in files:
    if isall:
        print(log)
#    plist = process_file(f"{path}/{log}")
    plist = process_file("./log_mem")
    addr_list = list([l[0][4] for l in plist])
    addr_dict = {}
    for addr in addr_list:
        if addr not in addr_dict.keys():
            addr_dict[addr] = 1
        else:
            addr_dict[addr] += 1
    addr_sorted = sorted(list(addr_dict.items()))
    global_addr_list.extend(addr_sorted)
    
    if isall:
        show_distr(addr_sorted, isbase, isverbose)

sorted_list = sorted(global_addr_list)
show_distr(sorted_list, isbase, isverbose)
