# YouTube Manager - Source Code Location

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

All commands are accessed via:

```bash
~/.claude/skills/youtube-manager/scripts/youtube-manager [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
youtube-manager --help
youtube-manager [command] --help
```

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

## Development Workflow

1. Make changes to source files in `~/projects/new/youtube-manager/src/`
2. Build: `make -C ~/projects/new/youtube-manager`
3. Test the binary: `~/projects/new/youtube-manager/youtube-manager --help`
4. Deploy to skill: `cp ~/projects/new/youtube-manager/youtube-manager ~/.claude/skills/youtube-manager/scripts/`
