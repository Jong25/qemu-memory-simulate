#!/bin/bash

dir="/sys/kernel/debug/tracing"

target=( "tracing_on" "current_tracer" "set_ftrace_filter" "set_event_pid" "set_ftrace_pid" )

for t in ${target[@]}
do
	echo $t:
	eval cat $dir/$t
done
