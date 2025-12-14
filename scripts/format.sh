#!/usr/bin/env bash

DATETIME="[ $(date '+%Y-%m-%d %H:%M:%S') ]";

read hook_info;
file_path="$(echo "$hook_info" | sed -E 's/.*"file_path" *: *"([^"]*)".*/\1/')";

if echo "$file_path" | grep -q "[.]py$"; then
    echo "$DATETIME Formatting Python file $file_path" >> $HOME/.logs/format.log;
    black -l 120 "$file_path";
else
    echo "$DATETIME Skipping formatting for non-Python file: $file_path" >> $HOME/.logs/format.log;
fi;
