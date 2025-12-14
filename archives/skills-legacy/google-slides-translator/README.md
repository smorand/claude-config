# Google Slides Translator Skill

Expert skill for translating Google Slides presentations to different languages while preserving all formatting, styles, and layout.

## Overview

This skill enables seamless translation of Google Slides presentations using Google Cloud Translation API. It automatically detects the source language and translates all text elements while maintaining formatting, colors, fonts, and layout.

## Quick Start

### Prerequisites

- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Cloud Translation API enabled
- **Google OAuth Credentials** stored in `~/.claude/credentials/`
- No other manual installation required!

### Setup Google OAuth

```bash
# 1. Create credentials directory
mkdir -p ~/.claude/credentials

# 2. Download OAuth credentials from Google Cloud Console
# - Go to https://console.cloud.google.com/
# - APIs & Services > Credentials
# - Create OAuth 2.0 Client ID (Desktop application)
# - Download JSON file

# 3. Save credentials
cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json

# 4. Enable required APIs
gcloud services enable slides.googleapis.com
gcloud services enable translate.googleapis.com
```

### Basic Usage

```bash
# Translate entire presentation to French
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> all fr

# Translate slides 10-15 to Spanish
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> 10-15 es

# Translate specific slides to German
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> 1,5,10 de
```

**First run:** May take a few seconds to create the virtual environment and install dependencies. A browser window will open for OAuth authentication. Subsequent runs are instant and automatic!

## Features

- ✅ Multi-range slide support (all, 10-15, 1,5,10, 2-4,6-8)
- ✅ Auto-detect source language
- ✅ Preserve all formatting, styles, colors, and fonts
- ✅ In-place translation (updates original presentation)
- ✅ 100+ target languages supported
- ✅ **Isolated virtual environment** (no system package conflicts)
- ✅ **Zero manual setup** (dependencies auto-installed)
- ✅ **OAuth authentication** (secure browser-based flow)
- ✅ Integration with Claude Code workflow

## How It Works

The skill uses a modern, isolated approach:

1. **run.sh** - Generic script runner
2. **uv** - Automatically creates `.venv` and installs dependencies
3. **OAuth 2.0** - Secure authentication with Google APIs
4. **Google APIs** - Slides API for presentation access, Translation API for translations
5. **replaceAllText** - Preserves formatting while updating text

## File Structure

```
~/.claude/skills/google-slides-translator/
├── README.md                           # This file
├── SKILL.md                            # Detailed skill guide
└── scripts/
    ├── run.sh                          # Generic script runner
    ├── pyproject.toml                  # Python dependencies
    ├── .venv/                          # Auto-created virtual environment
    └── src/
        └── translate_slides.py         # Python translation script
```

## Use Cases

### 1. Translate Complete Presentation
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz all fr
```

### 2. Translate Slide Range
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 10-15 es
```

### 3. Translate Specific Slides
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 1,3,5 de
```

### 4. Translate Multiple Ranges
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 2-4,6-8 it
```

## Slide Range Formats

| Format | Description | Example |
|--------|-------------|---------|
| `all` | All slides | `all` |
| `N` | Single slide | `5` |
| `N-M` | Range of slides | `10-15` |
| `N,M,P` | Specific slides | `1,5,10` |
| `N-M,P-Q` | Multiple ranges | `2-4,6-8` |

## Supported Languages

Use 2-letter ISO 639-1 language codes:

| Language | Code | Language | Code |
|----------|------|----------|------|
| French | fr | Spanish | es |
| German | de | Italian | it |
| Portuguese | pt | Japanese | ja |
| Chinese | zh | Korean | ko |
| Arabic | ar | Russian | ru |
| Dutch | nl | Polish | pl |

And 100+ more languages supported by Google Translate!

## How to Get Presentation ID

From a Google Slides URL:
```
https://docs.google.com/presentation/d/1abc123xyz/edit
                                       ^^^^^^^^^^^
                                    Presentation ID
```

## Environment Variables

None required! The script automatically:
- Stores credentials in `~/.claude/credentials/`
- Manages authentication tokens
- Refreshes expired tokens

## Integration with Claude Code

When using this skill in Claude Code conversations:

1. **User mentions translation:** "Translate this presentation to French"
2. **Claude extracts details:** Presentation ID, slide range, target language
3. **Script runs:** Automatic authentication and translation
4. **Results reported:** Translation statistics and completion status
5. **Handle errors:** Clear troubleshooting guidance if issues occur

## Output Example

```
✅ Authenticated successfully
📊 Translating slides in presentation: 1abc123xyz
🌍 Target language: fr
📄 Slide range: all
📝 Presentation: Q4 Planning
📊 Total slides: 15
🎯 Translating 15 slide(s): [1, 2, 3, ..., 15]

🔄 Processing slide 1...
  ✅ Translated element g1234abc...
  ✅ Translated element g5678def...
  📊 Slide 1: 2 elements translated

[... continues for all slides ...]

✅ Translation complete!
📊 Slides translated: 15/15
📝 Total text elements translated: 87
```

## Troubleshooting

### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with homebrew
brew install uv
```

### OAuth credentials not found
The script will display detailed setup instructions including:
- Link to Google Cloud Console
- Steps to create OAuth credentials
- Exact path where to save the file

```bash
# Quick fix:
mkdir -p ~/.claude/credentials
# Then download and save credentials.json from Google Cloud Console
```

### APIs not enabled
```bash
gcloud services enable slides.googleapis.com
gcloud services enable translate.googleapis.com
```

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.claude/credentials/google_token.json
```

### Permission denied on run.sh
```bash
chmod +x ~/.claude/skills/google-slides-translator/scripts/run.sh
```

## Dependencies

Automatically installed by uv:
- `google-api-python-client` - Google Slides API
- `google-auth-httplib2` - Authentication
- `google-auth-oauthlib` - OAuth 2.0 flow
- `google-cloud-translate` - Translation API

## Technical Details

### Formatting Preservation
- Uses `replaceAllText` API method
- Preserves bold, italic, underline
- Maintains fonts, sizes, colors
- Retains alignment and spacing
- Preserves hyperlinks

### Translation Process
1. Authenticates with OAuth 2.0
2. Fetches presentation structure
3. Extracts text from slide elements
4. Auto-detects source language
5. Translates each text segment
6. Updates in-place with `batchUpdate`
7. Reports progress and statistics

## Limitations

- Updates original presentation (no copy created)
- Translates text only (not images with text)
- Tables not currently supported
- Requires internet connection
- Subject to Google API quotas

## Security & Privacy

- OAuth 2.0 secure authentication
- Credentials stored locally in `~/.claude/credentials/`
- Only requests minimum required API scopes
- Text sent to Google Cloud Translation API
- No logging or storage of translated content

## Performance

- **Small presentations** (<20 slides): 30-60 seconds
- **Medium presentations** (20-50 slides): 1-3 minutes
- **Large presentations** (50+ slides): 3-10 minutes
- Depends on: Slide count, text volume, network speed

## See Also

- Full skill documentation: `SKILL.md`
- Related skills: `speech-to-text`, `pdf-extractor`, `video-creator`

## Support

For issues or questions:
1. Check `SKILL.md` for detailed documentation
2. Review troubleshooting section above
3. Ensure uv is installed
4. Verify Google OAuth credentials are set up
5. Check APIs are enabled in your GCP project
