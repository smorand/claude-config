---
name: google-slide-manager
description: Expert in managing Google Slides presentations. **Use this skill whenever the user mentions 'Google Slides', 'presentation', 'slides', or requests to create, edit, format, translate, export, or manage presentations.** Handles all presentation operations including creation, formatting, animations, themes, translations, screenshots, and exports.
---

# Google Slide Manager Skill

Expert in comprehensive Google Slides presentation management with advanced formatting, translation, animation, and export capabilities.

## Core Capabilities

### Presentation Management
- Create new presentations from scratch
- Copy themes between presentations
- Export to PowerPoint (PPTX) or PDF formats
- Extract all text content from presentations

### Slide Operations
- Add new slides to presentations
- Remove slides by index
- Duplicate existing slides
- Move slides to different positions
- Reorder multiple slides at once

### Content & Shapes
- Add shapes (RECTANGLE, ELLIPSE, TRIANGLE, etc.)
- Create tables with configurable rows/columns
- Update table cell content
- Style table cells (background colors)
- Copy text styling between elements

### Speaker Notes
- Add speaker notes to slides
- Get speaker notes from specific slides
- Extract all speaker notes from presentation

### Text Operations
- Search for text across presentation
- Find and replace text globally
- Extract all text content
- Copy text styling between elements

### Translation
- Translate presentations to 100+ languages (preserves formatting)
- Translate all slides or specific slide ranges
- Auto-detection of source language
- Supports complex slide range syntax (e.g., "1-5,7,10-12")

### Export & Distribution
- Export to PowerPoint (PPTX) format
- Export to PDF format
- Preserve all formatting and layouts

## When to Use This Skill

Use when users request:
- "Create a new Google Slides presentation"
- "Add a slide to this presentation"
- "Copy the theme from one presentation to another"
- "Translate this presentation to French"
- "Add a table to slide 3"
- "Add speaker notes to slide 5"
- "Export this as PowerPoint"
- "Download as PDF"
- "Search for text in the presentation"
- "Replace all instances of X with Y"
- "Extract all speaker notes"
- "Duplicate slide 3"
- "Move slide 5 to position 2"
- "Reorder the slides"

## Quick Start

### Basic Command Pattern
```bash
~/.claude/skills/google-slide-manager/scripts/google-slide-manager [command] [flags...]
```

### Common Operations

#### Create Presentation
```bash
# Create a new presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager create-presentation \
  --title "My Presentation Title"
```

#### Manage Slides
```bash
# Add a new slide
~/.claude/skills/google-slide-manager/scripts/google-slide-manager add-slide \
  --presentation-id <presentation_id>

# Duplicate a slide
~/.claude/skills/google-slide-manager/scripts/google-slide-manager duplicate-slide \
  --presentation-id <presentation_id> --slide-index 2

# Move slide from position 3 to position 1
~/.claude/skills/google-slide-manager/scripts/google-slide-manager move-slide \
  --presentation-id <presentation_id> --from-index 3 --to-index 1

# Reorder slides (e.g., reorder to 2,1,3,4)
~/.claude/skills/google-slide-manager/scripts/google-slide-manager reorder-slides \
  --presentation-id <presentation_id> --indices "2,1,3,4"

# Remove slide at index 3
~/.claude/skills/google-slide-manager/scripts/google-slide-manager remove-slide \
  --presentation-id <presentation_id> --slide-index 3
```

#### Content & Shapes
```bash
# Add a rectangle shape
~/.claude/skills/google-slide-manager/scripts/google-slide-manager add-shape \
  --presentation-id <presentation_id> --slide-index 1 --shape-type RECTANGLE \
  --x 100 --y 100 --width 200 --height 100

# Create a table
~/.claude/skills/google-slide-manager/scripts/google-slide-manager create-table \
  --presentation-id <presentation_id> --slide-index 1 \
  --rows 3 --columns 4 --x 50 --y 50 --width 600 --height 300

# Update table cell content
~/.claude/skills/google-slide-manager/scripts/google-slide-manager update-cell \
  --presentation-id <presentation_id> --table-id <table_id> \
  --row 0 --column 1 --text "Updated Content"

# Style table cell (background color)
~/.claude/skills/google-slide-manager/scripts/google-slide-manager style-cell \
  --presentation-id <presentation_id> --table-id <table_id> \
  --row 0 --column 1 --bg-color "#FF5733"

# Copy text style from one element to another
~/.claude/skills/google-slide-manager/scripts/google-slide-manager copy-text-style \
  --presentation-id <presentation_id> --source-element-id <source_id> \
  --target-element-id <target_id>
```

#### Speaker Notes
```bash
# Add speaker notes to a slide
~/.claude/skills/google-slide-manager/scripts/google-slide-manager add-notes \
  --presentation-id <presentation_id> --slide-index 1 \
  --notes "Remember to mention the key points"

# Get speaker notes from a slide
~/.claude/skills/google-slide-manager/scripts/google-slide-manager get-notes \
  --presentation-id <presentation_id> --slide-index 1

# Extract all speaker notes from presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager extract-all-notes \
  --presentation-id <presentation_id>
```

#### Text Operations
```bash
# Search for text in presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager search-text \
  --presentation-id <presentation_id> --query "search term"

# Find and replace text
~/.claude/skills/google-slide-manager/scripts/google-slide-manager replace-text \
  --presentation-id <presentation_id> --find "old text" --replace "new text"

# Extract all text from presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager extract-all-text \
  --presentation-id <presentation_id>
```

#### Translation
```bash
# Translate all slides to French
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides \
  --presentation-id <presentation_id> --target-lang fr

# Translate specific slides (5-10) to Spanish
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides \
  --presentation-id <presentation_id> --target-lang es --slide-range "5-10"

# Translate single slide to German
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides \
  --presentation-id <presentation_id> --target-lang de --slide-range "3"
```

#### Theme Management
```bash
# Copy theme from one presentation to another
~/.claude/skills/google-slide-manager/scripts/google-slide-manager copy-theme \
  --source-presentation-id <source_id> --target-presentation-id <target_id>
```

#### Export
```bash
# Export as PowerPoint
~/.claude/skills/google-slide-manager/scripts/google-slide-manager export-pptx \
  --presentation-id <presentation_id> --output ~/Downloads/presentation.pptx

# Export as PDF
~/.claude/skills/google-slide-manager/scripts/google-slide-manager export-pdf \
  --presentation-id <presentation_id> --output ~/Downloads/presentation.pdf
```

## Available Shape Types

- `RECTANGLE` - Rectangle shape
- `ELLIPSE` - Ellipse/circle shape
- `TRIANGLE` - Triangle shape
- `ROUND_RECTANGLE` - Rectangle with rounded corners
- `TEXT_BOX` - Text box
- `CLOUD` - Cloud shape
- `STAR` - Star shape
- `ARROW` - Arrow shape

## Translation Features

### Language Support
Supports 100+ languages via Google Cloud Translation API with auto-detection of source language.

### Common Language Codes
| Language | Code | Language | Code |
|----------|------|----------|------|
| French | `fr` | Spanish | `es` |
| German | `de` | Italian | `it` |
| Portuguese | `pt` | Japanese | `ja` |
| Chinese | `zh` | Korean | `ko` |
| Arabic | `ar` | Russian | `ru` |

### Slide Range Formats
- If no `--slide-range` is specified, all slides are translated
- `--slide-range "5"` - Only slide 5
- `--slide-range "10-15"` - Slides 10 through 15
- `--slide-range "1,3,5"` - Slides 1, 3, and 5
- `--slide-range "2-4,6-8"` - Multiple ranges

## How It Works

The `google-slide-manager` binary is a standalone Go executable that:
1. Authenticates with Google APIs using OAuth 2.0
2. Executes presentation operations via Google Slides API
3. Handles translation via Google Cloud Translation API
4. Exports presentations to PDF/PowerPoint formats
5. Manages all operations efficiently in a single binary

No dependencies required - just run the binary directly.

## Prerequisites

### System Requirements
- **GCP Project** with Slides API, Translation API, and Drive API enabled
- **OAuth credentials** in `~/.credentials/google_credentials.json`

### Quick Setup
```bash
# Enable required APIs
gcloud services enable slides.googleapis.com translate.googleapis.com drive.googleapis.com

# Create credentials directory
mkdir -p ~/.credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.credentials/google_credentials.json
```

First run opens browser for OAuth consent. Token saved to `~/.credentials/google_token.json` for future use.

## Example Workflows

### Create and Format a Presentation
```bash
# 1. Create presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager create-presentation \
  --title "Q4 Results"

# 2. Add a new slide
~/.claude/skills/google-slide-manager/scripts/google-slide-manager add-slide \
  --presentation-id <id>

# 3. Create a table on slide 2
~/.claude/skills/google-slide-manager/scripts/google-slide-manager create-table \
  --presentation-id <id> --slide-index 1 --rows 4 --columns 3 \
  --x 50 --y 50 --width 600 --height 300

# 4. Update table cells with data
~/.claude/skills/google-slide-manager/scripts/google-slide-manager update-cell \
  --presentation-id <id> --table-id <table_id> --row 0 --column 0 --text "Metric"

~/.claude/skills/google-slide-manager/scripts/google-slide-manager update-cell \
  --presentation-id <id> --table-id <table_id> --row 1 --column 0 --text "Revenue"

# 5. Add speaker notes
~/.claude/skills/google-slide-manager/scripts/google-slide-manager add-notes \
  --presentation-id <id> --slide-index 1 \
  --notes "Highlight 25% revenue growth and customer acquisition"
```

### Translate Existing Presentation
```bash
# Translate slides 1-10 to French
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides \
  --presentation-id <id> --target-lang fr --slide-range "1-10"

# Translate all slides to Spanish
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides \
  --presentation-id <id> --target-lang es
```

### Export Presentation
```bash
# Export as PowerPoint
~/.claude/skills/google-slide-manager/scripts/google-slide-manager export-pptx \
  --presentation-id <id> --output ~/Downloads/presentation.pptx

# Export as PDF
~/.claude/skills/google-slide-manager/scripts/google-slide-manager export-pdf \
  --presentation-id <id> --output ~/Downloads/presentation.pdf
```

### Working with Text
```bash
# Search for specific text
~/.claude/skills/google-slide-manager/scripts/google-slide-manager search-text \
  --presentation-id <id> --query "revenue"

# Replace text throughout presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager replace-text \
  --presentation-id <id> --find "2024" --replace "2025"

# Extract all text from presentation
~/.claude/skills/google-slide-manager/scripts/google-slide-manager extract-all-text \
  --presentation-id <id>
```

## Best Practices

- **Backup presentations:** Make copies before major changes (use duplicate feature)
- **Monitor output:** Watch for progress and error messages
- **Use descriptive names:** Clear presentation and slide titles
- **Test operations:** Preview slides after making changes
- **API quotas:** Be mindful of Google API limits (quotas apply per project)
- **Slide indices:** Remember that slide indices are 0-based (first slide is index 0)
- **Table IDs:** When working with tables, note the table ID from creation for subsequent operations

## What Gets Preserved

When translating presentations:
- Text formatting (bold, italic, underline)
- Font families and sizes
- Colors and backgrounds
- Text alignment and spacing
- Hyperlinks and special characters
- Images and layouts
- Slide structure and order
- Speaker notes (also translated)

## Limitations

- **Translation:** Images with embedded text are not OCR'd or translated
- **Slide layouts:** Cannot create custom layouts (uses presentation's default)
- **Advanced formatting:** Some complex text effects may not be fully supported
- **Table styling:** Limited to background colors (no borders, text formatting in cells)
- **Binary size:** 22MB Go binary (all dependencies compiled in)

## Getting Help

For detailed command help, use the `--help` flag:

```bash
# Get general help
~/.claude/skills/google-slide-manager/scripts/google-slide-manager --help

# Get help for a specific command
~/.claude/skills/google-slide-manager/scripts/google-slide-manager create-presentation --help
~/.claude/skills/google-slide-manager/scripts/google-slide-manager translate-slides --help
~/.claude/skills/google-slide-manager/scripts/google-slide-manager export-pdf --help
```

Each command includes detailed usage information, required flags, and examples.

## Quick Troubleshooting

### "Google OAuth credentials not found"
```bash
mkdir -p ~/.credentials
# Download from Google Cloud Console and save to:
# ~/.credentials/google_credentials.json
```

### "Permission denied" or "API not enabled"
```bash
gcloud services enable slides.googleapis.com translate.googleapis.com drive.googleapis.com
```

### "Presentation not found"
- Verify presentation ID from URL (format: `https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit`)
- Check you have view/edit access to the presentation
- Ensure you're authenticated with the correct Google account

### "Token expired" or authentication errors
```bash
# Remove the old token to force re-authentication
rm ~/.credentials/google_token.json
# Next run will prompt for OAuth consent again
```

### Binary not executable
```bash
chmod +x ~/.claude/skills/google-slide-manager/scripts/google-slide-manager
```
