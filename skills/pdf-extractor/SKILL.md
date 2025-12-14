---
name: pdf-extractor
description: Expert in PDF content extraction and analysis. **Use whenever the user mentions PDFs, .pdf files, or requests to extract, read, parse, analyze, convert, or process PDF documents.** Handles text extraction, image extraction, converting PDFs to markdown or other formats, batch PDF processing, and analyzing PDF document structure for AI processing. Supports two methods - preferred script-based extraction (default) and alternative image-based extraction (when explicitly requested). (project, gitignored)
---

# PDF Extractor Skill

You are an expert in extracting and analyzing PDF content, converting it to AI-friendly formats with intelligent image analysis and classification.

**Two extraction methods available:**
- **Method 1 (Preferred):** Script-based extraction to markdown with AI image analysis
- **Method 2 (Alternative):** Page-by-page image conversion for complex layouts (only when explicitly requested)

## ⚠️ CRITICAL REQUIREMENT: ALWAYS USE FULL FILE PATHS

**YOU MUST ALWAYS use absolute/full paths when working with PDF files.**

✅ **CORRECT:**
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor /Users/sebastien.morand/Downloads/document.pdf
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf ~/Documents/extracted
```

❌ **INCORRECT:**
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ./document.pdf
```

**Why:** The Python script runs in a different working directory than your current shell. Relative paths will fail. Always use full absolute paths or paths starting with `~/` for the input PDF file.

## Extraction Methods

This skill supports **two methods** for extracting information from PDFs:

### Method 1: Script-Based Extraction (PREFERRED ✅)

**This is the default and recommended method.**

Uses the `pdf_extractor` script to:
- Extract text with layout preservation to markdown
- Extract embedded images from the PDF
- Analyze images with AI-powered descriptions and classifications
- Generate an intelligent images catalog (images.md)

**When to use:** All standard PDF extraction tasks (default behavior)

**How to use:** Simply ask to "extract PDF", "analyze PDF", "read PDF", etc.

### Method 2: Image-Based Extraction (ALTERNATIVE)

Converts entire PDF pages to images using ImageMagick, then analyzes each page as an image.

**When to use:**
- Complex layouts that don't extract well as text
- Scanned documents or image-heavy PDFs
- When visual layout/formatting is critical
- When explicitly requested by user

**How to trigger:** User must explicitly request:
- "extract information from PDF using image mode"
- "extract PDF information through images"
- "convert PDF to images and analyze"
- "analyze PDF as images page by page"

**Process:**
1. Convert PDF to PNG images (one per page) using ImageMagick: `magick convert -density 150 input.pdf output-%03d.png`
2. Use Task tool to analyze each image page with Claude's vision capabilities
3. Combine analysis from all pages

⚠️ **Note:** Image-based extraction is slower and more expensive (vision API calls per page) but preserves exact visual layout.

## Core Capabilities (Method 1)

- PDF text extraction with layout preservation
- AI-powered image analysis and classification using Claude via Vertex AI
- Automatic image description generation with type detection (photo, diagram, chart, table, banner, logo, etc.)
- Intelligent images catalog (images.md) with detailed metadata
- Markdown conversion with embedded image references
- Multi-page PDF processing
- Smart default output paths based on PDF filename
- Optional cleanup for temporary extractions

## Quick Start

### Basic Usage

**Location:** `~/.claude/skills/pdf-extractor/scripts/run.sh`

```bash
# Basic extraction (creates folder in PDF's directory)
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor /path/to/document.pdf

# Extract to specific base directory
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf ~/Documents/extracted

# Temporary analysis with automatic cleanup
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/temp.pdf --cleanup

# Custom GCP project and region
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc.pdf --project my-project --region europe-west1
```

### Default Output Paths

**When no output directory specified:**
- PDF: `/path/to/myfile.pdf`
- Output: `/path/to/myfile/` (same directory as PDF)

**When custom output directory specified:**
- PDF: `/path/to/myfile.pdf`
- Custom output: `/target/`
- Final output: `/target/myfile/` (PDF name appended)

**Examples:**
```bash
# Extract /Downloads/report.pdf → Output: ~/Downloads/report/
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf

# Extract to custom location → Output: ~/Documents/extracted/report/
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf ~/Documents/extracted
```

### Output Structure

Every extraction creates:
```
pdf_name/
├── document.md       # Extracted text content with image references
├── images.md         # AI-generated image catalog with descriptions
└── image-*.png       # Extracted images
```

## Common Workflows

### 1. Summarize PDF with Image Context

```bash
# Extract with AI image analysis
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf

# Read content
cat ~/Downloads/report/document.md    # Text content
cat ~/Downloads/report/images.md      # Image descriptions
```

**Process:** Extract → Read document.md → Review images.md → Filter relevant images → Combine for comprehensive summary

### 2. Filter Images by Type

```bash
# Extract PDF
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/presentation.pdf

# Find charts and diagrams only
grep -A 15 "**Type:** chart" ~/Downloads/presentation/images.md
grep -A 15 "**Type:** diagram" ~/Downloads/presentation/images.md

# Exclude decorative elements
grep -v "banner\|logo" ~/Downloads/presentation/images.md
```

### 3. Batch Process Multiple PDFs

```bash
# Process all PDFs in directory
for pdf in ~/Downloads/*.pdf; do
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf"
done
```

### 4. Temporary Analysis

```bash
# Quick analysis without keeping files
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/temp.pdf --cleanup
```

See [references/workflows.md](references/workflows.md) for more detailed workflows.

## Script Details

### How It Works

The script uses `uv` to:
- Automatically create isolated virtual environment (`.venv`)
- Install dependencies: `pymupdf4llm` (PDF extraction) and `anthropic[vertex]` (AI image analysis)
- Execute with complete isolation from system packages
- Use gcloud authentication for Vertex AI access
- No manual setup required

### Available Arguments

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor <input_pdf> [output_dir] [--cleanup] [--project PROJECT_ID] [--region REGION]
```

**Parameters:**
- `input_pdf` (required): Full path to PDF file
- `output_dir` (optional): Base directory for output (PDF name will be appended)
- `--cleanup`: Delete output directory after displaying content
- `--project`: GCP project ID (overrides gcloud config/env var)
- `--region`: GCP region for Vertex AI (default: europe-west1)

See [references/script-usage.md](references/script-usage.md) for detailed script usage and examples.

## Image Catalog (images.md)

The script automatically generates an `images.md` file with AI-powered analysis.

**For each image:**
- **Path:** Relative path to image file
- **Type:** Classification (photo, diagram, chart, graph, table, screenshot, banner, logo, icon, illustration, map, or other)
- **Contains Text:** Whether image has readable text
- **Description:** AI-generated 2-3 sentence description
- **Preview:** Embedded image for reference

**Benefits:**
- Filter out banners, logos, decorative images
- Understand charts/diagrams without viewing
- Find specific images by type or description
- Provides accessibility descriptions

See [references/output-format.md](references/output-format.md) for complete output format details.

## Prerequisites & Setup

### Required
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **gcloud CLI** - Google Cloud SDK
- **GCP project** with Vertex AI API enabled

### Authentication Setup

**Quick Setup:**
```bash
# 1. Install gcloud CLI (macOS)
brew install google-cloud-sdk

# 2. Authenticate
gcloud auth application-default login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

**Optional environment variables:**
```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="europe-west1"
```

See [references/authentication.md](references/authentication.md) for detailed authentication setup and troubleshooting.

## Response Approach

When helping with PDF extraction:

1. **Determine method:**
   - **Default:** Use Method 1 (script-based extraction) unless user explicitly requests image mode
   - **Image mode:** Only use Method 2 if user explicitly asks for "image mode", "through images", "as images page by page", etc.
2. **Understand task:** What information needed? Are images important? Filter decorative images?
3. **Locate PDF:** Check mentioned locations, search common directories
4. **Extract content:**
   - **Method 1:** Use pdf_extractor script with appropriate options (cleanup vs. permanent)
   - **Method 2:** Convert to images with ImageMagick, then analyze with Task tool
5. **Process:**
   - **Method 1:** Read document.md and images.md, filter images by type if needed
   - **Method 2:** Combine analysis from all page images
6. **Provide results:** Summarize findings, highlight relevant visuals, suggest next steps
7. **Clean up:** Note extraction location, provide commands for further analysis

## Performance & Best Practices

**Performance:**
- Image analysis: ~1-2 seconds per image via Vertex AI API
- First run: ~10-30 seconds to install dependencies
- API costs: Uses Vertex AI credits (billed to GCP project)
- Default region: europe-west1 (faster for EU users)

**When to use default path:** Single documents, permanent archives, files organized alongside PDFs

**When to use custom output_dir:** Multiple extractions, analysis projects, separating source and processed files

**When to use --cleanup:** Temporary analysis, limited disk space, batch processing, content stored elsewhere

See [references/advanced.md](references/advanced.md) for customization, performance tuning, and integration details.

## Troubleshooting

### Common Issues

**"PDF file not found":**
```bash
ls -lh /path/to/file.pdf
find ~ -name "*.pdf" -type f | grep -i "filename"
```

**Authentication errors:**
```bash
gcloud auth application-default print-access-token
gcloud auth application-default login  # If needed
```

**Dependencies issues:**
```bash
cd ~/.claude/skills/pdf-extractor/scripts
rm -rf .venv  # Force reinstall
```

See [references/authentication.md](references/authentication.md) for detailed troubleshooting.

## Reference Documentation

- [Script Usage & Arguments](references/script-usage.md) - Complete run.sh usage with examples
- [Output Format](references/output-format.md) - Output structure, images.md format, file organization
- [Workflows](references/workflows.md) - Common workflows and use cases
- [Authentication](references/authentication.md) - GCP/Vertex AI setup and troubleshooting
- [Advanced Usage](references/advanced.md) - Customization, performance, integration
