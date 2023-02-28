#!/bin/bash

QEMU_BIN=/home/arcuser/serverless/qemu-virtiofs-main/build/x86_64-softmmu/qemu-system-x86_64
DISK_PATH=/home/arcuser/serverless/qemu-memory-simulate/disk-img/img
KERNEL_IMG=/usr/src/serverless-dedup-host-kernel-main/arch/x86_64/boot/bzImage
INITRD_PATH=/boot/initrd.img-5.4.0
DISK_ISO=/home/arcuser/serverless/qemu-memory-simulate/disk-img/ubuntu-20.04.5-live-server-amd64.iso
TRACE=/home/arcuser/serverless/qemu-memory-simulate/disk-img/trace_functions

IMG=( "guest0.qcow2" "guest1.qcow2" )
debug_flag=""
img_ind=0
graphic_flag="-nographic"
trace_flag=""
monitor_flag=""

while getopts di:gtm: flag
do
	case "${flag}" in
		d) debug_flag="-s -S";;
		i) img_ind=${OPTARG};;
		g) graphic_flag="";;
		t) trace_flag='--trace events=$TRACE';;
		m) monitor_flag="-monitor telnet:127.0.0.1:${OPTARG},server,nowait";;
	esac
done

if [ "$debug_flag" != "" ];
then
	echo "running in debug mode..."
fi
sudo $QEMU_BIN \
		-m 512M \
		-smp 1 \
		-enable-kvm \
		-cpu host \
		-drive if=virtio,file=$DISK_PATH/${IMG[$img_ind]},format=qcow2 \
		-kernel $KERNEL_IMG \
		-initrd $INITRD_PATH \
		-append "root=/dev/vda2 console=ttyS0 earlyprintk=ttyS0 ftrace_dump_on_oops nokaslr" \
		$monitor_flag \
		$graphic_flag \
		$debug_flag \
		$trace_flag \
#		-cdrom $DISK_ISO \