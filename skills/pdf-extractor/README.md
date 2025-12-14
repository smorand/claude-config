# PDF Extractor Skill

Expert skill for extracting and analyzing PDF content with AI-powered processing.

## Overview

This skill enables seamless PDF content extraction, converting documents to AI-friendly markdown format with embedded images. It's designed to work efficiently with Claude Code for analyzing documents, answering questions, and extracting specific information.

## Quick Start

### Prerequisites

- **uv** - Python package manager (https://docs.astral.sh/uv/)
- No other manual installation required!

### Basic Usage

```bash
# Extract PDF to temp directory with auto-cleanup
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf --cleanup

# Extract to specific directory (permanent)
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf ./output

# Extract with cleanup to specific directory
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf ./output --cleanup
```

**First run:** May take a few seconds to create the virtual environment and install dependencies. Subsequent runs are instant!

## Features

- ✅ Text extraction with layout preservation
- ✅ Automatic image extraction from PDFs
- ✅ Markdown conversion with embedded image references
- ✅ Temporary extraction with automatic cleanup
- ✅ Multi-page PDF processing
- ✅ Batch processing support
- ✅ **Isolated virtual environment** (no system package conflicts)
- ✅ **Zero manual setup** (dependencies auto-installed)
- ✅ Integration with Claude Code workflow

## How It Works

The skill uses a modern, isolated approach:

1. **run.sh** - Generic script runner that takes script name as first argument
2. **uv** - Automatically creates `.venv` and installs dependencies from `pyproject.toml`
3. **Isolation** - Completely independent from system Python packages
4. **Scalable** - Easy to add more scripts to the same skill

## File Structure

```
~/.claude/skills/pdf-extractor/
├── README.md                    # This file
├── SKILL.md                     # Detailed skill guide
├── INSTALLATION.md              # Installation instructions
└── scripts/
    ├── run.sh                   # Generic script runner
    ├── pyproject.toml           # Python dependencies
    ├── .venv/                   # Auto-created virtual environment
    ├── uv.lock                  # Dependency lock file
    └── src/
        └── pdf_extractor.py     # Python extraction script
```

## Use Cases

### 1. Document Analysis
Extract and analyze reports, presentations, or documentation:
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor quarterly_report.pdf --cleanup
```

### 2. Information Extraction
Find specific data, dates, or metrics from PDFs:
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor invoice.pdf ./extracted
grep "Total Amount" ./extracted/document.md
```

### 3. Content Summarization
Extract content for AI summarization:
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor meeting_notes.pdf --cleanup
# Content is displayed and can be summarized by Claude
```

### 4. Format Conversion
Convert PDF to markdown and other formats:
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf ./output
pandoc ./output/document.md -o document.docx
```

## Output Structure

When you extract a PDF, you get:

```
output_directory/
├── document.md                   # Markdown with full content
├── image-0-0.png                # Extracted images
├── image-1-0.png
└── ...
```

The markdown file contains the full text with image references like `![image](image-0-0.png)`.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `script_name` | Yes | Name of the Python script (e.g., `pdf_extractor`) |
| `pdf_file` | Yes | Path to the PDF file to extract |
| `output_directory` | No | Directory to save extracted content (default: temp dir) |
| `--cleanup` | No | Automatically clean up extraction directory after reading |

## Configuration

The script uses these default settings:
- **Image format:** PNG
- **DPI:** 150
- **Encoding:** UTF-8

To customize, edit `~/.claude/skills/pdf-extractor/scripts/src/pdf_extractor.py` and modify the `to_markdown()` parameters.

## Examples

### Extract and analyze
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor report.pdf --cleanup
```

### Extract and preserve
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor presentation.pdf ./my_analysis
```

### Batch processing
```bash
for pdf in *.pdf; do
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" "./extracted/$(basename "$pdf" .pdf)"
done
```

### Extract and search
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor doc.pdf ./output
grep -i "keyword" ./output/document.md -C 3
```

## Integration with Claude Code

When using this skill in Claude Code conversations:

1. **Mention a PDF:** "Analyze the report.pdf in my Downloads"
2. **Automatic extraction:** Script runs in background
3. **Content available:** Claude reads and analyzes the markdown
4. **Answer questions:** Based on extracted content
5. **Clean up:** Automatic if --cleanup is used

## Troubleshooting

### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with homebrew
brew install uv
```

### PDF file not found
```bash
# Verify file path
ls -lh /path/to/file.pdf

# Search for file
find ~ -name "*.pdf" | grep -i "filename"
```

### Permission denied on run.sh
```bash
# Make script executable
chmod +x ~/.claude/skills/pdf-extractor/scripts/run.sh
```

### Poor extraction quality
- Try increasing DPI in script (change `dpi=150` to `dpi=300`)
- For scanned PDFs, consider OCR preprocessing
- Complex layouts may need manual review

### Virtual environment issues
```bash
# Remove and recreate .venv
rm -rf ~/.claude/skills/pdf-extractor/scripts/.venv
# Next run will recreate it automatically
```

## Dependencies

- **uv** - Python package manager (auto-installs Python and dependencies)
- **pymupdf4llm** - Automatically installed by uv on first run

## Adding More Scripts

To add a new script to this skill:

1. Create `scripts/src/my_new_script.py`
2. Add dependencies to `scripts/pyproject.toml`
3. Run with: `scripts/run.sh my_new_script [args...]`

The same `.venv` and dependencies are shared across all scripts in the skill.

## See Also

- Full skill documentation: `SKILL.md`
- Installation guide: `INSTALLATION.md`
- Related skills: `speech-to-text`, `video-creator`, `skill-creator`

## Support

For issues or questions:
1. Check `SKILL.md` for detailed documentation
2. Review troubleshooting section above
3. Ensure uv is installed
4. Check file paths and permissions
