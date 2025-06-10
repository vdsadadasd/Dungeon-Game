#!/bin/bash
# Kill all afplay processes
killall afplay 2>/dev/null

# Find all bash processes running the music loop and kill their process groups
ps aux | grep '[b]ash -c trap "" SIGHUP; while true; do afplay' | awk '{print $2}' | while read pid; do
    # Kill the process group
    pgid=$(ps -o pgid= -p "$pid" | tr -d ' ')
    if [ -n "$pgid" ]; then
        kill -TERM -"$pgid" 2>/dev/null
    fi
done
