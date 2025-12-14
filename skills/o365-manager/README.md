# Office 365 Manager Skill

A Claude Code skill for managing Office 365 emails and calendar through Microsoft Graph API using OAuth 2.1 PKCE authentication.

## Overview

This skill provides comprehensive email and calendar management capabilities for L'Oréal Office 365 accounts. It uses OAuth 2.1 with PKCE (Proof Key for Code Exchange) for secure authentication without requiring client secrets.

## Features

### Email Management
- **List emails** with filters (folder, unread, search)
- **Read email** content with full details and attachments
- **Send email** to one or multiple recipients
- **Reply to email** with automatic threading
- **Mark emails** as read/unread
- **Move emails** to any folder
- **Archive emails** (quick move to Archive folder)
- **Delete emails**
- **List folders** to see available destinations
- **Search emails** across mailbox

### Calendar Management
- **List upcoming events** with customizable time range
- **Get event details** including attendees and online meeting links
- **Create events** with attendees, location, and description
- **Update events** (change time, location, attendees)
- **Delete events**

## Setup

### Prerequisites

1. Python 3.7+ with the following packages:
   ```bash
   pip install requests
   ```

2. Azure AD application configured with:
   - Client ID: `76d42bf5-d461-4274-bd4d-a02576b9df36`
   - Public client with PKCE enabled
   - Redirect URI: `http://127.0.0.1:33418`
   - Required permissions: Mail.ReadWrite, Mail.Send, Calendars.ReadWrite, User.Read

### Installation

The skill is installed in `~/.claude/skills/o365-manager/` with:
- `scripts/run.sh` - Wrapper script using uv for dependency management
- `scripts/src/o365_manager.py` - Main Python script
- `scripts/pyproject.toml` - Python project dependencies
- `SKILL.md` - Skill prompt for Claude
- `README.md` - This file

Credentials are stored in `~/.claude/credentials/`:
- `o365_tokens.json` - OAuth tokens (auto-managed)
- `btdp-app-pd-prd_creds.json` - Service principal credentials (reference only)

### First-Time Authentication

On first use, the script will:
1. Open your default browser
2. Redirect to Microsoft login
3. Ask for consent to access your email and calendar
4. Save refresh token for future use

To force re-authentication:
```bash
~/.claude/skills/o365-manager/scripts/run.sh auth
```

## Usage

### With Claude Code

Simply ask Claude to perform email or calendar operations:

**Email Examples:**
- "Show me my unread emails"
- "Read the latest email from Alice"
- "Send an email to bob@loreal.com about the project status"
- "Reply to the email about the meeting"
- "Archive this email"
- "Move this email to my Archive folder"
- "What folders do I have?"
- "Search for emails about budget"

**Calendar Examples:**
- "What meetings do I have this week?"
- "Schedule a meeting with Alice tomorrow at 2PM"
- "Show me the details of my next meeting"
- "Cancel the meeting with Bob on Friday"

### Command Line

The script can also be used directly from the command line.

#### Email Commands

**List inbox emails:**
```bash
./scripts/run.sh list-emails --limit 20
```

**List unread emails:**
```bash
./scripts/run.sh list-emails --unread --limit 10
```

**Search emails:**
```bash
./scripts/run.sh search-emails --query "project budget" --limit 20
```

**Read specific email:**
```bash
./scripts/run.sh read-email <message_id>
```

**Send email:**
```bash
./scripts/run.sh send-email \
  --to alice@loreal.com,bob@loreal.com \
  --subject "Project Update" \
  --body "Here is the latest update..." \
  --cc charlie@loreal.com
```

**Reply to email:**
```bash
./scripts/run.sh reply-email <message_id> \
  --comment "Thanks for the update!"
```

**Mark as read:**
```bash
./scripts/run.sh mark-read <message_id>
```

**Delete email:**
```bash
./scripts/run.sh delete-email <message_id>
```

**Move email to folder:**
```bash
./scripts/run.sh move-email <message_id> --folder "Archive"
```

**Archive email:**
```bash
./scripts/run.sh archive-email <message_id>
```

**List available folders:**
```bash
./scripts/run.sh list-folders
```

#### Calendar Commands

**List upcoming events (next 7 days):**
```bash
./scripts/run.sh list-events --days 7
```

**Get event details:**
```bash
./scripts/run.sh get-event <event_id>
```

**Create event:**
```bash
./scripts/run.sh create-event \
  --subject "Team Meeting" \
  --start "2025-11-12T14:00:00" \
  --end "2025-11-12T15:00:00" \
  --attendees "alice@loreal.com,bob@loreal.com" \
  --location "Conference Room A" \
  --body "Discussing Q4 objectives" \
  --timezone "Europe/Paris"
```

**Update event:**
```bash
./scripts/run.sh update-event <event_id> \
  --subject "Updated: Team Meeting" \
  --start "2025-11-12T15:00:00" \
  --end "2025-11-12T16:00:00"
```

**Delete event:**
```bash
./scripts/run.sh delete-event <event_id>
```

## Technical Details

### Authentication Flow

1. **PKCE Code Verifier & Challenge**: Generated using SHA-256 hash
2. **Authorization Request**: Opens browser with code_challenge
3. **User Consent**: User logs in and grants permissions
4. **Token Exchange**: Code exchanged for access and refresh tokens
5. **Token Storage**: Tokens saved to `~/.claude/credentials/o365_tokens.json`
6. **Auto Refresh**: Access token automatically refreshed when expired

### API Endpoints

The script uses Microsoft Graph API v1.0:
- Base URL: `https://graph.microsoft.com/v1.0`
- Email: `/me/messages`, `/me/mailFolders/{folder}/messages`
- Calendar: `/me/calendar/events`
- Send: `/me/sendMail`

### Permissions Required

- `Mail.ReadWrite` - Read and write access to user's mail
- `Mail.Send` - Send mail as the user
- `Calendars.ReadWrite` - Read and write access to user's calendar
- `User.Read` - Read user's profile

### Token Management

- **Access Token**: Valid for 1 hour, automatically refreshed
- **Refresh Token**: Long-lived, used to obtain new access tokens
- **Storage**: Tokens stored in `~/.claude/credentials/o365_tokens.json` with 0600 permissions
- **Re-auth**: Required only if refresh token expires (rare)

## Security

- **No Client Secret**: Uses PKCE flow (public client)
- **Local Redirect**: OAuth callback on localhost only
- **Secure Storage**: Token file permissions set to 0600 (owner read/write only)
- **Automatic Cleanup**: No secrets in environment variables or command history

## Troubleshooting

### Authentication Issues

**Problem**: Browser doesn't open
**Solution**: Manually open the URL displayed in terminal

**Problem**: "Invalid redirect URI"
**Solution**: Verify the redirect URI is exactly `http://127.0.0.1:33418` (no trailing slash)

**Problem**: Token refresh failed
**Solution**: Run `./scripts/run.sh auth` to re-authenticate

### API Errors

**Problem**: "Insufficient privileges"
**Solution**: Verify all required permissions are granted in Azure AD app

**Problem**: "Resource not found"
**Solution**: Check that the message_id or event_id is correct

**Problem**: Rate limiting
**Solution**: Reduce request frequency; Microsoft Graph has throttling limits

### Python Dependencies

Dependencies are automatically managed by `uv`. If you need to manually sync:
```bash
cd ~/.claude/skills/o365-manager/scripts
uv sync
```

## File Structure

```
~/.claude/skills/o365-manager/
├── README.md                      # This file
├── SKILL.md                       # Skill prompt for Claude
└── scripts/
    ├── run.sh                     # Wrapper script (main entry point)
    ├── pyproject.toml             # Python project dependencies
    ├── uv.lock                    # Locked dependencies
    ├── .venv/                     # Virtual environment (auto-created)
    └── src/
        └── o365_manager.py        # Main Python script

~/.claude/credentials/
├── o365_tokens.json               # OAuth tokens (auto-generated)
└── btdp-app-pd-prd_creds.json    # Service principal creds (reference)
```

## Environment

- **Tenant**: L'Oréal (e4e1abd9-eac7-4a71-ab52-da5c998aa7ba)
- **Client Application**: BTDP OAuth Client (76d42bf5-d461-4274-bd4d-a02576b9df36)
- **Default Timezone**: Europe/Paris
- **API Version**: Microsoft Graph v1.0

## Examples

### Workflow 1: Check and Reply to Important Email

```bash
# List unread emails
./scripts/run.sh list-emails --unread --limit 10

# Read specific email (copy ID from previous command)
./scripts/run.sh read-email AAMkAG...

# Reply to email
./scripts/run.sh reply-email AAMkAG... --comment "Will do, thanks!"

# Mark as read
./scripts/run.sh mark-read AAMkAG...
```

### Workflow 2: Schedule a Meeting

```bash
# Check calendar availability
./scripts/run.sh list-events --days 7

# Create meeting
./scripts/run.sh create-event \
  --subject "1:1 with Manager" \
  --start "2025-11-13T10:00:00" \
  --end "2025-11-13T10:30:00" \
  --attendees "manager@loreal.com" \
  --location "Teams" \
  --timezone "Europe/Paris"
```

### Workflow 3: Email Inbox Cleanup

```bash
# List available folders
./scripts/run.sh list-folders

# Search for old newsletters
./scripts/run.sh search-emails --query "newsletter" --limit 50

# Archive unwanted emails (use IDs from search results)
./scripts/run.sh archive-email AAMkAG...
./scripts/run.sh archive-email AAMkAG...

# Or move spam to Junk Email folder
./scripts/run.sh move-email AAMkAG... --folder "Junk Email"
```

## Maintenance

### Token Expiration

- Access tokens expire after 1 hour but are auto-refreshed
- Refresh tokens are long-lived (90 days by default)
- Re-authentication only needed if refresh token expires or is revoked

### Updating Permissions

If new permissions are needed:
1. Update the Azure AD app registration
2. Delete `~/.claude/credentials/o365_tokens.json`
3. Run `./scripts/run.sh auth` to re-consent

## Support

For issues or questions:
1. Check this README's Troubleshooting section
2. Verify Azure AD app configuration
3. Review error messages in script output
4. Contact BTDP team for assistance

## License

Internal L'Oréal BTDP tool. Not for external distribution.
