import sys
import os
import time
import subprocess
import json
from pprint import pprint
from telnetlib import Telnet
from script import build_memslots, extract_cr3, build_page_table
from script.general_bt_log import grep_process

seed = int(time.time())
port = 1235

paths = {
    "mem_bpf": "bt/mem_region.bt",
    "mem_bpf_log": f"log/mem_region/{seed}",
    "memslots": f"qemu-monitor/file/memslots_{seed}",
    "cr3_bpf": "bt/get_cr3.bt",
    "cr3_bpf_log": f"log/get_cr3/{seed}",
    "cr3": f"qemu-monitor/file/cr3_{seed}",
    "pmem": f"qemu-monitor/file/pmem_{seed}",
    "pagetable": "qemu-monitor/table/",
    "target": ""
}


cmd_bpf_mem = f"nohup bpftrace {paths['mem_bpf']} > {paths['mem_bpf_log']} &"
name_bpf_mem = paths["mem_bpf"][3:-3]
cmd_bpf_cr3 = f"nohup bpftrace {paths['cr3_bpf']} > {paths['cr3_bpf_log']} &"
name_bpf_cr3 = paths["cr3_bpf"][3:-3]

cmd_qemu = f"qemu-memory-simulate/disk-img/run.sh -i 0 -m {port}"
cmd_telnet = f"telnet 127.0.0.1 {port}"

def init_dir(dpath):
    if not os.path.exists(dpath):
        os.system(f"mkdir {dpath}")
    else:
        os.system(f"rm {dpath}/*")


log_list = [p[:p.rfind('/')]for p in paths.values() if '.' not in p]
for log in log_list:
    init_dir(log)

os.system(cmd_bpf_mem)
os.system(cmd_bpf_cr3)
time.sleep(1)


sp = subprocess.Popen(cmd_qemu.split(" "), stdout=subprocess.DEVNULL)
qemu_pid = sp.pid + 1
time.sleep(10)
print(qemu_pid)


access_count_memslot = {}
access_count_table = {}

try:
    tids = grep_process("bpftrace", name_bpf_mem)
    print(tids)
    os.system(f"kill -2 {tids[0]}")

    tids = grep_process("bpftrace", name_bpf_cr3)
    print(tids)
    os.system(f"kill -2 {tids[0]}")


    build_memslots.run(paths["mem_bpf_log"], paths["memslots"])
    extract_cr3.run(paths["cr3_bpf_log"], paths["cr3"])


    with open(paths["memslots"], 'r') as f:
        addr_spaces, guest_spaces, memslots = list(map(json.loads, f.readlines()))
    pprint(memslots)
    for mid, v in memslots[0].items():
        access_count_memslot[int(mid)] = 0


    with Telnet('localhost', port) as tn:
        query = f"pmemsave 0 {512 * 2 ** 20} pmem\n".encode("utf-8")
        # tn.write(b"info registers\n")
        # print("hey")
        # print(tn.read_until(b"CR3"))
        # print("hoy")
        tn.write(query)
        time.sleep(10)

    os.system(f"mv pmem {paths['pmem']}")
    page_table = build_page_table.run(paths["cr3"], paths["pmem"], paths["pagetable"], verbose=True)
    pprint(page_table)
    for cr3, pt in page_table.items():
        access_count_table[int(cr3, 16)]

    os.system(f"cat /proc/{qemu_pid}/maps > qemu-monitor/file/maps_{seed}")

    sp.terminate()
    os.system(f"pkill -P {qemu_pid}")

except Exception as e:
    print(e)
    sp.terminate()
    os.system(f"pkill -P {qemu_pid}")