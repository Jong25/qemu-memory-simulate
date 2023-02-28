#!/bin/bash

target="/sys/kernel/debug/tracing/current_tracer"
tracer=( "function" "function_graph" )
echo ${tracer[$1]} > $target

if [ $1 -eq 0 ]
then
	echo "current tracer: function"
else
	if [ $1 -eq 1 ]
	then
		echo "current tracer: function_graph"
	fi
fi
