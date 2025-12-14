# Audio Recorder Skill

## Overview

The Audio Recorder skill enables Claude to manage audio recordings using sox. It provides simple start/stop/status commands for capturing audio from meetings and conversations, with intelligent PID tracking to ensure only one recording at a time.

## What This Skill Does

### Core Capabilities

1. **Start Recording**: Captures audio from the default microphone and saves to OGG format
2. **Stop Recording**: Cleanly terminates the active recording
3. **Check Status**: Shows detailed information about the current recording including label, duration, and file size

### Key Features

- **Single Recording Enforcement**: Only one recording active at a time via PID file tracking
- **Automatic Stop-and-Replace**: Starting a new recording automatically stops any running recording
- **Descriptive Labels**: Custom labels for easy identification (e.g., "one2one_Marcelo", "SteeringCommittee")
- **Detailed Status**: Extract label, start time, duration, and file size from running recording
- **Clean Shutdown**: Uses SIGINT for proper file finalization
- **Stale PID Cleanup**: Automatically detects and cleans up crashed processes

## Recording Format

- **File Format**: OGG (Vorbis)
- **Filename Pattern**: `YYYY-mm-dd_HH:MM:SS_<label>.ogg`
- **Storage Location**: `~/Downloads/Records/`
- **Quality**: Default sox settings (optimized for voice)

## Usage Examples

### Start Recording with Label
```
User: Start recording one2one with Jean
Claude: Recording started: 2025-11-11_15:30:22_one2one_with_Jean.ogg
        PID: 12345
```

### Start Recording without Label
```
User: Start recording
Claude: Recording started: 2025-11-11_15:30:22_Unknown.ogg
        PID: 12345
```

### Check Recording Status
```
User: What am I recording?
Claude: ✓ Recording in progress (PID: 12345)

        Label: one2one Jean
        Started: 2025-11-11 at 15:30:22
        Duration: 15m 32s

        Full path: ~/Downloads/Records/2025-11-11_15:30:22_one2one_Jean.ogg
        Current size: 2.3M
```

### Stop Recording
```
User: Stop recording
Claude: Stopping recording (PID: 12345)...
        Recording stopped successfully
```

## How It Works

### PID File Tracking

The skill maintains a PID file at `~/Downloads/Records/.pid` that stores the process ID of the active sox recording. This ensures:

1. Only one recording runs at a time
2. Status can be checked by reading the PID
3. Recordings can be cleanly stopped
4. Stale processes are detected and cleaned up

### Label Sanitization

Labels are automatically made filesystem-safe by:
- Converting spaces to underscores
- Removing special characters
- Preserving alphanumeric characters, underscores, and hyphens

Examples:
- `"one2one Jean"` → `one2one_Jean`
- `"Team Meeting - Q4"` → `Team_Meeting_-_Q4`
- `"Steering Committee (Nov)"` → `Steering_Committee_Nov`

### Status Information Extraction

When checking status, the skill:
1. Reads the PID from the PID file
2. Uses `ps -p PID -o command=` to get the full sox command
3. Extracts the filename from the command
4. Parses the timestamp and label from the filename
5. Calculates duration (current time - start time)
6. Shows the file size

This provides complete visibility into the active recording without requiring any additional tracking files.

## Automatic Behaviors

### Stop-and-Replace

When you start a new recording while one is already running:
1. The old recording is automatically stopped cleanly
2. The PID file is removed
3. The new recording starts
4. A new PID is saved

This is intentional - you never need to manually stop before starting a new recording.

### Stale PID Cleanup

If the sox process crashes or is killed externally:
1. The PID file becomes "stale" (contains PID of non-existent process)
2. The skill detects this automatically
3. The stale PID file is removed
4. Operations proceed normally

## Integration with Other Skills

### With Topic Manager

Record a meeting and then add it to a topic:
```
User: Start recording one2one Jean
[... meeting happens ...]
User: Stop recording
User: Update my one 2 one with Jean topic using this recording
```

### With Speech-to-Text

Record and then transcribe:
```
User: Start recording team standup
[... standup happens ...]
User: Stop recording
User: Transcribe the latest recording
```

## Script Location

The recording functionality is implemented in:
`/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh`

**Direct Usage**:
```bash
# Start recording
record.sh start [label]

# Stop recording
record.sh stop

# Check status
record.sh status
```

## Requirements

### Software Dependencies

- **sox**: Audio recording tool
  - Install: `brew install sox` (macOS)
  - Verify: `sox --version`

### System Permissions

- **Microphone Access**: macOS requires granting microphone permissions to the terminal/application running the script
  - System Preferences → Security & Privacy → Privacy → Microphone

### Disk Space

- Ensure sufficient space in `~/Downloads/Records/`
- Typical file size: ~150 KB per minute of audio

## Common Workflows

### 1. Quick Meeting Recording

```
User: Record team sync
[... meeting happens ...]
User: Done
```

### 2. Labeled Recording with Status Check

```
User: Start recording one2one Marcelo
User: Am I recording?
Claude: [shows detailed status]
[... meeting continues ...]
User: Stop recording
```

### 3. Replace Existing Recording

```
User: Am I recording?
Claude: Yes, recording "old meeting" for 90m
User: Start recording new meeting
Claude: [stops old, starts new automatically]
```

### 4. Record and Process

```
User: Record steering committee
[... meeting happens ...]
User: Stop recording
User: Update the Steering Committee topic with this recording
```

## File Organization

All recordings are stored in:
```
~/Downloads/Records/
├── 2025-11-11_09:00:15_team_standup.ogg
├── 2025-11-11_14:30:45_one2one_Marcelo.ogg
├── 2025-11-11_16:15:10_steering_committee.ogg
└── .pid (when recording active)
```

### Best Practices

1. **Always provide descriptive labels**: Makes files easier to find and manage
2. **Check status if unsure**: Use "am I recording?" to verify state
3. **Move completed recordings**: Transfer to appropriate topic folders after recording
4. **Regular cleanup**: Archive or delete old recordings periodically
5. **Monitor disk space**: OGG files grow over time (~150 KB/min)

## Troubleshooting

### Sox Not Found

**Error**: `sox: command not found`
**Solution**: Install sox: `brew install sox`

### Microphone Permission Denied

**Error**: `Cannot open audio device`
**Solution**: Grant microphone permissions in System Preferences → Security & Privacy → Privacy → Microphone

### Recording Won't Stop

**Error**: Process doesn't respond to SIGINT
**Solution**: The script automatically force-kills (SIGKILL) after 5 seconds

### Stale PID File

**Status**: `No recording in progress (stale PID file)`
**Solution**: The script automatically cleans this up on next operation

## Skill Activation

This skill activates when you mention:
- "record", "recording"
- "start recording", "begin recording"
- "stop recording", "end recording"
- "recording status", "am I recording", "what am I recording"
- "record [meeting name]"
- "record one2one with [person]"
