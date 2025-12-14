#!/bin/bash

# Read Claude Code session data
input=$(cat)

# Get current working directory from Claude input
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')

# Function to get git branch
get_git_branch() {
    local branch
    if [ -d "$cwd/.git" ] || git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
        branch=$(git -C "$cwd" branch 2>/dev/null | awk '$0 ~ /^[*]/ {gsub("^[*] ",""); print $0}')
        if [ -n "$branch" ]; then
            echo "$branch"
        else
            echo "main"
        fi
    else
        echo "no-git"
    fi
}

# Function to get gcloud user
get_gcloud_user() {
    local account=$(gcloud config get-value account 2>/dev/null)
    # Remove @loreal.com suffix if present
    account="${account%@loreal.com}"
    echo "${account:-unknown}"
}

# Function to get gcloud project
get_gcloud_project() {
    local project=$(gcloud config get-value project 2>/dev/null)
    echo "${project:-unknown}"
}

# Function to format path with ~ for home directory
format_path() {
    local path="$1"
    local home_dir="/Users/$(whoami)"
    # Replace home directory with ~
    if [[ "$path" == "$home_dir"* ]]; then
        echo "~${path#$home_dir}"
    else
        echo "$path"
    fi
}

# Color definitions
CYAN='\033[1;36m'      # Bright cyan for brackets and parentheses
WHITE='\033[1;97m'     # Bright white
YELLOW='\033[1;93m'    # Bright yellow for date/time
MAGENTA='\033[1;35m'   # Bright magenta for @ and :
GREEN='\033[1;32m'     # Bright green for gcloud user
BLUE='\033[1;34m'      # Bright blue for gcloud project
RED='\033[1;31m'       # Bright red for path
PURPLE='\033[0;35m'    # Purple for git branch
RESET='\033[0m'        # Reset color

# Build the colorful status line
# Format: [DATE TIME] @<GCLOUD USER>:<GCLOUD PROJECT> <CURRENT_PATH> (<CURRENT GIT BRANCH>)
printf "${RESET}${CYAN}[${YELLOW}%s %s${CYAN}]${RESET} ${MAGENTA}@${GREEN}%s${MAGENTA}:${BLUE}%s${RESET} ${RED}%s${RESET} ${CYAN}(${PURPLE}%s${CYAN})${RESET}" \
    "$(date '+%Y-%m-%d')" \
    "$(date '+%H:%M:%S')" \
    "$(get_gcloud_user)" \
    "$(get_gcloud_project)" \
    "$(format_path "$cwd")" \
    "$(get_git_branch)"
