# made by Jong
# file tree
# root
# |- script (python scripts)
# |- bt (.bt files)
# \- log
# usage: $:/.../bt# python ../script/general_bt_log.py some_bpft_script.bt

import sys
import os
import time
import subprocess


def grep_process(text, catch):
	result = os.popen(f"ps -eLf | grep {text}").read()
	result = result.split("\n")
	filtered = [r.split(" ") for r in result if catch in r]
	for i, line in enumerate(filtered):
		filtered[i] = [w for w in line if w]
	tids = [w[3] for w in filtered]
	return tids


if __name__ == "__main__":
	bt = sys.argv[1]
	log = bt[:-3]

	bt_script = f"../bt/{bt}"

	cmd_bpf = f"nohup bpftrace {bt_script} > ../log/{log}/%d.log &"
	cmd_qemu = "/home/arcuser/serverless/qemu-memory-simulate/disk-img/run.sh -i 0 -m 1235"

	if not os.path.exists(f"../log/{log}"):
		os.system(f"mkdir ../log/{log}")
	offset = len(os.listdir(f"../log/{log}"))
	
	for i in range(1):
		os.system(cmd_bpf % (i+offset))
		time.sleep(1)
		
		sp = subprocess.Popen(cmd_qemu.split(" "), stdout=subprocess.DEVNULL)
		pid = sp.pid + 1
		#print(pid)
		time.sleep(10)
		sp.terminate()
		os.system(f"pkill -P {pid}")
		
		tids = grep_process("bpftrace", bt)
		print(tids)
		os.system(f"kill -2 {tids[0]}")
