import os
import sys
from pprint import pprint

WORD_SIZE = 8
PAGE_SIZE = 4 * 1024
PRESENT_BIT = 1 << 0
PAGE_SIZE_BIT = 1 << 7
NX_BIT = 1 << 63


class PageTableEntry:
	def __init__(self, gpa, val, nx):
		self.gpa = gpa
		self.val = val
		self.nx = nx
		self.size = val.total_size if isinstance(val, PageTable) else 1


class PageTable:
	def __init__(self, base, level):
		self.base = base
		self.level = level
		self.entries = []
		self.size = 0
		self.total_size = 0
	
	def add(self, entry):
		self.entries.append(entry)
		self.size += 1
		self.total_size += entry.size


def align(addr):
	return addr & (~0xfff)


def read_word(f, offset):
	f.seek(offset)
	raw = f.read(WORD_SIZE)[::-1]
	return raw


def build_pagetable(f, page_ind, lvl, page_table_page, data_page, page_table_entry):
	page_ind = align(page_ind)
	page_table_page.add(page_ind)
	result = PageTable(page_ind, lvl)
	for i in range(PAGE_SIZE // WORD_SIZE):
		offset = page_ind + i * WORD_SIZE
		f.seek(offset)
		data = int.from_bytes(f.read(WORD_SIZE)[::-1], "big")
		nx = True if data & NX_BIT != 0 else False
		present = True if data & PRESENT_BIT != 0 else False
		size_big = True if data & PAGE_SIZE_BIT != 0 else False
		
		data &= ~NX_BIT
		if data != 0 and present:
			page_table_entry.add(offset)
			if lvl > 1:
				if lvl == 2 and size_big:
					entry = PageTableEntry(offset, data, nx)
					data_page.add(align(data))
				elif data < 512 * 2 ** 20:
					val = build_pagetable(f, data, lvl-1, page_table_page, data_page, page_table_entry)
					entry = PageTableEntry(offset, val, nx)
				else:
					entry = PageTableEntry(offset, data, nx)
					data_page.add(align(data))
			else:
				entry = PageTableEntry(offset, data, nx)
				data_page.add(align(data))
			result.add(entry)

	return result


def print_pagetable(pt: PageTable):
	print(f"Page Table level {pt.level} base: {hex(pt.base)} size: {pt.size} total: {pt.total_size}")
	for entry in pt.entries:
		if type(entry.val) == int:
			pass#print("\t\t" * (5-pt.level) + f"{hex(entry.gpa)} - {hex(entry.val)}")
		else:
			print("\t\t" * (5-pt.level) + f"{hex(entry.gpa)}", end='')
			print("\n" + "\t\t" * (5-pt.level), end="")
			print_pagetable(entry.val)


def run(cr3_path, pmem_path, log_path, verbose=False):
	result = {}
	with open(pmem_path, 'rb') as pmem:
		with open(cr3_path, 'r') as cr3_file:
			for cr3 in cr3_file.readlines():
				page_table_page = set()
				data_page = set()
				page_table_entry = set()

				cr3 = int(cr3.strip(), 16)
				result_page = build_pagetable(pmem, align(cr3), 4, page_table_page, data_page, page_table_entry)
				result[hex(cr3)] = result_page

				if verbose:
					orig_stdout = sys.stdout
					f = open(f"{log_path}{hex(cr3)}", 'w')
					sys.stdout = f

					print(f"total page table page: {len(page_table_page)}")
					print(f"total data page: {len(data_page)}")
					print(f"total pte: {len(page_table_entry)}")
					print_pagetable(result_page)

					sys.stdout = orig_stdout
					f.close()
	return result

if __name__ == "__main__":
	run('/home/arcuser/serverless/qemu-memory-simulate/qemu-monitor/file/cr3', '/home/arcuser/serverless/qemu-memory-simulate/qemu-monitor/file/pmem', "/home/arcuser/serverless/qemu-memory-simulate/qemu-monitor/table/", verbose=True)