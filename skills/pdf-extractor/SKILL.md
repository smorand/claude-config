---
name: pdf-extractor
description: Expert in PDF content extraction and analysis. **Use whenever the user mentions PDFs, .pdf files, or requests to extract, read, parse, analyze, convert, or process PDF documents.** Handles text extraction, image extraction, converting PDFs to markdown or other formats, batch PDF processing, and analyzing PDF document structure for AI processing. Uses a fast Go binary with Vertex AI Gemini for intelligent image analysis. Supports two methods - preferred binary-based extraction (default) and alternative image-based extraction (when explicitly requested). (project, gitignored)
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
~/.claude/skills/pdf-extractor/scripts/pdf-extractor /Users/sebastien.morand/Downloads/document.pdf
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -output ~/Documents/extracted ~/Downloads/report.pdf
```

❌ **INCORRECT:**
```bash
~/.claude/skills/pdf-extractor/scripts/pdf-extractor document.pdf
~/.claude/skills/pdf-extractor/scripts/pdf-extractor ./document.pdf
```

**Why:** Always use full absolute paths or paths starting with `~/` for the input PDF file to ensure correct file resolution.

## Extraction Methods

This skill supports **two methods** for extracting information from PDFs:

### Method 1: Binary-Based Extraction (PREFERRED ✅)

**This is the default and recommended method.**

Uses the `pdf-extractor` Go binary to:
- Extract text with layout preservation to markdown
- Extract embedded images from the PDF
- Analyze images with AI-powered descriptions and classifications (via Vertex AI Gemini)
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

- PDF text extraction with layout preservation using Go-based pdfcpu library
- AI-powered image analysis and classification using Gemini 1.5 Flash via Vertex AI
- Automatic image description generation with type detection (photo, diagram, chart, table, banner, logo, etc.)
- Intelligent images catalog (images.md) with detailed metadata
- Markdown conversion with embedded image references
- Multi-page PDF processing
- Smart default output paths based on PDF filename
- Optional cleanup for temporary extractions
- Fast, standalone binary with no Python dependencies

## Quick Start

### Basic Usage

**Binary Location:** `~/.claude/skills/pdf-extractor/scripts/pdf-extractor`

```bash
# Basic extraction (creates folder in PDF's directory)
~/.claude/skills/pdf-extractor/scripts/pdf-extractor /path/to/document.pdf

# Extract to specific directory
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -output ~/Documents/extracted ~/Downloads/report.pdf

# Temporary analysis with automatic cleanup
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -cleanup ~/Downloads/temp.pdf

# Custom GCP project and region
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -project my-project -region europe-west1 ~/Downloads/doc.pdf

# Skip AI analysis (faster, no image descriptions)
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -no-ai ~/Downloads/doc.pdf

# Use different Gemini model
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -model gemini-1.5-pro ~/Downloads/doc.pdf
```

### Default Output Paths

**When no output directory specified:**
- PDF: `/path/to/myfile.pdf`
- Output: `/path/to/myfile_extraction/` (default suffix: `_extraction`)

**When custom output directory specified:**
- PDF: `/path/to/myfile.pdf`
- Custom output: `/target/`
- Final output: `/target/` (exact directory specified)

**Examples:**
```bash
# Extract ~/Downloads/report.pdf → Output: ~/Downloads/report_extraction/
~/.claude/skills/pdf-extractor/scripts/pdf-extractor ~/Downloads/report.pdf

# Extract to custom location → Output: ~/Documents/extracted/
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -output ~/Documents/extracted ~/Downloads/report.pdf
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
~/.claude/skills/pdf-extractor/scripts/pdf-extractor ~/Downloads/report.pdf

# Read content
cat ~/Downloads/report_extraction/document.md    # Text content
cat ~/Downloads/report_extraction/images.md      # Image descriptions
```

**Process:** Extract → Read document.md → Review images.md → Filter relevant images → Combine for comprehensive summary

### 2. Filter Images by Type

```bash
# Extract PDF
~/.claude/skills/pdf-extractor/scripts/pdf-extractor ~/Downloads/presentation.pdf

# Find charts and diagrams only
grep -A 15 "**Type:** chart" ~/Downloads/presentation_extraction/images.md
grep -A 15 "**Type:** diagram" ~/Downloads/presentation_extraction/images.md

# Exclude decorative elements
grep -v "banner\|logo" ~/Downloads/presentation_extraction/images.md
```

### 3. Batch Process Multiple PDFs

```bash
# Process all PDFs in directory
for pdf in ~/Downloads/*.pdf; do
    ~/.claude/skills/pdf-extractor/scripts/pdf-extractor "$pdf"
done
```

### 4. Temporary Analysis

```bash
# Quick analysis without keeping files
~/.claude/skills/pdf-extractor/scripts/pdf-extractor -cleanup ~/Downloads/temp.pdf
```

See [references/workflows.md](references/workflows.md) for more detailed workflows.

## Binary Details

### How It Works

The `pdf-extractor` is a standalone Go binary that:
- Extracts PDF text and images using the pdfcpu library
- Converts content to markdown format
- Uses Vertex AI Gemini API for AI-powered image analysis
- Authenticates via gcloud Application Default Credentials
- No dependencies or virtual environments required
- Fast execution with compiled Go performance

### Command-Line Arguments

```bash
pdf-extractor [OPTIONS] <pdf-file>
```

**Required:**
- `<pdf-file>`: Full path to the PDF file to process

**Options:**
- `-output string`: Output directory for extracted content (default: `pdf_name_extraction`)
- `-cleanup`: Delete extracted images after processing (keeps markdown files)
- `-no-ai`: Skip AI image analysis (faster, but no image descriptions)
- `-model string`: Vertex AI model to use (default: `gemini-1.5-flash`)
- `-project string`: GCP project ID for Vertex AI (default: `btdp-dta-gbl-0002-gen-ai-01`)
- `-region string`: GCP region for Vertex AI (default: `europe-west1`)

See [references/script-usage.md](references/script-usage.md) for detailed usage and examples.

## Image Catalog (images.md)

The binary automatically generates an `images.md` file with AI-powered analysis (unless `-no-ai` is used).

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
- **gcloud CLI** - Google Cloud SDK (for authentication)
- **GCP project** with Vertex AI API enabled
- No other dependencies - the binary is self-contained

### Authentication Setup

**Quick Setup:**
```bash
# 1. Install gcloud CLI (macOS)
brew install google-cloud-sdk

# 2. Authenticate with Application Default Credentials
gcloud auth application-default login

# 3. Set default project (optional - can override with -project flag)
gcloud config set project YOUR_PROJECT_ID

# 4. Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

**Override defaults via command-line flags:**
```bash
# Specify project and region at runtime
pdf-extractor -project my-project -region us-central1 ~/Downloads/file.pdf
```

See [references/authentication.md](references/authentication.md) for detailed authentication setup and troubleshooting.

## Response Approach

When helping with PDF extraction:

1. **Determine method:**
   - **Default:** Use Method 1 (binary-based extraction) unless user explicitly requests image mode
   - **Image mode:** Only use Method 2 if user explicitly asks for "image mode", "through images", "as images page by page", etc.
2. **Understand task:** What information needed? Are images important? Should AI analysis be skipped (-no-ai)?
3. **Locate PDF:** Check mentioned locations, search common directories
4. **Extract content:**
   - **Method 1:** Use pdf-extractor binary with appropriate flags (-cleanup, -no-ai, -output, etc.)
   - **Method 2:** Convert to images with ImageMagick, then analyze with Task tool
5. **Process:**
   - **Method 1:** Read document.md and images.md (if AI analysis was enabled), filter images by type if needed
   - **Method 2:** Combine analysis from all page images
6. **Provide results:** Summarize findings, highlight relevant visuals, suggest next steps
7. **Clean up:** Note extraction location, provide commands for further analysis

## Performance & Best Practices

**Performance:**
- Binary execution: Fast startup (no virtual environment setup)
- Text extraction: Very fast with compiled Go code
- Image analysis: ~1-2 seconds per image via Vertex AI Gemini API (when enabled)
- API costs: Uses Vertex AI credits (billed to GCP project)
- Default model: `gemini-1.5-flash` (fast and cost-effective)
- Alternative model: `gemini-1.5-pro` (higher quality, slower, more expensive)
- Default region: europe-west1 (optimized for EU users)

**When to use default output path:** Single documents, keeping extractions near source PDFs

**When to use -output flag:** Custom organization, multiple extractions, specific project directories

**When to use -cleanup flag:** Temporary analysis, limited disk space, only need text without images

**When to use -no-ai flag:** Fast extraction without image descriptions, cost savings, text-only analysis

See [references/advanced.md](references/advanced.md) for customization, performance tuning, and integration details.

## Troubleshooting

### Common Issues

**"PDF file not found":**
```bash
# Always use absolute paths
ls -lh ~/Downloads/file.pdf
# Find PDF files if location unknown
find ~ -name "*.pdf" -type f | grep -i "filename"
```

**Authentication errors:**
```bash
# Verify authentication
gcloud auth application-default print-access-token
# Re-authenticate if needed
gcloud auth application-default login
# Check current project
gcloud config get-value project
```

**Vertex AI API errors:**
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
# Verify project has access
gcloud projects describe YOUR_PROJECT_ID
```

**Binary permission issues:**
```bash
# Make binary executable
chmod +x ~/.claude/skills/pdf-extractor/scripts/pdf-extractor
```

See [references/authentication.md](references/authentication.md) for detailed troubleshooting.

## Reference Documentation

- [Binary Usage & Arguments](references/script-usage.md) - Complete binary usage with examples
- [Output Format](references/output-format.md) - Output structure, images.md format, file organization
- [Workflows](references/workflows.md) - Common workflows and use cases
- [Authentication](references/authentication.md) - GCP/Vertex AI setup and troubleshooting
- [Advanced Usage](references/advanced.md) - Performance tuning, model selection, integration

## Building from Source

The binary is built from Go source code located at `~/projects/new/pdf-extractor/`.

To rebuild after making changes:
```bash
# Build the binary
make -C ~/projects/new/pdf-extractor

# Deploy to skill directory
cp ~/projects/new/pdf-extractor/pdf-extractor ~/.claude/skills/pdf-extractor/scripts/
```

See [CLAUDE.md](CLAUDE.md) for complete development workflow.
