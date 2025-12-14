# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code skill for managing Office 365 professional emails and calendar through Microsoft Graph API. It uses OAuth 2.1 with PKCE (Proof Key for Code Exchange) for secure authentication without client secrets.

**Important Scope**: This skill is ONLY for professional L'Oréal Office 365 emails. For personal Gmail emails, use the `email-manager` skill instead.

## Architecture

### Implementation

**CRITICAL**: This skill has been migrated from Python to **Go** (as of December 2025).

- **Binary**: `scripts/o365-manager` - Compiled Go binary (macOS ARM64)
- **No Python dependencies** - Self-contained executable
- **Environment Variables Required**:
  - `O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36`
  - `O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba`

### Authentication Flow
- **OAuth 2.1 PKCE**: Public client flow without client secret
- **Token Management**: Access tokens auto-refresh when expired (1-hour lifetime)
- **Token Storage**: `~/.claude/credentials/o365_tokens.json`
- **Local Callback Server**: Temporary HTTP server on port 33418 for OAuth redirect
- **Token Format**: Go version requires `expires_at` as integer (not float)

### Microsoft Graph API Integration
- Base URL: `https://graph.microsoft.com/v1.0`
- Email endpoints: `/me/messages`, `/me/mailFolders/{folder}/messages`, `/me/sendMail`
- Calendar endpoints: `/me/calendar/events`
- Required scopes: Mail.ReadWrite, Mail.Send, Calendars.ReadWrite, User.Read

## Development Commands

### Running the Tool

**CRITICAL**: Always set environment variables before running commands:

```bash
export O365_CLIENT_ID=76d42bf5-d461-4274-bd4d-a02576b9df36
export O365_TENANT_ID=e4e1abd9-eac7-4a71-ab52-da5c998aa7ba
```

All commands use the Go binary directly:

```bash
# From skill directory
./scripts/o365-manager <category> <command> [flags]

# From anywhere
~/.claude/skills/o365-manager/scripts/o365-manager <category> <command> [flags]
```

### Common Commands

**Email Operations:**
```bash
# List emails
./scripts/o365-manager email list --limit 20 --unread

# Read specific email
./scripts/o365-manager email read <message_id>

# Send email (always use --body-type HTML for formatted emails)
./scripts/o365-manager email send --to addr@loreal.com --subject "Subject" --body "Body" --body-type HTML

# Send with attachments
./scripts/o365-manager email send --to addr@loreal.com --subject "Subject" --body "Body" --body-type HTML --attachments /path/to/file1,/path/to/file2

# Create draft
./scripts/o365-manager email create-draft --to addr@loreal.com --subject "Subject" --body "Body" --body-type HTML

# List folders
./scripts/o365-manager email list-folders

# Archive email
./scripts/o365-manager email archive <message_id>
```

**Calendar Operations:**
```bash
# ⚠️ WARNING: Calendar list commands have a DATE FORMATTING BUG in current Go binary
# The binary generates malformed timestamps like "2110:299:299"
# This affects --days and --days-back parameters
# Email operations work correctly

# List upcoming events (CURRENTLY BROKEN - see bug above)
./scripts/o365-manager calendar list --days 7

# Create event
./scripts/o365-manager calendar create \
  --subject "Meeting" \
  --start "2025-11-12T14:00:00" \
  --end "2025-11-12T15:00:00" \
  --attendees "alice@loreal.com,bob@loreal.com" \
  --location "Conference Room"

# Respond to event
./scripts/o365-manager calendar respond <event_id> --response accept
```

**Authentication:**
```bash
# Force re-authentication
./scripts/o365-manager auth
```

### Dependency Management

**No dependencies required** - the Go binary is self-contained.

To rebuild from source (if needed):
```bash
# Requires Go 1.21+ installed
cd <source-directory>
go build -o o365-manager
```

## Known Issues

### ⚠️ Calendar List Bug

**CRITICAL**: The current Go binary has a **date formatting bug** affecting calendar list operations:
- Commands: `calendar list --days N` and `calendar list --days-back N`
- Error: Generates malformed timestamps like `2110:299:299` instead of proper ISO 8601
- Impact: Calendar listing is **currently broken**
- Status: Needs to be fixed in the Go source code
- Workaround: None available - calendar list operations are non-functional

**Working commands:**
- ✅ All email operations (list, read, send, archive, etc.)
- ✅ Calendar create, update, delete, respond (if you have event IDs from other sources)
- ✅ Authentication

**Broken commands:**
- ❌ `calendar list --days N`
- ❌ `calendar list --days-back N`

### Token Format Compatibility

When migrating from Python to Go version:
- Python version stored `expires_at` as float (e.g., `1765551132.046113`)
- Go version requires `expires_at` as integer (e.g., `1765551132`)
- **Fix**: Convert float to int in token file: `python3 -c "import json; d=json.load(open('~/.claude/credentials/o365_tokens.json')); d['expires_at']=int(d['expires_at']); json.dump(d,open('~/.claude/credentials/o365_tokens.json','w'))"`

## Code Architecture Details

### Attachment Handling

**Email attachments**:
- Files encoded as base64 in message payload
- Multiple files supported (comma-separated paths)
- 4MB total request size limit (Microsoft Graph API)
- Implemented in email send and create-draft commands

**Calendar event attachments**:
- Separate workflow: list events → query attachments endpoint → download
- **Important**: `get` command does NOT return attachments - must query `/me/events/{id}/attachments` separately

### Token Refresh Logic

Access tokens are automatically refreshed:
- Checks if token expires in < 5 minutes
- Uses refresh token to get new access token
- Falls back to full re-authentication if refresh fails
- Updates `expires_at` timestamp for future checks
- **Note**: Token file must have `expires_at` as integer (not float)

## Configuration

### Azure AD Application
- **Client ID**: 76d42bf5-d461-4274-bd4d-a02576b9df36
- **Tenant ID**: e4e1abd9-eac7-4a71-ab52-da5c998aa7ba (L'Oréal)
- **Redirect URI**: http://127.0.0.1:33418 (exact match required, no trailing slash)
- **Type**: Public client with PKCE enabled

### Email Filtering Rules (Legacy - Not in Go version)

The Python version had inbox processing with `email_rules.json`:
- `vip_senders`: Auto-mark as important
- `partner_whitelist`: Technology partners to keep
- `auto_archive_keywords`: External recruitment spam keywords
- `auto_archive_domains`: Spam domains to auto-archive
- `system_emails`: System emails requiring action
- `auto_archive_subjects`: Subject patterns to auto-archive

### Default Settings
- **Timezone**: **CRITICAL** - Always detect local timezone using `date "+%Z"` command. Default is Europe/Paris but MUST be overridden with detected timezone using `--timezone` parameter
- **Email body type**: HTML (recommended for all professional emails)
- **Date format**: ISO 8601 (YYYY-MM-DDTHH:MM:SS)

## Testing

### Manual Testing

Test authentication:
```bash
./scripts/run.sh auth
```

Test email operations:
```bash
./scripts/run.sh list-emails --limit 5
./scripts/run.sh list-folders
```

Test inbox processing (dry-run first):
```bash
./scripts/run.sh process-inbox --limit 10 --dry-run
```

### Debugging

Enable verbose output by examining error messages in stderr. The script uses proper exception handling with traceback.

Common issues:
- **"Invalid redirect URI"**: Check Azure AD app has exactly `http://127.0.0.1:33418`
- **Token refresh failed**: Run `./scripts/run.sh auth` to re-authenticate
- **Port 33418 in use**: Kill process using the port or restart OAuth flow

## Important Notes for Claude

1. **Always use HTML body type** for professional emails: `--body-type HTML`
2. **Attachments are comma-separated**: Multiple files use commas, not spaces
3. **Event attachments require two-step process**: List events → query attachments API → download
4. **Dry-run before processing inbox**: Always test with `--dry-run` first
5. **JSON output**: All list/read commands return JSON for parsing
6. **Error handling**: Script exits with non-zero status on failure
7. **Token auto-refresh**: Access tokens refresh automatically; re-auth only if refresh token expires
8. **Search limitations**: `$search` parameter cannot be combined with `$orderby` in Microsoft Graph API
9. **CRITICAL - Date & Time Handling**: When the user mentions dates/times for calendar events or email filters:
   - **ALWAYS determine the local timezone first** by running: `date "+%Z"`
   - Use the detected timezone (not the default Europe/Paris) for all operations
   - Convert user-provided times to the local timezone
   - Example: If user says "tomorrow at 2PM", run `date` to get current date/time and timezone, then calculate the correct ISO 8601 timestamp

## Modifying This Skill

### CRITICAL: SKILL.md Updates Required

**IMPORTANT**: Whenever the user requests a modification to this skill (new features, bug fixes, configuration changes, etc.), you MUST follow this workflow:

1. **Implement the code changes** in the appropriate files (Python scripts, JSON configs, etc.)
2. **ALWAYS ask the user for approval BEFORE modifying SKILL.md** with a message like:
   - "I've implemented the changes. Should I now update SKILL.md to document this new functionality?"
   - "The feature is working. May I update SKILL.md to reflect these changes?"
3. **Update SKILL.md with AI-optimized documentation** that:
   - Uses clear trigger keywords for Claude to recognize when to use the skill
   - Provides concrete command examples with the new functionality
   - Explains the workflow and expected behavior
   - Is structured for LLM comprehension (clear sections, bullet points, examples)
4. **Update this CLAUDE.md file** if the changes affect architecture, development commands, or important implementation details

### SKILL.md Optimization Guidelines

When updating SKILL.md (after user approval):
- **Use bold keywords** for trigger phrases (e.g., "**Use this skill whenever the user mentions**")
- **Provide exact command syntax** with all parameters
- **Include workflow examples** showing step-by-step usage
- **Highlight limitations and gotchas** that Claude should be aware of
- **Use consistent formatting** with the existing SKILL.md structure
- **Add new commands to "Available Commands" section** with complete documentation
- **Update "Usage Examples" section** to demonstrate the new functionality

### Example Modification Workflow

User: "Add a feature to forward emails"

1. Implement `forward_email()` function in `o365_manager.py`
2. Add CLI command handling in `main()`
3. Test the functionality
4. **Ask user**: "I've implemented email forwarding. Should I update SKILL.md to document this new command?"
5. **After user approval**: Update SKILL.md with:
   - New command syntax in "Available Commands"
   - Usage example in "Usage Examples"
   - Trigger keywords if needed
6. Update this CLAUDE.md if architecture changed

## Related Skills

- **email-manager**: For personal Gmail emails (DO NOT use this skill for personal emails)
- **google-docs-manager**: For creating/editing Google Docs
- **google-drive-manager**: For file management in Google Drive
