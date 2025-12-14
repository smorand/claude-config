---
name: google-docs-manager
description: Expert in Google Docs management. Use when creating, reading, updating, formatting, or managing Google Docs with markdown support, advanced formatting, tables with full manipulation, images with styling, lists, headers/footers, and table of contents.
---

# Google Docs Manager Skill

Expert in managing and editing Google Docs with comprehensive read/write/update operations, advanced formatting, styling, table of contents, images, and tables.

## Core Capabilities

### Document Management
- **Create & Read:** Create documents from template, read full or sections
- **Content Editing:** Insert, update, delete text with advanced formatting
- **Structure Navigation:** Get document structure, navigate by headings

### Advanced Text Formatting
- **Text Styles:** Bold, italic, underline, strikethrough
- **Colors:** Apply RGB colors to text
- **Font Size:** Change font size in points
- **Alignment:** Left (START), center, right (END), justified

### Lists
- **Bulleted Lists:** Multiple styles (disc, checkbox, arrow, diamond)
- **Numbered Lists:** Hierarchical numbering (1. a. i.)
- **Remove Lists:** Convert lists back to normal text

### Advanced Table Operations
- **Create Tables:** Insert formatted tables from CSV with legends
- **Modify Structure:** Add/delete rows and columns dynamically
- **Update Content:** Edit individual cell content
- **Style Cells:** Apply background colors and padding
- **Merge/Unmerge:** Create complex table layouts

### Advanced Image Features
- **Insert Images:** Add images with legends from URLs
- **Resize:** Control image width and height
- **Borders:** Add colored borders to images
- **Text Wrapping:** Control how text flows around images

### Document Structure
- **Headers & Footers:** Add custom headers/footers with page numbers
- **Table of Contents:** Auto-generate and update TOC
- **Markdown Support:** Convert markdown to Google Docs (utility)

## When to Use This Skill

Use this skill when users request:

### Basic Operations
- "Create a new Google Doc from the template"
- "Read the content of this document"
- "Update chapter 3 in the document"
- "Convert this markdown to a Google Doc"
- "Get the content of the 'Introduction' section"

### Advanced Formatting
- "Make this text bold and red"
- "Apply amber color (#bf9000) to this status text"
- "Make this text green (#38761d) and bold"
- "Add strikethrough to this paragraph"
- "Center align this section"
- "Change the font size to 14 points"
- "Apply underline formatting"

### Lists
- "Create a bulleted list with checkboxes"
- "Add numbered bullets to these items"
- "Convert this list back to normal text"

### Table Operations
- "Add a table with this data"
- "Add 3 more rows to the table"
- "Delete the second column"
- "Update cell B3 with new data"
- "Merge the header cells"
- "Make the header row gray"

### Image Operations
- "Insert this image with a caption"
- "Resize the image to 600x400"
- "Add a black border to the image"

### Document Structure
- "Add a header with the company name"
- "Add a footer with page numbers"
- "Update the table of contents"

## Available Tools

### Docs Manager Script

**Location:** `~/.claude/skills/google-docs-manager/scripts/`

**Structure:**
```
~/.claude/skills/google-docs-manager/scripts/
├── run.sh                     # Generic script runner
├── pyproject.toml             # Python dependencies
├── .venv/                     # Auto-created virtual environment
└── src/
    ├── docs_manager.py        # Main CLI script
    ├── auth.py                # Authentication module
    └── docs_operations.py     # Document operations module
```

**Usage:**

**Basic Document Operations:**
```bash
# Create from template (RECOMMENDED)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template <title> <folder_id>

# Read document (full content)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read <document_id>

# Read specific section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read-section <document_id> <heading_text>

# Get document structure (headings with indices)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager get-structure <document_id>

# Set content from markdown
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown <document_id> <markdown_file>

# Update section from markdown
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-section <document_id> <heading_text> <markdown_file>

# Insert after section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-after-section <document_id> <heading_text> <markdown_file>

# Get document info
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager info <document_id>
```

**Text Operations:**
```bash
# Delete text range
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager delete-text <document_id> <start_index> <end_index>

# Format text (bold, italic, underline, strikethrough, color, font-size)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text <document_id> <start_index> <end_index> \
    [--bold true] [--italic true] [--underline true] [--strikethrough true] \
    [--color "R,G,B"] [--font-size N]

# Color Format Details:
# --color accepts RGB values as comma-separated integers (0-255)
# Format: "R,G,B" where R=Red, G=Green, B=Blue
#
# Hex to RGB Conversion:
# To convert hex colors (e.g., #bf9000) to RGB:
# 1. Split hex into pairs: #bf9000 → bf, 90, 00
# 2. Convert each pair from hex to decimal:
#    - bf (hex) = 191 (decimal)
#    - 90 (hex) = 144 (decimal)
#    - 00 (hex) = 0 (decimal)
# 3. Result: "191,144,0"
#
# Common Colors:
# - Black: "0,0,0" (#000000)
# - White: "255,255,255" (#ffffff)
# - Red: "255,0,0" (#ff0000)
# - Green: "0,255,0" (#00ff00)
# - Blue: "0,0,255" (#0000ff)
# - Dark Red: "153,0,0" (#990000)
# - Dark Green: "56,118,29" (#38761d)
# - Amber/Orange: "191,144,0" (#bf9000)
#
# Examples:
# Apply amber color to text at indices 100-115:
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text DOC_ID 100 115 --color "191,144,0"
#
# Apply dark green with bold:
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text DOC_ID 200 210 --bold true --color "56,118,29"
#
# Apply black color (default):
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text DOC_ID 300 315 --color "0,0,0"

# Align paragraph
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager align-paragraph <document_id> <start_index> <end_index> <ALIGNMENT>
# ALIGNMENT: START (left), CENTER, END (right), JUSTIFIED
```

**List Operations:**
```bash
# Create bulleted list
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-bullets <document_id> <start_index> <end_index> [--style STYLE]
# STYLES: BULLET_DISC_CIRCLE_SQUARE (default), BULLET_CHECKBOX, BULLET_ARROW_DIAMOND_DISC, BULLET_DIAMONDX_ARROW3D_SQUARE

# Create numbered list
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-numbered <document_id> <start_index> <end_index>

# Remove bullets/numbering
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager remove-bullets <document_id> <start_index> <end_index>
```

**Table Operations:**
```bash
# Insert table from CSV
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table <document_id> <csv_file> [--legend LEGEND] [--index INDEX]

# Add rows
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager add-table-rows <document_id> <table_index> <num_rows> [--after-row N]

# Add columns
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager add-table-columns <document_id> <table_index> <num_columns> [--after-column N]

# Delete row
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager delete-table-row <document_id> <table_index> <row_index>

# Delete column
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager delete-table-column <document_id> <table_index> <column_index>

# Update cell content
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-table-cell <document_id> <table_index> <row_index> <column_index> "text"

# Style cell (background color, padding)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager style-table-cell <document_id> <table_index> <row_index> <column_index> \
    [--bg-color "R,G,B"] [--padding N]
# Note: --bg-color uses same RGB format as --color (see format-text color documentation above)
# Example: --bg-color "191,144,0" for amber (#bf9000)

# Merge cells
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager merge-table-cells <document_id> <table_index> \
    <row_start> <row_end> <col_start> <col_end>

# Unmerge cells
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager unmerge-table-cells <document_id> <table_index> <row_index> <column_index>
```

**Image Operations:**
```bash
# Insert image
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image <document_id> <image_url> [--legend LEGEND] [--index INDEX]

# Style image (resize, border, wrapping)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager style-image <document_id> <image_index> \
    [--width N] [--height N] [--wrap TYPE] [--border-width N] [--border-color "R,G,B"]
# WRAP TYPES: INLINE (default), WRAP_TEXT, BREAK_TEXT
# Note: --border-color uses same RGB format as --color (see format-text color documentation above)
```

**Headers & Footers:**
```bash
# Add/update header
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager add-header <document_id> "text" [--page-number]

# Add/update footer
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager add-footer <document_id> "text" [--page-number]
```

**Table of Contents:**
```bash
# Update table of contents
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc <document_id>
```

**Examples:**
```bash
# Create a new document from template
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Q4 Report" 1folderabc123

# Read full document
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read 1docabc123xyz

# Read specific chapter
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read-section 1docabc123xyz "Introduction"

# Get document structure
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager get-structure 1docabc123xyz

# Set content from markdown file
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown 1docabc123xyz content.md

# Update specific section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-section 1docabc123xyz "Methodology" methodology.md

# Insert table with legend
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table 1docabc123xyz data.csv --legend "Table 1: Sales Data Q4 2024"

# Insert image with legend
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image 1docabc123xyz "https://example.com/chart.png" --legend "Figure 1: Revenue Trends"

# Apply color formatting (convert hex #bf9000 to RGB 191,144,0)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text 1docabc123xyz 100 115 --color "191,144,0"

# Apply multiple formatting options (green + bold)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager format-text 1docabc123xyz 200 215 --bold true --color "56,118,29"

# Update table of contents
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc 1docabc123xyz
```

**How It Works:**
The `run.sh` script uses `uv` to:
- Automatically create an isolated virtual environment (`.venv`)
- Install dependencies from `pyproject.toml`
- Execute the Python script with complete isolation
- No manual installation or setup required

## Template Document

**Template URL:** https://docs.google.com/document/d/1lcUWzmqtj-h0OMdM_NcvDN_qa4EyAfwCgE-IZUAlLPc

This template includes pre-configured styles:
- **Title** style (for `# title`)
- **Heading 1** style (for `## chapter`)
- **Heading 2** style (for `### sub-chapter`)
- **Heading 3** style (for `#### sub-sub-chapter`)
- **Heading 4** style (for `##### sub-sub-sub-chapter`)
- **Heading 5** style (for `###### sub-sub-sub-sub-chapter`)

## Markdown to Google Docs Mapping

| Markdown | Google Docs Style |
|----------|------------------|
| `# title` | Title |
| `## Chapter` | Heading 1 |
| `### Sub Chapter` | Heading 2 |
| `#### Sub Sub Chapter` | Heading 3 |
| `##### Sub Sub Sub Chapter` | Heading 4 |
| `###### Sub Sub Sub Sub Chapter` | Heading 5 |
| Regular text | Normal Text |
| `**bold**` | Bold text |
| `*italic*` or `_italic_` | Italic text |
| Tables | Google Docs tables with italic legend above |
| Images | Inline images with italic legend below (left-aligned) |

**Note:** Italic formatting supports both asterisk (`*text*`) and underscore (`_text_`) syntax. This is particularly useful for scientific names and technical terms that conventionally use underscores in markdown (e.g., `_Chlamydophila pneumoniae_`).

## Operations

### 1. Create Document from Template
Creates a new document by copying the template and clearing its content, preserving styles.

**Process:**
1. Copy template document to destination folder
2. Clear all content (preserving styles)
3. Insert empty table of contents placeholder
4. Return new document ID

### 2. Read Document
Extract document content as markdown or plain text.

**Full Read:**
- Returns entire document content
- Preserves structure (headings, paragraphs, tables)
- Converts to markdown format

**Section Read:**
- Extracts content under specific heading
- Returns only the section content
- Preserves formatting

### 3. Get Document Structure
Returns hierarchical structure of document headings.

**Output:**
```json
{
  "headings": [
    {
      "level": 1,
      "text": "Introduction",
      "index": 15,
      "style": "HEADING_1"
    },
    {
      "level": 2,
      "text": "Background",
      "index": 45,
      "style": "HEADING_2"
    }
  ]
}
```

### 4. Set Content from Markdown (Utility)
**This is a utility function for markdown conversion. The primary focus of this skill is document editing.**

Replaces entire document content with markdown-formatted content.

**Markdown Conversion Process:**
1. Clear existing content
2. Parse markdown and convert to Google Docs API requests
3. Apply proper styles based on heading levels:
   - `# text` → Title style
   - `## text` → Heading 1 style
   - `### text` → Heading 2 style
   - `#### text` → Heading 3 style
   - `##### text` → Heading 4 style
   - `###### text` → Heading 5 style
   - Regular text → Normal Text style
   - `**bold**` → Bold formatting
   - `*italic*` or `_italic_` → Italic formatting (both syntaxes supported)
   - `- item` → Bullet point (Normal Text with dash)
4. Split requests into batches of 400 (Google Docs API limit)
5. Execute batch updates sequentially

**Important Notes:**
- Google Docs API has a limit of ~400 requests per batchUpdate call
- Large documents are automatically split into multiple batches
- Empty lines in markdown are skipped to avoid unwanted spacing
- Paragraphs flow continuously without extra blank lines
- After content insertion, always use `update-toc` to add automatic TOC
- Markdown conversion is a convenience feature; main purpose is document editing

### 5. Update Section
Updates content under a specific heading.

**Process:**
1. Find heading in document structure
2. Determine section boundaries
3. Replace section content with new markdown
4. Preserve surrounding content
5. Update table of contents

### 6. Insert Table
Inserts a formatted table with optional legend.

**Format:**
```
Table 1: Sales Data Q4 2024  (italic, above table)

┌────────────┬──────────┬──────────┐
│   Month    │  Sales   │  Growth  │
├────────────┼──────────┼──────────┤
│  October   │  $125k   │   +5%    │
│  November  │  $142k   │  +13%    │
│  December  │  $198k   │  +39%    │
└────────────┴──────────┴──────────┘
```

**Input:** CSV file or JSON data
**Output:** Google Docs table with legend

### 7. Insert Image
Inserts an image into the document with optional legend.

**CRITICAL LIMITATION - Google Docs API Requirements:**
Google Docs API ONLY accepts images via publicly accessible HTTP/HTTPS URLs. Local files CANNOT be inserted directly.

**Required Workflow for Local Images:**
1. **Upload to Google Drive:** Local image files must first be uploaded to Google Drive
2. **Make Publicly Accessible:** Set Drive file permissions to `type: anyone, role: reader`
3. **Get Drive URL:** Use format `https://drive.google.com/uc?export=view&id=FILE_ID`
4. **Insert into Document:** Use the Drive URL with insert-image command

**Alternative Approaches (NOT supported by API):**
- ❌ Base64 data URIs (API rejects with "URL should start with http:// or https://")
- ❌ Direct local file paths
- ❌ File system URLs (file://)

**Recommended Practice:**
- Upload images to the same Google Drive folder as the document
- This keeps all related content together in Google Workspace
- Images are accessible through proper Drive permissions
- No dependency on external hosting services

**Format:**
```
[Image]

Figure 1: Revenue Trends  (italic, below image, left-aligned)

[blank line automatically added after legend for spacing]
```

**Input:** Publicly accessible HTTP/HTTPS URL (typically from Google Drive)
**Output:** Inline image with legend and blank line after for proper spacing

**Example Workflow:**
```bash
# 1. Upload image to Drive
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload image.png --parent FOLDER_ID

# 2. Make public (using Python script)
python3 << 'EOF'
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

with open('~/.claude/credentials/google_token.json', 'r') as f:
    token_data = json.load(f)
creds = Credentials(token=token_data['token'], ...)
service = build('drive', 'v3', credentials=creds)
service.permissions().create(
    fileId='FILE_ID',
    body={'type': 'anyone', 'role': 'reader'}
).execute()
EOF

# 3. Insert into document
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image DOC_ID \
    "https://drive.google.com/uc?export=view&id=FILE_ID" \
    --legend "Figure 1: Description"
```

### 8. Update Table of Contents
Inserts "Table of content" heading placeholder at document start.

**IMPORTANT LIMITATION:**
Google Docs API v1 does NOT support programmatic TOC insertion. This command only inserts the heading.

**Process:**
1. Check if "Table of content" heading already exists at document start
2. If not, insert "Table of content" heading (Heading 1 style) at position 1
3. Provide instructions for manual TOC insertion

**Manual Steps Required:**
After running this command, you must manually complete the TOC insertion:
1. Open the document in Google Docs UI
2. Place cursor after the "Table of content" heading
3. Click Insert > Table of contents > Choose style (with page numbers or links)

**Notes:**
- The automatic TOC will be clickable and navigable
- TOC automatically updates when headings change
- Shows all heading levels that are formatted as headings

## Prerequisites

### System Requirements
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Docs API enabled
- **Google OAuth Credentials** stored in `~/.claude/credentials/`
- Python 3.8+ (managed by uv)

### Google Cloud Setup

1. **Enable Required APIs:**
   ```bash
   gcloud services enable docs.googleapis.com
   gcloud services enable drive.googleapis.com
   ```

2. **Create OAuth Credentials:**
   - Go to Google Cloud Console (https://console.cloud.google.com/)
   - Navigate to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID (Desktop application type)
   - Download credentials as JSON file
   - Save to `~/.claude/credentials/google_credentials.json`

3. **First-time Authentication:**
   ```bash
   # Create credentials directory
   mkdir -p ~/.claude/credentials

   # Copy downloaded credentials
   cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json

   # Run any command - will open browser for OAuth consent
   ~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager info 1lcUWzmqtj-h0OMdM_NcvDN_qa4EyAfwCgE-IZUAlLPc

   # Token saved to ~/.claude/credentials/google_token.json for future use
   ```

4. **Subsequent Runs:**
   - Token automatically refreshed when expired
   - No browser interaction needed
   - Seamless authentication

### Installation
**No manual installation required!** The `run.sh` script automatically:
1. Creates an isolated virtual environment (`.venv`)
2. Installs all dependencies from `pyproject.toml`
3. Runs the script with proper isolation

The first run may take a few seconds to set up the environment. Subsequent runs are instant.

## Common Workflows

### 1. Create New Report

```bash
# Create from template
DOC_ID=$(~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Q4 Sales Report" 1folderabc123 | grep "Document ID:" | cut -d' ' -f3)

# Set content from markdown
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown $DOC_ID report.md

# Add table
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table $DOC_ID sales_data.csv --legend "Table 1: Quarterly Sales"

# Add chart image
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image $DOC_ID "https://charts.example.com/q4.png" --legend "Figure 1: Sales Trends"

# Update TOC
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc $DOC_ID
```

### 2. Update Existing Document Section

```bash
# Read current section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read-section 1docabc123 "Methodology" > methodology.md

# Edit methodology.md locally...

# Update section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-section 1docabc123 "Methodology" methodology.md

# Update TOC
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc 1docabc123
```

### 3. Generate Report from Data

```bash
# Create document
DOC_ID=$(~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Analysis Report" 1folder123 | grep "Document ID:" | cut -d' ' -f3)

# Generate markdown report from data
python generate_report.py --output report.md

# Set content
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown $DOC_ID report.md

# Add multiple tables
for table in results/*.csv; do
    legend=$(basename "$table" .csv | sed 's/_/ /g')
    ~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table $DOC_ID "$table" --legend "Table: $legend"
done

# Update TOC
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc $DOC_ID
```

## Best Practices

### Document Creation
- **Always use template:** Start with template to ensure consistent styling
- **Clear before writing:** Template copy clears content but preserves styles
- **TOC placement:** Table of contents is inserted at document start

### Content Management
- **Section updates:** Use section updates for partial modifications to preserve other content
- **Structure first:** Use `get-structure` to understand document organization
- **TOC updates:** Always update TOC after content changes

### Markdown Conversion
- **Heading levels:** Follow markdown to heading style mapping
- **Tables:** Use CSV format for clean table conversion
- **Images:** Upload images to Drive first if using local files

### Formatting
- **Table legends:** Always in italic above the table
- **Image legends:** Always in italic below the image, left-aligned
- **Consistent styles:** Use template styles for uniform formatting

### Performance
- **Batch operations:** Group multiple updates when possible
- **Large documents:** Consider section updates for large documents
- **API limits:** Be mindful of Google Docs API quotas

## How to Respond to Docs Requests

When users request Docs operations:

1. **Identify the operation:**
   - Create, read, update, insert table/image, update TOC

2. **Gather required parameters:**
   - Document ID (from user or search)
   - Content/markdown file
   - Section headings
   - Table/image data

3. **Run the appropriate command:**
   - Execute script with proper arguments
   - Monitor output for progress and errors
   - Report results to user

4. **Handle document structure:**
   - Use `get-structure` to understand organization
   - Find section boundaries for updates
   - Verify heading names exist

5. **Handle errors:**
   - Check authentication if OAuth errors occur
   - Verify document IDs if not found
   - Confirm API access if permission errors occur

## Example Interactions

### Example 1: Create Document and Add Content

**User:** "Create a new Google Doc for the Q4 report and add this markdown content"

**Response:**
```
I'll create a new Google Doc from the template and add your content.

Creating document...
```

**Execute:**
```bash
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Q4 Report" 1folderabc123
```

**Then:**
```bash
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown 1newdoc123 content.md
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc 1newdoc123
```

**Final response:**
```
✅ Created document "Q4 Report"
✅ Added content from markdown
✅ Updated table of contents

Document link: https://docs.google.com/document/d/1newdoc123/edit
```

### Example 2: Update Specific Section

**User:** "Update the 'Conclusion' section in this document with new content"

**Response:**
```
I'll update the Conclusion section with your new content.

First, let me check the document structure...
```

**Execute:**
```bash
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager get-structure 1docabc123
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-section 1docabc123 "Conclusion" new_conclusion.md
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc 1docabc123
```

**Final response:**
```
✅ Updated 'Conclusion' section
✅ Refreshed table of contents

The Conclusion section has been updated while preserving all other content.
```

## Troubleshooting

### "Google OAuth credentials not found"
```bash
# Create credentials directory
mkdir -p ~/.claude/credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.claude/credentials/google_credentials.json
```

### "Permission denied" errors
```bash
# Ensure Docs and Drive APIs are enabled
gcloud services enable docs.googleapis.com drive.googleapis.com

# Verify OAuth scopes include:
# - https://www.googleapis.com/auth/documents
# - https://www.googleapis.com/auth/drive
```

### "Section not found"
- Verify exact heading text (case-sensitive)
- Use `get-structure` to see all available headings
- Check heading style (must be Heading 1-5, not just bold text)

### "Template access denied"
- Ensure template document is accessible
- Share template with service account or OAuth user
- Verify template URL is correct

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.claude/credentials/google_token.json
# Run any command to re-authenticate
```

## Security & Privacy

- **OAuth authentication:** Uses secure OAuth 2.0 flow
- **Local credentials:** Stores credentials in `~/.claude/credentials/`
- **API access:** Only requests minimum required scopes
- **No logging:** Script does not log or store document content
- **Secure transfer:** All transfers use HTTPS

## Dependencies

Automatically installed by uv:
- `google-api-python-client` - Google Docs/Drive API client
- `google-auth-httplib2` - Authentication transport
- `google-auth-oauthlib` - OAuth 2.0 flow

## Response Approach

To accomplish Docs management tasks:

1. Identify the specific operation requested
2. Gather required parameters (document ID, content, sections)
3. Check document structure if needed (get-structure)
4. Execute the appropriate command
5. Update table of contents if content changed
6. Monitor output for progress and errors
7. Report results with document link
8. Handle errors with appropriate troubleshooting steps
