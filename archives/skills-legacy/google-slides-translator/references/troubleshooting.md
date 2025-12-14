# Troubleshooting Guide

## Authentication Errors

### "Google OAuth credentials not found"

**Cause:** Missing OAuth credentials file.

**Solution:**
```bash
# 1. Create credentials directory
mkdir -p ~/.claude/credentials

# 2. Download OAuth credentials from Google Cloud Console:
#    https://console.cloud.google.com/
#    Navigate to: APIs & Services > Credentials
#    Create OAuth 2.0 Client ID (Desktop application type)

# 3. Save to correct location
cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json
```

The script will provide detailed instructions if credentials are missing.

### "Permission denied" or "Insufficient authentication scopes"

**Cause:** Required APIs not enabled or incorrect OAuth scopes.

**Solution:**
```bash
# Enable required APIs
gcloud services enable slides.googleapis.com
gcloud services enable translate.googleapis.com

# Delete token and re-authenticate with correct scopes
rm ~/.claude/credentials/google_token.json

# Run script to trigger new OAuth flow
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> all <lang>
```

**Required scopes:**
- `https://www.googleapis.com/auth/presentations`
- `https://www.googleapis.com/auth/cloud-translation`

### "Authentication browser not opening"

**Cause:** OAuth flow not triggering or browser blocked.

**Solution:**
```bash
# 1. Delete existing token
rm ~/.claude/credentials/google_token.json

# 2. Run script again to trigger new OAuth flow
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> all <lang>

# 3. Manually open the URL if browser doesn't auto-open
#    The script will display the authorization URL
```

## Presentation Errors

### "Presentation not found"

**Cause:** Invalid presentation ID or insufficient access permissions.

**Solution:**
- Verify presentation ID is correct (extract from URL)
- Ensure you have view/edit access to the presentation
- Check presentation is not deleted or in trash
- Verify you're authenticated with the correct Google account

**Example URL:**
```
https://docs.google.com/presentation/d/1abc123xyz/edit
                                     ^^^^^^^^^^^
                                     This is the ID
```

### "Unable to fetch presentation"

**Cause:** Network issues or API availability.

**Solution:**
- Check internet connection
- Verify Google APIs are accessible
- Retry after a few moments
- Check [Google Cloud Status Dashboard](https://status.cloud.google.com/)

## Translation Errors

### "Translation API quota exceeded"

**Cause:** Exceeded Google Cloud Translation API quota limits.

**Solution:**
- Check quota in [Google Cloud Console](https://console.cloud.google.com/apis/api/translate.googleapis.com/quotas)
- Request quota increase if needed
- Wait for quota to reset (usually daily)
- Implement batching for very large presentations

### "Translation failed for element"

**Cause:** Specific text element cannot be translated.

**Solution:**
- Script continues with remaining elements
- Check output for specific element IDs that failed
- Manually review and translate failed elements if needed
- Re-run script to retry failed elements

### "Source language detection failed"

**Cause:** Text not clear enough for auto-detection.

**Solution:**
- Ensure source text is well-written
- Check for mixed languages in single text element
- Verify text is not just numbers or special characters

## System Errors

### "uv not found"

**Cause:** uv package manager not installed.

**Solution:**
```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with homebrew
brew install uv

# Or with pip
pip install uv
```

### "Permission denied: run.sh"

**Cause:** Script not executable.

**Solution:**
```bash
chmod +x ~/.claude/skills/google-slides-translator/scripts/run.sh
```

### "Virtual environment creation failed"

**Cause:** Insufficient permissions or disk space.

**Solution:**
```bash
# Check disk space
df -h ~/.claude/skills/google-slides-translator/scripts/

# Check permissions
ls -la ~/.claude/skills/google-slides-translator/scripts/

# Manually create venv
cd ~/.claude/skills/google-slides-translator/scripts/
uv venv

# Try running script again
./run.sh translate_slides <id> all <lang>
```

## Network Errors

### "Connection timeout"

**Cause:** Network connectivity issues.

**Solution:**
- Check internet connection
- Verify firewall not blocking Google APIs
- Try again with stable network
- Check proxy settings if behind corporate firewall

### "SSL certificate verification failed"

**Cause:** SSL/TLS certificate issues.

**Solution:**
- Update system certificates
- Check system date/time is correct
- Verify corporate proxy not intercepting SSL

## Common Issues

### Partial translation (some elements missing)

**Cause:** Some text elements failed to translate.

**Solution:**
- Check output for error messages
- Script continues on errors, reports at end
- Re-run script to retry failed elements
- Manually translate any remaining elements

### Formatting changes after translation

**Cause:** Text length changed significantly.

**Solution:**
- This is expected for languages with different text lengths
- Review slides and adjust layouts manually if needed
- Script preserves formatting but not layout constraints

### Special characters not translating correctly

**Cause:** Character encoding issues.

**Solution:**
- Google Cloud Translation API handles most Unicode
- Check source text encoding
- Report specific character issues to Google Cloud support

## Debug Mode

For detailed debugging:

```bash
# Add verbose output (if implemented)
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> all <lang> --verbose

# Check script logs
cat ~/.claude/skills/google-slides-translator/scripts/translation.log
```

## Getting Help

If issues persist:

1. **Check Google Cloud Console** for API errors and quota
2. **Review OAuth consent screen** configuration
3. **Verify billing enabled** on GCP project
4. **Check script output** for specific error messages
5. **Review API documentation**:
   - [Google Slides API](https://developers.google.com/slides/api)
   - [Cloud Translation API](https://cloud.google.com/translate/docs)

## Known Limitations

- **No table support:** Table cells not translated
- **Images with text:** OCR not performed on images
- **Charts:** Chart text not extracted/translated
- **Embedded objects:** Only native text elements processed
- **In-place updates:** Original presentation modified (no copy)
