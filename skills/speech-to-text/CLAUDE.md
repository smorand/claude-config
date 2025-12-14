# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Speech-to-text transcription skill for audio/video files using VertexAI Gemini 2.5 Flash. Generates meeting minutes with speaker identification and attendee detection.

**Implementation:** Go binary (single executable, no dependencies or environment setup required)

## Critical Requirements

### 1. No Environment Variables Required

**The Go binary has a default project built-in (`oa-data-btdpexploration-np`).**

You can optionally override it with the `-project` flag if needed:
```bash
~/.claude/skills/speech-to-text/scripts/speech-to-text audio.mp3 -project my-custom-project
```

### 2. Always Use Absolute Paths

**ALWAYS use full/absolute paths for audio files for reliability.**

✅ Correct:
```bash
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/Downloads/meeting.mp3
~/.claude/skills/speech-to-text/scripts/speech-to-text /Users/sebastien.morand/Downloads/audio.wav
```

✅ Also works (relative paths):
```bash
~/.claude/skills/speech-to-text/scripts/speech-to-text meeting.mp3  # If in same directory
```

**Recommendation:** Use absolute paths for clarity and to avoid confusion.

### 3. Never Run Transcriptions in Parallel

**CRITICAL: Always process files sequentially, one at a time.**

✅ Correct (sequential):
```bash
for audio in ~/Downloads/*.mp3; do
    ~/.claude/skills/speech-to-text/scripts/run.sh speech_to_text "$audio" > "${audio%.mp3}_transcript.md"
    # Wait for completion before next file
done
```

❌ Wrong (parallel):
```bash
for audio in ~/Downloads/*.mp3; do
    ~/.claude/skills/speech-to-text/scripts/run.sh speech_to_text "$audio" > "${audio%.mp3}_transcript.md" &
done
wait
```

**Why:** Parallel processing hits VertexAI API rate limits and will fail.

## Running Transcriptions

### Basic Usage

```bash
# Transcribe audio file (output to stdout)
~/.claude/skills/speech-to-text/scripts/speech-to-text /path/to/audio.mp3

# Save output to file
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/Downloads/meeting.mp3 -o transcript.md

# With custom meeting name
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/Downloads/meeting.mp3 -m "Weekly Team Sync"

# With custom GCP region (optional, default: global)
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/audio.wav -location europe-west1

# With custom project
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/audio.wav -project my-gcp-project
```

### Performance

- **Startup:** Instant (compiled Go binary, no dependencies to load)
- **Processing time:** Up to 20 minutes for long recordings (Gemini 2.5 Flash processing)
- **Automatic chunking:** Files >30 minutes are split into 30-minute chunks with overlaps

## Architecture

### Go Binary Implementation

The skill uses a compiled Go binary with no external dependencies:

1. **Single executable** - No Python, no virtual environment, no package installation
2. **Built-in defaults** - Default GCP project is compiled into the binary
3. **Fast startup** - Instant execution (no import overhead)
4. **Self-contained** - All dependencies compiled into the binary

### Key Files

- `scripts/speech-to-text` - Compiled Go binary (single executable)
- `main.go` - Go source code for transcription
- `go.mod` / `go.sum` - Go dependencies
- `build.sh` - Build script to compile the binary
- `SKILL.md` - Detailed skill documentation
- `README.md` - Comprehensive usage guide
- `CLAUDE.md` - This file (AI interaction guidelines)

## Output Format

The transcription generates 2 clean sections:

1. **Attendees:** List of identified speaker names (extracted from conversation)
2. **Minutes:** Verbatim transcription with speaker attribution using actual names

## Command-Line Flags

| Flag | Required | Default | Description |
|----------|----------|---------|-------------|
| `<audio-file>` | **Yes** | - | Path to audio file (positional argument) |
| `-o` | No | stdout | Output markdown file path |
| `-m` | No | filename | Custom meeting name for title |
| `-project` | No | `oa-data-btdpexploration-np` | GCP project with VertexAI enabled |
| `-location` | No | `global` | GCP region for VertexAI |
| `-model` | No | `gemini-2.5-flash` | Gemini model to use |

## Supported Audio Formats

MP3, WAV, M4A, FLAC, OGG, AAC

MIME types are auto-detected based on file extension.

## Prerequisites

- **ffmpeg** - Audio processing (for chunking files >30 minutes)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
- **GCP Authentication:** `gcloud auth application-default login`
- **VertexAI API enabled:** `gcloud services enable aiplatform.googleapis.com --project=oa-data-btdpexploration-np`

## Common Workflows

### Locate and Transcribe Audio from Downloads

```bash
# Find audio files
find ~/Downloads -name "*.mp3" -o -name "*.m4a" | grep -i "meeting"

# Transcribe to file
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/Downloads/meeting-recording.mp3 -o transcript.md
```

### Extract Specific Sections

```bash
# Get attendees list only
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/audio.mp3 | grep -A 10 "## Attendees"

# Get minutes only
~/.claude/skills/speech-to-text/scripts/speech-to-text ~/audio.mp3 | grep -A 100 "## Minutes"
```

### Process Multiple Files Sequentially

```bash
for audio in ~/Downloads/*.mp3; do
    echo "Processing: $audio"
    ~/.claude/skills/speech-to-text/scripts/speech-to-text "$audio" -o "${audio%.mp3}_transcript.md"
    # Each transcription completes before next starts
done
```

## Troubleshooting

**ERROR: Audio file not found**
- Use absolute paths for reliability
- Verify file exists: `ls -lh /full/path/to/audio.mp3`

**Failed to initialize VertexAI / Authentication errors**
- Re-authenticate: `gcloud auth application-default login`
- Enable API: `gcloud services enable aiplatform.googleapis.com --project=oa-data-btdpexploration-np`

**ffmpeg not found**
- Install on macOS: `brew install ffmpeg`
- Install on Linux: `sudo apt-get install ffmpeg`

**Rate limit errors (429)**
- Wait a few minutes before retrying
- Process files sequentially, not in parallel

## Model Information

**Default Model:** Gemini 2.5 Flash (`gemini-2.5-flash`)
- Multimodal (audio + text)
- Auto-detects language
- Optimized for speed and cost-effectiveness
- Best for meeting transcriptions with speaker identification

**Alternative Models:**
- `gemini-2.5-pro` - Higher accuracy, slower, more expensive
- Specify with `-model` flag if needed
