# Google Docs Manager - Source Code Location

## Source Code

The google-docs-manager binary is built from Go source code located at:

**~/projects/new/google-docs-manager/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/google-docs-manager
```

The compiled binary will be created at:
`~/projects/new/google-docs-manager/google-docs-manager`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/google-docs-manager/google-docs-manager ~/.claude/skills/google-docs-manager/scripts/
```

## Binary Usage

All commands are accessed via:

```bash
~/.claude/skills/google-docs-manager/scripts/google-docs-manager [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
google-docs-manager --help
google-docs-manager [command] --help
```

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

## Development Workflow

1. Make changes to source files in `~/projects/new/google-docs-manager/src/`
2. Build: `make -C ~/projects/new/google-docs-manager`
3. Test the binary: `~/projects/new/google-docs-manager/google-docs-manager --help`
4. Deploy to skill: `cp ~/projects/new/google-docs-manager/google-docs-manager ~/.claude/skills/google-docs-manager/scripts/`
