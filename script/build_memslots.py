# made by Jong
# file tree
# root
# |- script (python scripts)
# |- bt (.bt files)
# \- log
# usage: $:/.../bt# python ../script/simulate.py some_bpft_script.bt


import sys
import os
import re
import bisect
import json
from pprint import pprint


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

def mr_code(op):
    if True:
        change = ""
        new = op[0]
        old = op[1]
        #print([hex(o) for o in old])
        #print([hex(n) for n in new])
        if new[3] != 0:
            if not old[3] != 0:
                change = "CREATE"
            else:
                if (new[4] != old[4]) or (new[3] // 0x1000 != old[3]) or (new[1]&old[1]&2):
                    return change
                if new[2] // 0x1000 != old[2]:
                    change = "MOVE"
                elif new[1] != old[1]:
                    change = "FLAGS"
                else:
                    change = "NOTHING"
                    return change
        else:
            if not old[3] != 0:
                return change
            change = "DELETE"
    return change

def print_hex(arg):
    if type(arg) == tuple:
        print(f"({hex(arg[0])}, {hex(arg[1])})")
    elif type(arg) == list:
        print("[", end="")
        for l in arg:
            print(" ", end="")
            print_hex(l)
        print("]")

def simulate(steps, modes, path, verbose=False):
    # memslots = {id: [gpa, addr, size]}
    addr_spaces = [[], []]
    guest_spaces = [[], []]
    memslots = [{}, {}]

    for i, op in enumerate(steps):
        new = op[0]
        old = op[1]
        mode = modes[i]
        
        as_id = new[0] // 0x10000
        mem_id = new[0] % 0x10000

        target_slots = memslots[as_id]

        addr = new[4]
        gpa = new[2]
        size = new[3]

        addr_space = addr_spaces[as_id]
        guest_space = guest_spaces[as_id]

        if mode == "CREATE":
            if mem_id in target_slots.keys():
                print("err CREATE")
            else:
                target_slots[mem_id] = (gpa, addr, size)
                bisect.insort_left(addr_space, (addr, addr+size))
                bisect.insort_left(guest_space, (gpa, gpa+size))
        elif mode == "DELETE":
            if mem_id not in target_slots.keys():
                print("err DELETE")
            else:
                del target_slots[mem_id]
                del addr_space[bisect.bisect(addr_space, (addr, addr+size))]
                del guest_space[bisect.bisect(guest_space, (gpa, gpa+size))]


    hex_addr_space = [[(hex(a[0]), hex(a[1])) for a in addr_spaces[0]], [(hex(a[0]), hex(a[1])) for a in addr_spaces[1]]]
    hex_guest_space = [[(hex(g[0]), hex(g[1])) for g in guest_spaces[0]], [(hex(g[0]), hex(g[1])) for g in guest_spaces[1]]]
    hex_memslots = [ {k:(hex(v[0]), hex(v[1]), hex(v[2])) for k,v in memslots[0].items()}, {k:(hex(v[0]), hex(v[1]), hex(v[2])) for k,v in memslots[1].items()} ]

    if verbose:
        print("address space")
        pprint(hex_addr_space)
        print("guest space")
        pprint(hex_guest_space)
        print("memslots")
        pprint(hex_memslots)
    
    with open(path, 'w') as f:
        f.write(json.dumps(addr_spaces))
        f.write("\n")
        f.write(json.dumps(guest_spaces))
        f.write("\n")
        f.write(json.dumps(memslots))


def run(log_path, json_path):
    plist = process_file(log_path)
    modes = [mr_code(step) for step in plist]
    simulate(plist, modes, json_path)