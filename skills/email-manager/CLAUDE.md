# Email Manager - Source Code Location

## Source Code

The email-manager binary is built from Go source code located at:

**~/projects/new/email-manager/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/email-manager
```

The compiled binary will be created at:
`~/projects/new/email-manager/email-manager`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/email-manager/email-manager ~/.claude/skills/email-manager/scripts/
```

## Binary Usage

All commands are accessed via:

```bash
~/.claude/skills/email-manager/scripts/email-manager [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
email-manager --help
email-manager [command] --help
```

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

## Development Workflow

1. Make changes to source files in `~/projects/new/email-manager/src/`
2. Build: `make -C ~/projects/new/email-manager`
3. Test the binary: `~/projects/new/email-manager/email-manager --help`
4. Deploy to skill: `cp ~/projects/new/email-manager/email-manager ~/.claude/skills/email-manager/scripts/`
