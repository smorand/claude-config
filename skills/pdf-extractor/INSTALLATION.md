# PDF Extractor Skill - Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip or uv package manager

## Installation Steps

### 1. Install Python Package

Choose one of the following methods:

#### Using pip (standard)
```bash
pip install pymupdf4llm
```

#### Using pip3 (if pip defaults to Python 2)
```bash
pip3 install pymupdf4llm
```

#### Using uv (recommended for L'Oréal projects)
```bash
uv pip install pymupdf4llm
```

### 2. Verify Installation

```bash
python3 -c "import pymupdf4llm; print('pymupdf4llm installed successfully')"
```

Expected output:
```
pymupdf4llm installed successfully
```

### 3. Test the Script

```bash
python3 ~/.claude/scripts/pdf_extractor.py
```

Expected output (help message):
```
Usage: python pdf_extractor.py <pdf_file> [output_directory] [--cleanup]

Arguments:
  pdf_file           Path to the PDF file to extract
  output_directory   Optional: Directory to save extracted content
                     (default: creates temp directory)
  --cleanup          Optional: Clean up extraction directory after reading

Examples:
  python pdf_extractor.py document.pdf
  python pdf_extractor.py document.pdf ./output
  python pdf_extractor.py document.pdf --cleanup
  python pdf_extractor.py document.pdf ./output --cleanup
```

## Troubleshooting

### "No module named 'pymupdf4llm'"

This means the package is not installed. Run:
```bash
pip install pymupdf4llm
```

### "pip: command not found"

Try using pip3:
```bash
pip3 install pymupdf4llm
```

### "Permission denied"

Install for user only:
```bash
pip install --user pymupdf4llm
```

Or use sudo (not recommended):
```bash
sudo pip install pymupdf4llm
```

### Virtual Environment Issues

If using a virtual environment:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Then install
pip install pymupdf4llm
```

## Package Information

- **Package name:** pymupdf4llm
- **Description:** Convert PDF documents to markdown for LLM processing
- **Dependencies:** PyMuPDF (automatically installed)
- **License:** AGPL-3.0

## Next Steps

After installation:

1. Try extracting a sample PDF:
   ```bash
   python3 ~/.claude/scripts/pdf_extractor.py ~/Downloads/sample.pdf --cleanup
   ```

2. Read the skill documentation:
   ```bash
   cat ~/.claude/skills/pdf-extractor/SKILL.md
   ```

3. Use in Claude Code conversations by mentioning PDFs you want to analyze

## Support

For issues:
- Check Python version: `python3 --version`
- Verify pip installation: `pip3 --version`
- Update pip: `pip3 install --upgrade pip`
- Reinstall package: `pip3 install --force-reinstall pymupdf4llm`
