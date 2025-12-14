# Google Docs Manager Skill

Expert skill for managing Google Docs with comprehensive read/write/update operations, markdown integration, styling, table of contents, images, and tables.

## Features

### Core Features
- **Create from Template**: Start with pre-configured styles
- **Read/Write**: Full document or section-level operations
- **Markdown Support**: Convert markdown to Google Docs with proper formatting
- **Structure Navigation**: Query document structure by headings

### Content Management
- **Insert After Section**: Add content without replacing existing sections
- **Delete Text**: Remove text by index range
- **Tables**: Insert formatted tables from CSV with legends
- **Images**: Insert images with legends and styling
- **Table of Contents**: Auto-generate and update TOC

### Advanced Formatting
- **Text Formatting**: Bold, italic, underline, strikethrough, color, font size
- **Paragraph Alignment**: Left, center, right, justified
- **Lists**: Bulleted lists with custom styles (disc, checkbox, arrow) and numbered lists

### Advanced Table Operations
- **Add/Delete Rows & Columns**: Dynamically modify table structure
- **Update Cell Content**: Edit individual cells
- **Cell Styling**: Background colors, padding
- **Merge/Unmerge Cells**: Create complex table layouts

### Advanced Image Features
- **Resize Images**: Set custom width and height
- **Image Borders**: Add borders with custom colors
- **Text Wrapping**: Control how text flows around images

### Headers & Footers
- **Custom Headers**: Add document headers with optional page numbers
- **Custom Footers**: Add document footers with optional page numbers

## Quick Start

### Prerequisites

1. Install `uv` (Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Enable Google APIs:
   ```bash
   gcloud services enable docs.googleapis.com drive.googleapis.com
   ```

3. Set up OAuth credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download and save to `~/.claude/credentials/google_credentials.json`

### First-Time Authentication

```bash
# Create credentials directory
mkdir -p ~/.claude/credentials

# Copy your OAuth credentials
cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json

# Run any command to authenticate (opens browser)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager info 1lcUWzmqtj-h0OMdM_NcvDN_qa4EyAfwCgE-IZUAlLPc
```

## Usage

### Create Document from Template

```bash
# Creates a new document with pre-configured styles
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Q4 Report" 1folderabc123
```

### Read Document

```bash
# Read full document as markdown
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read 1docabc123xyz

# Read specific section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager read-section 1docabc123xyz "Introduction"
```

### Get Document Structure

```bash
# List all headings
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager get-structure 1docabc123xyz
```

### Update Content

```bash
# Replace entire content with markdown
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown 1docabc123xyz content.md

# Update specific section
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-section 1docabc123xyz "Methodology" methodology.md
```

### Insert Tables

```bash
# Insert table with legend (CSV format)
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table 1docabc123xyz data.csv --legend "Table 1: Sales Data Q4 2024"
```

### Insert Images

```bash
# Insert image with legend
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image 1docabc123xyz "https://example.com/chart.png" --legend "Figure 1: Revenue Trends"
```

### Update Table of Contents

```bash
# Regenerate TOC based on current headings
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc 1docabc123xyz
```

## Template Document

The skill uses a template document with pre-configured styles:

**Template ID**: `1lcUWzmqtj-h0OMdM_NcvDN_qa4EyAfwCgE-IZUAlLPc`

### Style Mapping

| Markdown | Google Docs Style |
|----------|------------------|
| `# Title` | Title |
| `## Chapter` | Heading 1 |
| `### Sub Chapter` | Heading 2 |
| `#### Sub Sub Chapter` | Heading 3 |
| `##### Level 4` | Heading 4 |
| `###### Level 5` | Heading 5 |

### Inline Formatting

- `**bold**` → **Bold text**
- `*italic*` → *Italic text*

### Special Elements

- **Table legends**: Italic text above table
- **Image legends**: Italic text below image, left-aligned, with blank line after for spacing
- **Table of Contents**: Auto-generated from headings

## Example Workflow

```bash
# 1. Create document from template
DOC_ID=$(~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager create-from-template "Analysis Report" 1folder123 | tail -1)

# 2. Add content from markdown
cat > report.md << 'EOF'
# Annual Analysis Report

## Executive Summary
This report provides comprehensive analysis of Q4 performance.

## Methodology
Our analysis used the following approach:
- Data collection from primary sources
- Statistical analysis using **advanced models**
- Peer review validation
EOF

~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager set-markdown $DOC_ID report.md

# 3. Add a table
cat > data.csv << 'EOF'
Month,Sales,Growth
October,$125k,+5%
November,$142k,+13%
December,$198k,+39%
EOF

~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-table $DOC_ID data.csv --legend "Table 1: Quarterly Sales Performance"

# 4. Add an image
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image $DOC_ID "https://charts.example.com/q4.png" --legend "Figure 1: Sales Trends"

# 5. Update table of contents
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager update-toc $DOC_ID

# 6. View the document
echo "Document link: https://docs.google.com/document/d/$DOC_ID/edit"
```

## Architecture

```
scripts/
├── run.sh                     # uv-based script runner
├── pyproject.toml             # Dependencies
└── src/
    ├── docs_manager.py        # CLI interface
    ├── auth.py                # OAuth authentication
    └── docs_operations.py     # Core operations
```

## Operations

### Document Management
- `create`: Create blank document
- `create-from-template`: Create from template with styles (RECOMMENDED)
- `info`: Get document metadata

### Content Operations
- `read`: Read full document as markdown
- `read-section`: Read specific section
- `get-structure`: List all headings with indices
- `set-markdown`: Replace content with markdown
- `update-section`: Update section with markdown
- `insert-after-section`: Insert content after a section

### Text Operations
- `delete-text`: Delete text range by indices
- `format-text`: Apply text formatting (bold, italic, underline, strikethrough, color, font-size)
- `align-paragraph`: Set paragraph alignment (START, CENTER, END, JUSTIFIED)

### List Operations
- `create-bullets`: Create bulleted list with custom styles
- `create-numbered`: Create numbered list
- `remove-bullets`: Remove bullets/numbering from text

### Table Operations
- `insert-table`: Add table from CSV with legend
- `add-table-rows`: Add rows to existing table
- `add-table-columns`: Add columns to existing table
- `delete-table-row`: Delete a table row
- `delete-table-column`: Delete a table column
- `update-table-cell`: Update individual cell content
- `style-table-cell`: Apply cell styling (background color, padding)
- `merge-table-cells`: Merge a range of cells
- `unmerge-table-cells`: Unmerge previously merged cells

### Image Operations
- `insert-image`: Add image with legend
- `style-image`: Resize, add borders, and control text wrapping

### Document Structure
- `add-header`: Add/update document header with optional page numbers
- `add-footer`: Add/update document footer with optional page numbers
- `update-toc`: Regenerate table of contents

## Best Practices

1. **Always use template**: Ensures consistent styling
2. **Update TOC**: Call `update-toc` after content changes
3. **Section updates**: Use `update-section` to preserve other content
4. **Structure first**: Use `get-structure` to understand document organization
5. **CSV for tables**: Use proper CSV format for clean tables

## Troubleshooting

### Authentication Issues

```bash
# Delete token and re-authenticate
rm ~/.claude/credentials/google_token.json
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager info DOCUMENT_ID
```

### API Not Enabled

```bash
gcloud services enable docs.googleapis.com drive.googleapis.com
```

### Section Not Found

Use exact heading text (case-sensitive):

```bash
# Check available headings
~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager get-structure DOCUMENT_ID
```

## Development

No installation required! The `run.sh` script uses `uv` to:
- Auto-create virtual environment
- Install dependencies
- Run isolated scripts

First run may take a few seconds for setup. Subsequent runs are instant.

## Dependencies

- `google-api-python-client` - Google Docs/Drive API
- `google-auth-httplib2` - Auth transport
- `google-auth-oauthlib` - OAuth flow

## Security

- OAuth 2.0 authentication
- Credentials stored in `~/.claude/credentials/`
- Minimum required scopes only
- All transfers use HTTPS
- No content logging

## Links

- [Template Document](https://docs.google.com/document/d/1lcUWzmqtj-h0OMdM_NcvDN_qa4EyAfwCgE-IZUAlLPc)
- [Google Docs API](https://developers.google.com/docs/api)
- [Google Drive API](https://developers.google.com/drive/api)
