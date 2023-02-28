#!/bin/bash

dir="/sys/kernel/debug/tracing/"

if [ $1 -eq 0 ]
then
	echo 0 > $dir/tracing_on	
else if [ $1 -eq 1 ]
then
	echo 1 > $dir/tracing_on
else if [ $1 -eq 2 ]
then
	echo "pid filter set"
	echo 1 > $dir/tracing_on
	eval python3 pid_filter.py
fi
fi
fi
