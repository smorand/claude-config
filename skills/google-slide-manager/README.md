# Google Slide Manager

Comprehensive Google Slides presentation management skill for Claude Code.

## Features

- **Presentation Management**
  - Create new presentations
  - Export to PowerPoint (PPTX) and PDF
  - Change themes (UI-based guidance)

- **Slide Operations**
  - Add/remove slides with various layouts
  - Describe slide structure and content
  - Take screenshots of slides

- **Content Formatting**
  - Add formatted text (bold, italic, underline, colors, fonts)
  - Create bullet points and numbered lists
  - Insert images from URLs
  - Control positioning and sizing

- **Element Transformation**
  - Move elements by relative offset or absolute position
  - Add/remove borders (solid, dotted, dashed, double)
  - Add/remove shadows with custom properties
  - Update element text and delete elements

- **Version Management**
  - List all revisions with timestamps and authors
  - Get details of specific revisions
  - Pin/unpin revisions to create named versions
  - Create named versions from current state

- **Advanced Features**
  - Translate presentations to 100+ languages (auto-detects source)
  - Add slide transitions (UI-based guidance)
  - Add element animations (UI-based guidance)
  - Adapt slides from screenshots using AI vision

## Quick Start

### Prerequisites

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Enable required Google APIs
gcloud services enable slides.googleapis.com translate.googleapis.com drive.googleapis.com

# Set up OAuth credentials
mkdir -p ~/.claude/credentials
# Download credentials.json from Google Cloud Console
# Save to ~/.claude/credentials/google_credentials.json
```

### Basic Usage

```bash
# Create a new presentation
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "My Presentation"

# Add a slide
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <presentation_id> add --layout TITLE_AND_BODY

# Add text with formatting
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <presentation_id> add-text \
  --slide 1 --text "Hello World" --bold --font-size 24

# Add bullet points
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <presentation_id> add-bullets \
  --slide 1 --items "Point 1" "Point 2" "Point 3"

# Translate to French
~/.claude/skills/google-slide-manager/scripts/run.sh translate_slides <presentation_id> all fr

# Export as PowerPoint
~/.claude/skills/google-slide-manager/scripts/run.sh export <presentation_id> pptx output.pptx

# Export as PDF
~/.claude/skills/google-slide-manager/scripts/run.sh export <presentation_id> pdf output.pdf

# Move an element
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> move --dx 10

# Add a border
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> border --width 2 --color "#FF0000"

# Add a shadow
~/.claude/skills/google-slide-manager/scripts/run.sh transform_element <presentation_id> <element_id> shadow

# List revisions
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> list

# Create a named version
~/.claude/skills/google-slide-manager/scripts/run.sh manage_versions <presentation_id> create-version "Version 1.0"
```

## Available Operations

### create_presentation
Create a new Google Slides presentation.

```bash
run.sh create_presentation "Title"
```

### manage_slides
Add, remove, or describe slides.

```bash
# Add slide
run.sh manage_slides <id> add --layout TITLE_AND_BODY

# Remove slide
run.sh manage_slides <id> remove --slide 3

# Describe slide
run.sh manage_slides <id> describe --slide 2
```

**Available layouts:** `BLANK`, `TITLE`, `TITLE_AND_BODY`, `TITLE_AND_TWO_COLUMNS`, `SECTION_HEADER`

### format_content
Format slide content with text, bullets, and images.

```bash
# Add text
run.sh format_content <id> add-text --slide 1 --text "Hello" --bold --font-size 24

# Add bullets
run.sh format_content <id> add-bullets --slide 1 --items "A" "B" "C"

# Add numbered list
run.sh format_content <id> add-numbered --slide 1 --items "1" "2" "3"

# Add image
run.sh format_content <id> add-image --slide 1 --url "https://example.com/img.png"
```

### translate_slides
Translate presentation to different languages.

```bash
# Translate all slides to French
run.sh translate_slides <id> all fr

# Translate slides 5-10 to Spanish
run.sh translate_slides <id> 5-10 es

# Translate specific slides to German
run.sh translate_slides <id> 1,3,5 de
```

**Common language codes:** `fr`, `es`, `de`, `it`, `pt`, `ja`, `zh`, `ko`, `ar`, `ru`

**Slide ranges:** `all`, `5`, `10-15`, `1,3,5`, `2-4,6-8`

### export
Export presentation as PowerPoint or PDF.

```bash
# Export as PowerPoint
run.sh export <id> pptx ~/Downloads/presentation.pptx

# Export as PDF
run.sh export <id> pdf ~/Downloads/presentation.pdf
```

### animations
Add transitions (limited API support - provides UI guidance).

```bash
run.sh animations <id> add-transition --slide 2 --type FADE
```

### screenshot
Get slide information for screenshots (provides UI guidance).

```bash
run.sh screenshot <id> 3 output.png
```

### change_theme
Change presentation theme (provides UI guidance).

```bash
run.sh change_theme <id> "Simple Light"
```

### adapt_slide
Adapt slide layout from screenshot using AI vision.

```bash
run.sh adapt_slide <id> --slide 2 --screenshot /path/to/screenshot.png
```

### transform_element
Move elements and apply borders/shadows.

```bash
# Move element by relative offset
run.sh transform_element <id> <element_id> move --dx 10 --dy -5

# Move element to absolute position
run.sh transform_element <id> <element_id> move --x 100 --y 200

# Add border
run.sh transform_element <id> <element_id> border --width 2 --style SOLID --color "#000000"

# Remove border
run.sh transform_element <id> <element_id> remove-border

# Add shadow
run.sh transform_element <id> <element_id> shadow --blur 6 --color "#000000" --alpha 0.3

# Remove shadow
run.sh transform_element <id> <element_id> remove-shadow
```

**Border styles:** `SOLID`, `DOTTED`, `DASHED`, `DOUBLE`

### manage_versions
List revisions and create named versions.

```bash
# List all revisions
run.sh manage_versions <id> list

# List limited revisions
run.sh manage_versions <id> list --limit 10

# Get revision details
run.sh manage_versions <id> get <revision_id>

# Pin a revision
run.sh manage_versions <id> pin <revision_id>

# Unpin a revision
run.sh manage_versions <id> unpin <revision_id>

# Create a named version
run.sh manage_versions <id> create-version "Version 1.0 - Final"
```

## API Limitations

The Google Slides API has some limitations:

- **Animations**: Cannot be added programmatically (manual UI required)
- **Transitions**: Limited support (manual UI required)
- **Themes**: Cannot be changed programmatically (manual UI required)
- **Screenshots**: No direct API support (provides guidance for alternatives)
- **Local images**: Must use public URLs (local file upload not yet implemented)

These operations provide guidance on how to perform them manually.

## Authentication

First run opens a browser for OAuth consent. Credentials are saved to:
- `~/.claude/credentials/google_token.json` (auto-generated token)
- `~/.claude/credentials/google_credentials.json` (OAuth client credentials)

## Documentation

- [skill.md](skill.md) - Complete skill reference
- [CLAUDE.md](CLAUDE.md) - AI implementation guide
- [references/](references/) - Detailed operation documentation

## Migration from google-slides-translator

This skill replaces the `google-slides-translator` skill and includes all translation functionality plus comprehensive presentation management capabilities.

## License

Part of Claude Code skills collection.
