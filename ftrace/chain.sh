#!/bin/bash

target="/sys/kernel/debug/tracing/set_ftrace_filter"
echo "*$1*" >> $target
sleep 1
echo "$1 <-"
eval cat "/sys/kernel/debug/tracing/trace" | grep "$1 <-"

