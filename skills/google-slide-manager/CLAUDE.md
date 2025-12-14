# Google Slide Manager - Source Code Location

## Source Code

The google-slide-manager binary is built from Go source code located at:

**~/projects/new/google-slide-manager/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/google-slide-manager
```

The compiled binary will be created at:
`~/projects/new/google-slide-manager/google-slide-manager`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/google-slide-manager/google-slide-manager ~/.claude/skills/google-slide-manager/scripts/
```

## Binary Usage

All commands are accessed via:

```bash
~/.claude/skills/google-slide-manager/scripts/google-slide-manager [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
google-slide-manager --help
google-slide-manager create-presentation --help
google-slide-manager add-slide --help
```

## Available Commands

- `create-presentation` - Create new presentation
- `add-slide` - Add slide to presentation
- `remove-slide` - Remove a slide
- `move-slide` - Move slide to new position
- `duplicate-slide` - Duplicate a slide
- `reorder-slides` - Reorder slides
- `add-shape` - Add shapes (RECTANGLE, ELLIPSE, etc.)
- `create-table` - Create tables
- `update-cell` - Update table cell content
- `style-cell` - Style table cells
- `add-notes` - Add speaker notes
- `get-notes` - Get speaker notes
- `extract-all-notes` - Extract all notes
- `extract-all-text` - Extract all text
- `search-text` - Search for text
- `replace-text` - Find and replace text
- `copy-text-style` - Copy text styling
- `copy-theme` - Copy theme between presentations
- `translate-slides` - Translate to target language
- `export-pdf` - Export as PDF
- `export-pptx` - Export as PowerPoint

## Authentication

The binary uses OAuth2 credentials stored at:
- Credentials: `~/.credentials/google_credentials.json`
- Token: `~/.credentials/google_token.json`

## Development Workflow

1. Make changes to source files in `~/projects/new/google-slide-manager/src/`
2. Build: `make -C ~/projects/new/google-slide-manager`
3. Test the binary: `~/projects/new/google-slide-manager/google-slide-manager --help`
4. Deploy to skill: `cp ~/projects/new/google-slide-manager/google-slide-manager ~/.claude/skills/google-slide-manager/scripts/`
