# Troubleshooting Guide

## Common Errors and Solutions

### Authentication Errors

#### "Google OAuth credentials not found"

**Problem:** The OAuth credentials file is missing.

**Solution:**
```bash
# Create credentials directory
mkdir -p ~/.claude/credentials

# Download OAuth credentials from Google Cloud Console:
# 1. Go to https://console.cloud.google.com/
# 2. Select your project
# 3. Go to APIs & Services > Credentials
# 4. Create OAuth 2.0 Client ID (Desktop application)
# 5. Download credentials.json
# 6. Save to ~/.claude/credentials/google_credentials.json
```

#### "Permission denied" or "API not enabled"

**Problem:** Required Google APIs are not enabled.

**Solution:**
```bash
# Enable all required APIs
gcloud services enable slides.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable drive.googleapis.com
```

#### "Refresh token expired"

**Problem:** The saved authentication token has expired.

**Solution:**
```bash
# Remove the old token
rm ~/.claude/credentials/google_token.json

# Re-run any command - it will prompt for re-authentication
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "Test"
```

### Presentation Errors

#### "Presentation not found"

**Problem:** Invalid presentation ID or no access to presentation.

**Solutions:**
1. Verify the presentation ID from the URL
2. Ensure you have edit access to the presentation
3. Check if the presentation was deleted

**URL format:**
```
https://docs.google.com/presentation/d/1abc123xyz/edit
                                      └─────┬─────┘
                                    Presentation ID
```

#### "Invalid slide number"

**Problem:** Slide number is out of range.

**Solution:**
```bash
# First, describe the presentation to see total slides
~/.claude/skills/google-slide-manager/scripts/run.sh manage_slides <id> describe --slide 1

# Then use valid slide numbers (1-based indexing)
```

### Translation Errors

#### "Translation quota exceeded"

**Problem:** You've exceeded the Google Cloud Translation API quota.

**Solutions:**
1. Wait for quota to reset (usually monthly)
2. Increase quota in Google Cloud Console
3. Use a different GCP project

**Check quota:**
```bash
# View quota usage in Google Cloud Console
# APIs & Services > Dashboard > Translation API > Quotas
```

#### "Invalid language code"

**Problem:** Unsupported or misspelled language code.

**Solution:**
Use valid 2-letter language codes:
- French: `fr`
- Spanish: `es`
- German: `de`
- Italian: `it`
- Portuguese: `pt`
- Japanese: `ja`
- Chinese: `zh`
- Korean: `ko`
- Arabic: `ar`
- Russian: `ru`

See complete list: [Google Cloud Translation supported languages](https://cloud.google.com/translate/docs/languages)

### Formatting Errors

#### "Failed to add text/image"

**Problem:** Invalid coordinates, size, or formatting parameters.

**Solutions:**
1. Check that x, y coordinates are within slide bounds (0-720 for width, 0-540 for height in points)
2. Verify image URLs are publicly accessible
3. Ensure color codes are valid hex format (#RRGGBB)

**Valid example:**
```bash
~/.claude/skills/google-slide-manager/scripts/run.sh format_content <id> add-text \
  --slide 1 \
  --text "Hello" \
  --x 100 --y 100 \
  --width 500 --height 100 \
  --color "#FF0000"
```

#### "Image upload failed"

**Problem:** Local file upload or invalid image URL.

**Solutions:**
1. Use publicly accessible image URLs (local file upload not yet implemented)
2. Upload image to Google Drive or image hosting service first
3. Ensure URL is direct image link, not a webpage

### Export Errors

#### "Export failed" or "Access denied"

**Problem:** No permission to export or invalid presentation.

**Solutions:**
1. Verify you have view/edit access to presentation
2. Check Drive API is enabled
3. Ensure output directory exists and is writable

```bash
# Create output directory
mkdir -p ~/Downloads

# Export with full path
~/.claude/skills/google-slide-manager/scripts/run.sh export <id> pptx ~/Downloads/presentation.pptx
```

### Installation Errors

#### "uv not found"

**Problem:** The `uv` package manager is not installed.

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"
```

#### "Module not found" or import errors

**Problem:** Dependencies not installed or virtual environment not created.

**Solution:**
```bash
# Navigate to scripts directory
cd ~/.claude/skills/google-slide-manager/scripts

# Remove old venv if exists
rm -rf .venv

# Let run.sh recreate the environment
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "Test"
```

### API Limitations

Some features have limited or no API support:

#### Animations
**Issue:** Google Slides API doesn't support adding animations programmatically.

**Workaround:** Add animations manually in Google Slides UI.

#### Transitions
**Issue:** Limited transition support in API.

**Workaround:** Set transitions manually in Google Slides UI (Slide menu > Transition).

#### Themes
**Issue:** Cannot change themes programmatically.

**Workaround:** Change theme manually (Slide menu > Change theme) or import slides from themed template.

#### Screenshots
**Issue:** No direct screenshot API.

**Workaround:**
1. Use Google Slides UI: File > Download > PNG Image
2. Use browser screenshot tools
3. Use the export PDF feature and convert pages to images

## Getting More Help

### Enable Debug Output

For more detailed error information, run Python scripts directly:

```bash
cd ~/.claude/skills/google-slide-manager/scripts
uv run src/create_presentation.py --help
```

### Check Logs

Authentication and API errors are logged to stderr. Redirect to file:

```bash
~/.claude/skills/google-slide-manager/scripts/run.sh create_presentation "Test" 2> error.log
```

### Verify Setup

1. Check uv installation:
```bash
uv --version
```

2. Check Google Cloud project:
```bash
gcloud config get-value project
```

3. Check enabled APIs:
```bash
gcloud services list --enabled | grep -E "slides|translate|drive"
```

4. Check credentials exist:
```bash
ls -la ~/.claude/credentials/
```

### Contact Support

If issues persist:
1. Check Google Cloud Console for API errors
2. Review Google Slides API documentation
3. Verify GCP billing is enabled (some APIs require billing)
4. Check API quotas and limits

## Best Practices

To avoid common issues:

1. **Always verify presentation ID** before operations
2. **Test with small presentations** first
3. **Keep backups** before major changes
4. **Monitor API quotas** for large operations
5. **Use valid parameters** (check documentation for ranges)
6. **Handle errors gracefully** in automated workflows
7. **Re-authenticate** if seeing persistent auth errors
