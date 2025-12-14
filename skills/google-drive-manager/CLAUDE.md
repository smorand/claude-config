# Google Drive Manager - Source Code Location

## Source Code

The gdrive binary is built from Go source code located at:

**~/projects/new/gdrive/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/gdrive
```

The compiled binary will be created at:
`~/projects/new/gdrive/gdrive`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/gdrive/gdrive ~/.claude/skills/google-drive-manager/scripts/
```

## Binary Usage

All commands are accessed via:

```bash
~/.claude/skills/google-drive-manager/scripts/gdrive [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
gdrive --help
gdrive [command] --help
```

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

## Development Workflow

1. Make changes to source files in `~/projects/new/gdrive/src/`
2. Build: `make -C ~/projects/new/gdrive`
3. Test the binary: `~/projects/new/gdrive/gdrive --help`
4. Deploy to skill: `cp ~/projects/new/gdrive/gdrive ~/.claude/skills/google-drive-manager/scripts/`
