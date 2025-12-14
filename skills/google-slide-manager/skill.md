---
name: google-slide-manager
description: Expert in managing Google Slides presentations. **Use this skill whenever the user mentions 'Google Slides', 'presentation', 'slides', or requests to create, edit, format, translate, export, or manage presentations.** Handles all presentation operations including creation, formatting, animations, themes, translations, screenshots, and exports.
---

# Google Slide Manager Skill

Expert in comprehensive Google Slides presentation management with advanced formatting, translation, animation, and export capabilities.

## Core Capabilities

### Presentation Management
- Create new presentations from scratch
- Change presentation themes
- Export to PowerPoint (PPTX) or PDF formats
- Describe presentation structure

### Slide Operations
- Add new slides
- Remove slides
- Describe slide content and layout
- Adapt slides from screenshots
- Take screenshots of slides

### Content Formatting
- Add and format text (bold, italic, underline, colors)
- Create bullet points and numbered lists
- Insert and position images
- Control text alignment and spacing
- Manage fonts and sizes
- Update existing element text
- Delete elements from slides

### Element Transformation
- Move elements by relative offset (dx, dy) or absolute position (x, y)
- Add/remove borders with custom width, style, and color
- Add/remove shadows with custom blur, color, transparency, and offset
- Support for SOLID, DOTTED, DASHED, DOUBLE border styles

### Version Management
- List all revisions with timestamps and authors
- Get details of specific revisions
- Pin revisions to create named versions
- Unpin revisions
- Create named versions from current state

### Advanced Features
- Translate presentations to 100+ languages (preserves formatting)
- Add slide transitions
- Create animations within slides
- Apply and customize themes

## When to Use This Skill

Use when users request:
- "Create a new Google Slides presentation"
- "Add a slide with bullet points"
- "Change the theme to [theme name]"
- "Translate this presentation to French"
- "Add a transition between slides"
- "Insert an image on slide 3"
- "Export this as PowerPoint"
- "Download as PDF"
- "Adapt this slide to match this screenshot"
- "Add animations to the text"
- "Take a screenshot of slide 5"

## Quick Start

### Basic Command Pattern
```bash
~/.claude/skills/google-slide-manager/scripts/run.sh <operation> [args...]
```

### Common Operations

#### Create Presentation
```bash
# Create a new presentation
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "My Presentation Title"
```

#### Manage Slides
```bash
# Add a new slide
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <presentation_id> add --layout TITLE_AND_BODY

# Remove slide 3
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <presentation_id> remove --slide 3

# Describe slide 2
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <presentation_id> describe --slide 2
```

#### Format Content
```bash
# Add text with formatting
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <presentation_id> add-text \
  --slide 1 --text "Hello World" --bold --font-size 24

# Add bullet points
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <presentation_id> add-bullets \
  --slide 1 --items "Point 1" "Point 2" "Point 3"

# Insert image
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <presentation_id> add-image \
  --slide 1 --url "https://example.com/image.png" --width 400 --height 300
```

#### Animations & Transitions
```bash
# Add slide transition
~/.claude/skills/google-slide-manager/scripts/run.sh animations <presentation_id> add-transition \
  --slide 2 --type FADE

# Add text animation
~/.claude/skills/google-slide-manager/scripts/run.sh animations <presentation_id> add-animation \
  --slide 1 --element <element_id> --type APPEAR
```

#### Translation
```bash
# Translate all slides to French
~/.claude/skills/google-slide-manager/scripts/run.sh translate_slides <presentation_id> all fr

# Translate slides 5-10 to Spanish
~/.claude/skills/google-slide-manager/scripts/run.sh translate_slides <presentation_id> 5-10 es
```

#### Export & Screenshot
```bash
# Export as PowerPoint
~/.claude/skills/google-slide-manager/scripts/run.sh export <presentation_id> pptx output.pptx

# Export as PDF
~/.claude/skills/google-slide-manager/scripts/run.sh export <presentation_id> pdf output.pdf

# Take screenshot of slide 3
~/.claude/skills/google-slide-manager/scripts/run.sh screenshot <presentation_id> 3 output.png
```

#### Change Theme
```bash
# Apply a theme
~/.claude/skills/google-slide-manager/scripts/run.sh change_theme <presentation_id> <theme_name>
```

#### Adapt from Screenshot
```bash
# Adapt slide to match a screenshot
~/.claude/skills/google-slide-manager/scripts/run.sh adapt_slide <presentation_id> \
  --slide 2 --screenshot /path/to/screenshot.png
```

#### Update Element
```bash
# Update text of an existing element
~/.claude/skills/google-slide-manager/scripts/run.sh update_element <presentation_id> <element_id> "New text content"
```

#### Delete Element
```bash
# Delete an element from a slide
~/.claude/skills/google-slide-manager/scripts/run.sh delete_element <presentation_id> <element_id>
```

#### Transform Element
```bash
# Move element 10 pixels to the right
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> move --dx 10

# Move element 10 pixels up
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> move --dy -10

# Move element to absolute position
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> move --x 100 --y 200

# Add a solid black border (2 PT)
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> border --width 2

# Add a red dashed border
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> border --width 3 --style DASHED --color "#FF0000"

# Remove border
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> remove-border

# Add a drop shadow
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> shadow

# Add a custom shadow
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> shadow --blur 10 --color "#0000FF" --alpha 0.5 --offset-x 5 --offset-y 5

# Remove shadow
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> remove-shadow
```

#### Manage Versions
```bash
# List revisions
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> list

# List only 10 most recent revisions
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> list --limit 10

# Get details of a specific revision
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> get <revision_id>

# Pin a revision (create a version)
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> pin <revision_id>

# Create a named version from current state
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> create-version "Version 1.0 - Final"
```

## Available Slide Layouts

- `BLANK` - Empty slide
- `TITLE` - Title slide
- `TITLE_AND_BODY` - Title with content
- `TITLE_AND_TWO_COLUMNS` - Title with two columns
- `SECTION_HEADER` - Section divider

## Available Transition Types

- `FADE` - Fade transition
- `SLIDE_FROM_RIGHT` - Slide from right
- `SLIDE_FROM_LEFT` - Slide from left
- `FLIP` - Flip transition
- `CUBE` - Cube rotation

## Available Animation Types

- `APPEAR` - Element appears
- `FADE_IN` - Fade in
- `FLY_IN_FROM_LEFT` - Fly from left
- `FLY_IN_FROM_RIGHT` - Fly from right
- `FLY_IN_FROM_TOP` - Fly from top
- `FLY_IN_FROM_BOTTOM` - Fly from bottom

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
- `all` - All slides in presentation
- `5` - Only slide 5
- `10-15` - Slides 10 through 15
- `1,3,5` - Slides 1, 3, and 5
- `2-4,6-8` - Multiple ranges

## How It Works

The `run.sh` script automatically:
1. Creates isolated virtual environment (`.venv`)
2. Installs dependencies via `uv`
3. Authenticates with Google APIs (OAuth 2.0)
4. Executes the requested operation
5. Reports results and statistics

No manual setup required - just run the script.

## Prerequisites

### System Requirements
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Slides API and Translation API enabled
- **OAuth credentials** in `~/.claude/credentials/google_credentials.json`

### Quick Setup
```bash
# Enable required APIs
gcloud services enable slides.googleapis.com translate.googleapis.com drive.googleapis.com

# Create credentials directory
mkdir -p ~/.claude/credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.claude/credentials/google_credentials.json
```

First run opens browser for OAuth consent. Token saved for future use.

## Example Workflows

### Create and Format a Presentation
```bash
# 1. Create presentation
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "Q4 Results"

# 2. Add title slide content
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <id> add-text \
  --slide 1 --text "Q4 Results 2025" --bold --font-size 36

# 3. Add content slide
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <id> add --layout TITLE_AND_BODY

# 4. Add bullet points
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <id> add-bullets \
  --slide 2 --items "Revenue up 25%" "New customers: 1,200" "Market expansion"

# 5. Add image
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <id> add-image \
  --slide 2 --url "https://example.com/chart.png"

# 6. Add transitions
~/.claude/skills/google-slide-manager/scripts/run.sh animations <id> add-transition \
  --slide 2 --type FADE
```

### Translate Existing Presentation
```bash
# Translate slides 1-10 to French
~/.claude/skills/google-slide-manager/scripts/run.sh translate_slides <id> 1-10 fr
```

### Export Presentation
```bash
# Export as PowerPoint
~/.claude/skills/google-slide-manager/scripts/run.sh export <id> pptx ~/Downloads/presentation.pptx

# Export as PDF
~/.claude/skills/google-slide-manager/scripts/run.sh export <id> pdf ~/Downloads/presentation.pdf
```

## Best Practices

- **Backup presentations:** Make copies before major changes
- **Monitor output:** Watch for progress and error messages
- **Use descriptive names:** Clear presentation and slide titles
- **Test formatting:** Preview slides after formatting changes
- **API quotas:** Be mindful of Google API limits

## What Gets Preserved

When translating or formatting:
- Text formatting (bold, italic, underline)
- Font families and sizes
- Colors and backgrounds
- Text alignment and spacing
- Hyperlinks and special characters
- Images and layouts

## Limitations

- **Translation:** Images with embedded text not OCR'd
- **Table translation:** Limited support for table content
- **Complex animations:** Some advanced animations may need manual adjustment
- **Theme customization:** Limited to predefined themes

## Reference Documentation

- **[operations.md](references/operations.md)** - Complete command reference for all operations
- **[authentication.md](references/authentication.md)** - Google OAuth setup and credentials
- **[formatting.md](references/formatting.md)** - Text formatting, bullets, images, alignment
- **[animations.md](references/animations.md)** - Transitions and slide animations
- **[translation.md](references/translation.md)** - Translation workflows and language codes
- **[export.md](references/export.md)** - Export to PowerPoint and PDF
- **[troubleshooting.md](references/troubleshooting.md)** - Common errors and solutions

## Quick Troubleshooting

### "Google OAuth credentials not found"
```bash
mkdir -p ~/.claude/credentials
# Download from Google Cloud Console and save to:
# ~/.claude/credentials/google_credentials.json
```

### "Permission denied"
```bash
gcloud services enable slides.googleapis.com translate.googleapis.com drive.googleapis.com
```

### "Presentation not found"
- Verify presentation ID from URL
- Check you have view/edit access

### "uv not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For detailed troubleshooting, see: [references/troubleshooting.md](references/troubleshooting.md)
