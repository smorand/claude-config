#!/bin/bash
# Audio Recording Script
# Manages audio recording using sox with PID tracking

set -euo pipefail

RECORDS_DIR="$HOME/Downloads/Records"
PID_FILE="$RECORDS_DIR/.pid"

# Ensure records directory exists
mkdir -p "$RECORDS_DIR"

# Function to stop running recording cleanly
stop_recording() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")

        # Check if process is actually running
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "Stopping recording (PID: $pid)..."
            kill -SIGINT "$pid" 2>/dev/null || true

            # Wait for process to terminate (max 5 seconds)
            local count=0
            while ps -p "$pid" > /dev/null 2>&1 && [ $count -lt 50 ]; do
                sleep 0.1
                count=$((count + 1))
            done

            if ps -p "$pid" > /dev/null 2>&1; then
                echo "Warning: Process did not stop cleanly, forcing..."
                kill -9 "$pid" 2>/dev/null || true
            else
                echo "Recording stopped successfully"
            fi
        else
            echo "PID file exists but process not running (cleaning up stale PID)"
        fi

        # Remove PID file
        rm -f "$PID_FILE"
    else
        echo "No recording in progress"
    fi
}

# Function to rename active recording
rename_recording() {
    local new_label="${1:-}"

    if [ -z "$new_label" ]; then
        echo "Error: New label is required"
        exit 1
    fi

    if [ ! -f "$PID_FILE" ]; then
        echo "Error: No recording in progress"
        exit 1
    fi

    local pid=$(cat "$PID_FILE")

    # Check if process is actually running
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "Error: No recording in progress (stale PID file)"
        rm -f "$PID_FILE"
        exit 1
    fi

    # Get the current filename from the process command line
    cmdline=$(ps -p "$pid" -o command= 2>/dev/null || echo "")
    current_file=$(echo "$cmdline" | grep -o "$RECORDS_DIR/[^ ]*\.ogg" || echo "")

    if [ -z "$current_file" ] || [ ! -f "$current_file" ]; then
        echo "Error: Could not find current recording file"
        exit 1
    fi

    # Extract timestamp from current filename
    basename_file=$(basename "$current_file")
    if [[ "$basename_file" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2})_(.+)\.ogg$ ]]; then
        timestamp="${BASH_REMATCH[1]}"
    else
        echo "Error: Could not parse timestamp from filename"
        exit 1
    fi

    # Sanitize new label
    new_label=$(echo "$new_label" | tr ' ' '_' | tr -cd '[:alnum:]_-')

    # Build new filename with same timestamp
    new_file="$RECORDS_DIR/${timestamp}_${new_label}.ogg"

    # Rename the file (mv works even if file is being written to)
    mv "$current_file" "$new_file"

    echo "Recording renamed successfully"
    echo "Old: $(basename "$current_file")"
    echo "New: $(basename "$new_file")"
    echo ""
    echo "Note: Recording continues uninterrupted (PID: $pid)"
}

# Function to start recording
start_recording() {
    # Stop eventual current record
    stop_recording

    local label="${1:-Unknown}"

    # Generate timestamp
    local timestamp=$(date +"%Y-%m-%d_%H:%M:%S")

    # Sanitize label (replace spaces and special chars with underscores)
    label=$(echo "$label" | tr ' ' '_' | tr -cd '[:alnum:]_-')

    # Build filename
    local filename="$RECORDS_DIR/${timestamp}_${label}.ogg"

    echo "Starting recording: $filename"

    # Start sox in background (redirect output to avoid clutter)
    sox -d "$filename" > /dev/null 2>&1 &
    local new_pid=$!

    # Save PID
    echo "$new_pid" > "$PID_FILE"

    echo "Recording started (PID: $new_pid)"
    echo "File: $filename"
}

# Main logic
case "${1:-}" in
    start)
        # Check if recording already running
        if [ -f "$PID_FILE" ]; then
            pid=$(cat "$PID_FILE")
            if ps -p "$pid" > /dev/null 2>&1; then
                echo "Existing recording detected, stopping it first..."
                stop_recording
                echo ""
            else
                echo "Stale PID file found, cleaning up..."
                rm -f "$PID_FILE"
            fi
        fi

        # Start new recording with label (if provided)
        label="${2:-Unknown}"
        start_recording "$label"
        ;;

    stop)
        stop_recording
        ;;

    rename)
        # Rename recording with new label
        new_label="${2:-}"
        if [ -z "$new_label" ]; then
            echo "Error: New label is required"
            echo "Usage: $0 rename <new_label>"
            exit 1
        fi
        rename_recording "$new_label"
        ;;

    status)
        if [ -f "$PID_FILE" ]; then
            pid=$(cat "$PID_FILE")
            if ps -p "$pid" > /dev/null 2>&1; then
                echo "✓ Recording in progress (PID: $pid)"
                echo ""

                # Get the full command from ps to extract filename
                cmdline=$(ps -p "$pid" -o command= 2>/dev/null || echo "")

                if [ -n "$cmdline" ]; then
                    # Extract filename from command (sox -d "filename")
                    recording_file=$(echo "$cmdline" | grep -o "$RECORDS_DIR/[^ ]*\.ogg" || echo "")

                    if [ -n "$recording_file" ]; then
                        # Extract basename for parsing
                        basename_file=$(basename "$recording_file")

                        # Extract timestamp and label from filename: YYYY-mm-dd_HH:MM:SS_label.ogg
                        if [[ "$basename_file" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2})_(.+)\.ogg$ ]]; then
                            timestamp="${BASH_REMATCH[1]}"
                            label="${BASH_REMATCH[2]}"

                            # Convert timestamp to more readable format
                            start_date=$(echo "$timestamp" | cut -d'_' -f1)
                            start_time=$(echo "$timestamp" | cut -d'_' -f2)

                            echo "Label: ${label//_/ }"
                            echo "Started: $start_date at $start_time"

                            # Calculate duration
                            if command -v gdate > /dev/null 2>&1; then
                                start_epoch=$(gdate -d "$start_date $start_time" +%s 2>/dev/null || echo "0")
                                current_epoch=$(gdate +%s)
                            else
                                start_epoch=$(date -j -f "%Y-%m-%d %H:%M:%S" "$start_date $start_time" +%s 2>/dev/null || echo "0")
                                current_epoch=$(date +%s)
                            fi

                            if [ "$start_epoch" != "0" ]; then
                                duration_seconds=$((current_epoch - start_epoch))
                                duration_minutes=$((duration_seconds / 60))
                                duration_remaining=$((duration_seconds % 60))

                                if [ $duration_minutes -gt 0 ]; then
                                    echo "Duration: ${duration_minutes}m ${duration_remaining}s"
                                else
                                    echo "Duration: ${duration_seconds}s"
                                fi
                            fi
                        else
                            echo "File: $basename_file"
                        fi

                        echo ""

                        # Check if file actually exists (may have been renamed)
                        if [ ! -f "$recording_file" ]; then
                            echo "Note: File was renamed, detecting new name..."
                            # Find the actual file by looking for .ogg files newer than PID file
                            actual_file=$(find "$RECORDS_DIR" -name "*.ogg" -newer "$PID_FILE" 2>/dev/null | head -1)
                            if [ -n "$actual_file" ]; then
                                recording_file="$actual_file"
                                basename_file=$(basename "$recording_file")
                                # Re-extract label from actual filename
                                if [[ "$basename_file" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2})_(.+)\.ogg$ ]]; then
                                    echo "Detected label: ${BASH_REMATCH[2]//_/ }"
                                fi
                            fi
                        fi

                        echo "Full path: $recording_file"

                        # Show file size
                        if [ -f "$recording_file" ]; then
                            size=$(du -h "$recording_file" | cut -f1)
                            echo "Current size: $size"
                        fi
                    else
                        # Fallback: try to find the file by timestamp
                        recording_file=$(find "$RECORDS_DIR" -name "*.ogg" -newer "$PID_FILE" 2>/dev/null | head -1)
                        if [ -n "$recording_file" ]; then
                            echo "File: $recording_file"
                            if [ -f "$recording_file" ]; then
                                size=$(du -h "$recording_file" | cut -f1)
                                echo "Size: $size"
                            fi
                        fi
                    fi
                fi
            else
                echo "✗ No recording in progress (stale PID file)"
            fi
        else
            echo "✗ No recording in progress"
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|rename|status} [label]"
        echo ""
        echo "Examples:"
        echo "  $0 start                    # Start recording with 'Unknown' label"
        echo "  $0 start one2one_Marcelo    # Start recording with custom label"
        echo "  $0 stop                     # Stop current recording"
        echo "  $0 rename Team_Meeting      # Rename active recording (does NOT stop it)"
        echo "  $0 status                   # Check recording status"
        exit 1
        ;;
esac
