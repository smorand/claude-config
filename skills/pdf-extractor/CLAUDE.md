# PDF Extractor - Source Code Location

## Source Code

The pdf-extractor binary is built from Go source code located at:

**~/projects/new/pdf-extractor/**

## Building the Binary

To rebuild the binary after making changes to the source:

```bash
make -C ~/projects/new/pdf-extractor
```

The compiled binary will be created at:
`~/projects/new/pdf-extractor/pdf-extractor`

## Installation to Skill

After building, copy the binary to the skill's scripts directory:

```bash
cp ~/projects/new/pdf-extractor/pdf-extractor ~/.claude/skills/pdf-extractor/scripts/
```

## Binary Usage

All commands are accessed via:

```bash
~/.claude/skills/pdf-extractor/scripts/pdf-extractor [command] [args...]
```

Use `--help` with any command to see detailed usage:

```bash
pdf-extractor --help
pdf-extractor [command] --help
```

## Development Workflow

1. Make changes to source files in `~/projects/new/pdf-extractor/src/`
2. Build: `make -C ~/projects/new/pdf-extractor`
3. Test the binary: `~/projects/new/pdf-extractor/pdf-extractor --help`
4. Deploy to skill: `cp ~/projects/new/pdf-extractor/pdf-extractor ~/.claude/skills/pdf-extractor/scripts/`
