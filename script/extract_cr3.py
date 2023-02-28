def align(addr):
	return addr & (~0xfff)


def process_file(fi):
    with open(fi, 'r') as f:
        lines = f.readlines()
    cr3_list = []
    cr3_base_set = set()
    for line in lines:
        if "cr3" in line:
            cr3 = int(line.split(": ")[1].strip(), 16)
            if cr3 != 0 and align(cr3) not in cr3_base_set:
                cr3_list.append(hex(cr3))
                cr3_base_set.add(align((cr3)))

    return cr3_list


def run(log_path, txt_path):
    plist = process_file(log_path)
    print(plist)
    with open(txt_path, 'w') as f:
        for cr3 in plist:
             f.write(cr3 + '\n')