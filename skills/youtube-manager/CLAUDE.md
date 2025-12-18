# YouTube Manager - Binary-Based Skill

## Overview

This skill uses a pre-compiled Go binary instead of Python scripts. The binary is self-contained with no external dependencies (except yt-dlp for downloads).

## Source Code

The youtube-manager binary is built from Go source code located at:

**~/projects/new/youtube-manager/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/youtube-manager
```

The compiled binary will be created at:
`~/projects/new/youtube-manager/youtube-manager`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/youtube-manager/youtube-manager ~/.claude/skills/youtube-manager/scripts/
```

## Binary Usage

All commands are accessed via the binary:

```bash
~/.claude/skills/youtube-manager/scripts/youtube-manager [command] [args...]
```

Available commands:
- `list-playlists` - List your YouTube playlists
- `get-playlist` - Get videos from a playlist
- `download` - Download a YouTube video using yt-dlp
- `search` - Search for videos on YouTube
- `get-video` - Get detailed information about a video
- `create-playlist` - Create a new playlist
- `delete-playlist` - Delete a playlist
- `add-to-playlist` - Add a video to a playlist

Use `--help` with any command to see detailed usage:

```bash
youtube-manager --help
youtube-manager [command] --help
```

## Authentication

The binary uses OAuth2 credentials stored at:
- **Credentials:** `~/.credentials/google_credentials.json`
- **Token:** `~/.credentials/google_token.json`

First run will open a browser for OAuth consent. Token is automatically refreshed when expired.

## External Dependencies

- **yt-dlp:** Required for video downloads. Must be installed separately on the system.

## Development Workflow

1. Make changes to source files in `~/projects/new/youtube-manager/`
2. Build: `make -C ~/projects/new/youtube-manager`
3. Test the binary: `~/projects/new/youtube-manager/youtube-manager --help`
4. Deploy to skill: `cp ~/projects/new/youtube-manager/youtube-manager ~/.claude/skills/youtube-manager/scripts/`

## Advantages of Binary Approach

- **No dependencies:** Self-contained executable with all Go libraries compiled in
- **Fast execution:** No virtual environment setup or interpreter overhead
- **Simple deployment:** Single file to copy/distribute
- **Cross-platform:** Can compile for different OS/architectures
- **No version conflicts:** No Python version or package dependency issues
