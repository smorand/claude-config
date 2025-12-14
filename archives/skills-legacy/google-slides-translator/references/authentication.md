# Authentication Reference

## Overview

The translation script uses Google OAuth 2.0 for secure authentication with Google Slides and Cloud Translation APIs.

## Prerequisites

### System Requirements
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Cloud Translation API enabled
- Python 3.8+ (automatically managed by uv)

### Required Google APIs
```bash
gcloud services enable slides.googleapis.com
gcloud services enable translate.googleapis.com
```

## OAuth Credentials Setup

### 1. Create OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services > Credentials**
3. Click **Create Credentials > OAuth 2.0 Client ID**
4. Select **Desktop application** as application type
5. Download credentials as JSON file
6. Save to `~/.claude/credentials/google_credentials.json`

### 2. Required OAuth Scopes

The script requires the following scopes:
- `https://www.googleapis.com/auth/presentations` - Read/write access to Google Slides
- `https://www.googleapis.com/auth/cloud-translation` - Access to Cloud Translation API

These scopes are automatically requested during the OAuth flow.

## First-Time Authentication

```bash
# 1. Create credentials directory
mkdir -p ~/.claude/credentials

# 2. Copy downloaded credentials
cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json

# 3. Run script - will open browser for OAuth consent
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> all <lang>

# 4. Follow browser prompts:
#    - Select your Google account
#    - Review requested permissions
#    - Click "Allow"

# 5. Token automatically saved to ~/.claude/credentials/google_token.json
```

## Token Management

### Token Storage
- **Credentials:** `~/.claude/credentials/google_credentials.json` (OAuth client secret)
- **Token:** `~/.claude/credentials/google_token.json` (Access/refresh tokens)

### Automatic Token Refresh
- Token automatically refreshed when expired
- No browser interaction needed after first authentication
- Seamless re-authentication

### Manual Token Reset
```bash
# Delete existing token to force re-authentication
rm ~/.claude/credentials/google_token.json

# Run script again to trigger new OAuth flow
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> all <lang>
```

## Security Best Practices

- **Local storage:** Credentials stored in `~/.claude/credentials/` (user-only access)
- **Minimum scopes:** Only requests required API scopes
- **No logging:** Script does not log or store credentials
- **OAuth 2.0:** Industry-standard secure authentication flow

## Permission Requirements

### GCP Project
- Cloud Translation API enabled
- Sufficient quota for translation requests

### Google Slides
- View or edit access to target presentation
- Shared presentations work if you have appropriate access

## Troubleshooting Authentication

See `troubleshooting.md` for detailed authentication error resolution.
