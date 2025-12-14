# Script Usage & Arguments

Complete guide to using the `run.sh` script for PDF extraction.

## Script Location

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh
```

## Basic Syntax

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor <input_pdf> [output_dir] [--cleanup] [--project PROJECT_ID] [--region REGION]
```

## Parameters

### Required Parameters

#### `input_pdf` (required)
- **Type:** String (file path)
- **Description:** Full absolute path to the PDF file to extract
- **Must be:** Absolute path or path starting with `~/`
- **Examples:**
  ```bash
  /Users/sebastien.morand/Downloads/document.pdf
  ~/Downloads/report.pdf
  ~/Documents/presentation.pdf
  ```

### Optional Parameters

#### `output_dir` (optional)
- **Type:** String (directory path)
- **Description:** Base directory where output folder will be created
- **Behavior:** PDF name will be appended as subfolder
- **Default:** Same directory as input PDF
- **Examples:**
  ```bash
  ~/Documents/extracted
  ~/analysis
  /tmp/pdf_extracts
  ```

#### `--cleanup` (flag)
- **Type:** Boolean flag
- **Description:** Delete output directory after displaying content
- **Use case:** Temporary analysis without keeping files
- **Default:** false (keep files)

#### `--project` (optional)
- **Type:** String
- **Description:** GCP project ID for Vertex AI billing
- **Overrides:** gcloud config and GCP_PROJECT_ID environment variable
- **Example:**
  ```bash
  --project my-gcp-project-123
  ```

#### `--region` (optional)
- **Type:** String
- **Description:** GCP region for Vertex AI API
- **Default:** europe-west1
- **Common values:**
  - `europe-west1` (Belgium) - Default, fastest for EU
  - `us-central1` (Iowa) - US central
  - `us-east1` (South Carolina) - US east
  - `asia-southeast1` (Singapore) - Asia
- **Example:**
  ```bash
  --region us-central1
  ```

## Usage Examples

### Basic Extraction

Extract PDF to default location (same directory as PDF):

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf
```

**Result:**
- Input: `~/Downloads/report.pdf`
- Output: `~/Downloads/report/`

### Custom Output Directory

Extract to specific base directory:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/document.pdf ~/Documents/extracted
```

**Result:**
- Input: `~/Downloads/document.pdf`
- Output: `~/Documents/extracted/document/`

### Temporary Analysis with Cleanup

Extract, analyze, and automatically delete:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/temp.pdf --cleanup
```

**Result:**
- Content displayed
- Output directory deleted after completion

### Custom GCP Configuration

Extract with specific GCP project and region:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc.pdf --project my-project --region us-central1
```

**Result:**
- Uses specified project for Vertex AI billing
- Uses US central region for API calls

### Combined Parameters

All parameters together:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf ~/analysis --cleanup --project my-project --region europe-west1
```

**Result:**
- Input: `~/Downloads/report.pdf`
- Output: `~/analysis/report/` (temporary)
- Uses specified project and region
- Deleted after analysis

## Path Requirements

### ⚠️ CRITICAL: Use Full Paths

**Always use absolute paths or paths starting with `~/`:**

✅ **CORRECT:**
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/document.pdf
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor /Users/sebastien.morand/Documents/file.pdf
```

❌ **INCORRECT:**
```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ./document.pdf
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ../Downloads/file.pdf
```

**Why:** The Python script runs in a different working directory. Relative paths will fail with "File not found" errors.

## Output Path Behavior

### Default Path (No output_dir)

When no output directory is specified:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor /path/to/myfile.pdf
```

**Output:** `/path/to/myfile/` (folder named after PDF in same directory)

### Custom Path (With output_dir)

When output directory is specified:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor /path/to/myfile.pdf /target/
```

**Output:** `/target/myfile/` (PDF name appended as subfolder)

### Examples

| Input PDF | Output Dir | Final Output |
|-----------|------------|--------------|
| `~/Downloads/report.pdf` | (none) | `~/Downloads/report/` |
| `~/Downloads/report.pdf` | `~/Documents/extracted` | `~/Documents/extracted/report/` |
| `~/docs/q4.pdf` | (none) | `~/docs/q4/` |
| `~/docs/q4.pdf` | `~/analysis` | `~/analysis/q4/` |

## Script Output

### Console Output Structure

The script provides structured output:

```
📄 Extracting: /Users/user/Downloads/presentation.pdf
📁 Output to: /Users/user/Downloads/presentation

🔍 Analyzing images with LLM...
   Analyzing 1/3: image-0-0.png
   Analyzing 2/3: image-1-0.png
   Analyzing 3/3: image-2-0.png
✅ Image catalog created: /Users/user/Downloads/presentation/images.md

📄 PDF: presentation
📁 Output directory: /Users/user/Downloads/presentation
📝 Markdown file: /Users/user/Downloads/presentation/document.md
🖼️  Images catalog: /Users/user/Downloads/presentation/images.md
🖼️  Images extracted: 3
   Image files:
   - image-0-0.png
   - image-1-0.png
   - image-2-0.png

================================================================================
EXTRACTED CONTENT:
================================================================================
[Full markdown content displayed here]
================================================================================
```

### Summary Information

The script always provides:
- PDF filename
- Output directory location
- Markdown file path
- Images catalog path
- Number of images extracted
- List of image files

### File Output

Three types of files created:
1. **document.md** - Full text content with image references
2. **images.md** - AI-generated image catalog
3. **image-*.png** - Extracted images

## Batch Processing Examples

### Process All PDFs in Directory

```bash
for pdf in ~/Downloads/*.pdf; do
    echo "Processing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf"
done
```

**Result:** Each PDF extracted to folder in same directory

### Process with Custom Output

```bash
for pdf in ~/Downloads/*.pdf; do
    echo "Processing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" ~/analysis
done
```

**Result:** All extractions organized under `~/analysis/`

### Temporary Batch Analysis

```bash
for pdf in ~/Downloads/*.pdf; do
    echo "Analyzing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" --cleanup > "/tmp/$(basename "$pdf" .pdf).txt"
done
```

**Result:** Analysis saved to text files, no PDF extractions kept

## Environment Variables

The script respects these environment variables:

### GCP_PROJECT_ID
- **Description:** Default GCP project for Vertex AI
- **Overridden by:** `--project` argument
- **Example:**
  ```bash
  export GCP_PROJECT_ID="my-project-123"
  ```

### GCP_REGION
- **Description:** Default GCP region for Vertex AI
- **Default:** europe-west1
- **Overridden by:** `--region` argument
- **Example:**
  ```bash
  export GCP_REGION="us-central1"
  ```

## How the Script Works

### Execution Flow

1. **Validation:**
   - Check input PDF path exists
   - Validate parameters
   - Check gcloud authentication

2. **Environment Setup (First Run Only):**
   - Create `.venv` virtual environment using `uv`
   - Install dependencies: `pymupdf4llm`, `anthropic[vertex]`
   - Takes ~10-30 seconds on first run

3. **Extraction:**
   - Create output directory (PDF name folder)
   - Extract text content to `document.md`
   - Extract images to `image-*.png` files

4. **AI Analysis:**
   - Analyze each image using Claude via Vertex AI
   - Classify image type (chart, diagram, photo, etc.)
   - Detect text presence
   - Generate 2-3 sentence description
   - Create `images.md` catalog

5. **Output:**
   - Display summary information
   - Show full extracted content
   - Optionally cleanup if `--cleanup` flag used

### Dependencies Managed by uv

The script uses `uv` for dependency management:

```toml
[project]
dependencies = [
    "pymupdf4llm>=0.0.17",
    "anthropic[vertex]>=0.39.0",
]
```

**No manual installation required** - `uv` handles everything automatically.

## Error Handling

The script handles common errors gracefully:

### File Not Found
```
Error: PDF file not found: /path/to/file.pdf
```
**Solution:** Verify file path, use absolute path

### Authentication Error
```
Error: GCP authentication failed
```
**Solution:** Run `gcloud auth application-default login`

### API Error
```
Warning: Image analysis failed for image-0-0.png
```
**Solution:** Check network, verify Vertex AI API enabled, check project permissions

### Permission Denied
```
Error: Permission denied: /path/to/output
```
**Solution:** Check write permissions on output directory

## Performance Considerations

### Execution Time

- **First run:** 10-30 seconds (dependency installation)
- **Subsequent runs:** Near instant startup
- **Image analysis:** ~1-2 seconds per image
- **Text extraction:** Very fast (< 1 second for most PDFs)

**Example:** 10-page PDF with 5 images
- Setup: 0 seconds (after first run)
- Text extraction: < 1 second
- Image analysis: ~5-10 seconds
- **Total:** ~6-11 seconds

### Cost Considerations

- **Vertex AI API:** Billed to your GCP project
- **Claude Haiku model:** Low-cost, fast inference
- **Typical cost:** Fractions of a cent per image
- **Region:** europe-west1 default (may vary by region)

### Optimization Tips

1. **Use cleanup flag** for temporary analysis (saves disk space)
2. **Batch process** multiple PDFs in sequence
3. **Choose nearby region** for faster API calls
4. **Monitor API costs** in GCP console for large batches
