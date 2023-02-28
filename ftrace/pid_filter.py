import sys
import os
import re

target = ["/sys/kernel/debug/tracing/set_event_pid", "/sys/kernel/debug/tracing/set_ftrace_pid"]
p = "virtiofs"
exc1 = "sudo"
exc2 = "cpulimit"

result = os.popen(f"ps -eLf | grep qemu").read()
result = result.split("\n")
#print(len(result))
filtered = [r.split(" ") for r in result if p in r and exc1 not in r and exc2 not in r]
for i, line in enumerate(filtered):
    filtered[i] = [w for w in line if w]
#print(filtered)
tids = [w[3] for w in filtered]
print(tids)

for t in target:
    os.system(f"echo '' > {t}")
    for tid in tids:
        os.system(f"echo {tid} >> {t}")
