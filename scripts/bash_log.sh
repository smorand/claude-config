#!/bin/bash

# Bash command logging script for Claude Code
# Logs bash commands with structured format: [ DATETIME ] PATH: COMMAND

read CLAUDE_TOOL_INPUT;

# Get current timestamp
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')";

# Get current working directory
CURRENT_PATH="$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.cwd // "."')";

# Extract command from the tool input JSON
COMMAND="$(echo -e "$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.tool_input.description // "Unknown command"')\n$ $(echo "$CLAUDE_TOOL_INPUT" | jq -r '.tool_input.command // "No command provided"')")";

# Log format: [ DATETIME ] PATH: COMMAND
LOG_ENTRY="[ $TIMESTAMP ] $CURRENT_PATH: $COMMAND";

# Append to log file
echo "$LOG_ENTRY" >> ~/.claude/bash-command-log.txt;
