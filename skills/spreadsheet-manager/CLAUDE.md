# Spreadsheet Manager - Source Code Location

## Source Code

The spreadsheet-manager binary is built from Go source code located at:

**~/projects/new/spreadsheet-manager/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/spreadsheet-manager
```

The compiled binary will be created at:
`~/projects/new/spreadsheet-manager/spreadsheet-manager`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/spreadsheet-manager/spreadsheet-manager ~/.claude/skills/spreadsheet-manager/scripts/
```

## Source Structure

```
~/projects/new/spreadsheet-manager/
├── src/
│   ├── main.go      - Entry point, command registration
│   ├── cli.go       - All command definitions and implementations
│   ├── auth.go      - OAuth2 authentication logic
│   ├── helpers.go   - Utility functions (A1 notation, colors, etc.)
│   ├── go.mod       - Module definition
│   └── go.sum       - Dependency checksums
├── Makefile         - Build targets
├── README.md        - User documentation
└── CLAUDE.md        - AI documentation
```

## Development Workflow

1. Make changes to source files in `~/projects/new/spreadsheet-manager/src/`
2. Build: `make -C ~/projects/new/spreadsheet-manager`
3. Test the binary: `~/projects/new/spreadsheet-manager/spreadsheet-manager --help`
4. Deploy to skill: `cp ~/projects/new/spreadsheet-manager/spreadsheet-manager ~/.claude/skills/spreadsheet-manager/scripts/`

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

Note: The skill documentation references `~/.claude/credentials/` but the binary uses `~/.credentials/`.
