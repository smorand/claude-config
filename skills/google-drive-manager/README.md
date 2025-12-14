# Google Drive Manager Skill

Expert skill for managing Google Drive files and folders. Search, copy, move, upload, download, share, and organize files with comprehensive Drive operations.

## Overview

This skill enables comprehensive Google Drive file management through a command-line interface. Perform all essential Drive operations including searching, uploading, downloading with smart export for Google Workspace files, copying, moving, creating folders, sharing, and more.

## Quick Start

### Prerequisites

- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Drive API enabled
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

# 4. Enable required API
gcloud services enable drive.googleapis.com
```

### Basic Usage

```bash
# Search for files
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'report' --limit 10

# Upload a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload document.pdf

# Download a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1abc123xyz output.pdf

# Copy a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy 1abc123xyz --name 'Copy of Document'

# Move a file to folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager move 1abc123xyz 1folder456

# Share a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role writer

# Get file path hierarchy
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager path 1abc123xyz

# List file permissions
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions 1abc123xyz

# Share with anyone (public)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone 1abc123xyz --role reader

# Remove public access
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-public 1abc123xyz

# List folder contents
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager list-folder 1folder123xyz --limit 50

# Rename file or folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager rename 1abc123xyz 'New Name'
```

**First run:** May take a few seconds to create the virtual environment and install dependencies. A browser window will open for OAuth authentication. Subsequent runs are instant and automatic!

## Features

- ✅ Search by name, query, or MIME type (includes files "Shared with me")
- ✅ Upload files with optional parent folder
- ✅ Download with smart export for Google Workspace files (Docs→PDF, Sheets→XLSX, Slides→PPTX)
- ✅ Copy files with optional renaming
- ✅ Move files between folders
- ✅ Create and delete folders
- ✅ Share files with specific permissions (users, groups, or anyone with the link)
- ✅ **List and manage file permissions** (view who has access, remove access)
- ✅ **Public sharing** (make files accessible to anyone with the link)
- ✅ Get detailed file information
- ✅ **Get full path hierarchy** (shows complete folder structure from root to file)
- ✅ **List folder contents** (browse files and subfolders inside any folder)
- ✅ **Rename files and folders** (change names without moving)
- ✅ **Isolated virtual environment** (no system package conflicts)
- ✅ **Zero manual setup** (dependencies auto-installed)
- ✅ **OAuth authentication** (secure browser-based flow)
- ✅ Integration with Claude Code workflow

## How It Works

The skill uses a modern, isolated approach:

1. **run.sh** - Generic script runner
2. **uv** - Automatically creates `.venv` and installs dependencies
3. **OAuth 2.0** - Secure authentication with Google APIs
4. **Google Drive API** - Comprehensive file and folder operations

## File Structure

```
~/.claude/skills/google-drive-manager/
├── README.md                           # This file
├── SKILL.md                            # Detailed skill guide
└── scripts/
    ├── run.sh                          # Generic script runner
    ├── pyproject.toml                  # Python dependencies
    ├── .venv/                          # Auto-created virtual environment
    └── src/
        └── drive_manager.py            # Python Drive manager script
```

## Use Cases

### 1. Search Files

```bash
# Search by name
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'Q4 Report'

# Search by MIME type
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --mime-type 'application/pdf' --limit 20

# Advanced query
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --query "name contains 'report' and modifiedTime > '2024-01-01'"
```

### 2. Upload Files

```bash
# Upload to root
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload report.pdf

# Upload to specific folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload report.pdf --parent 1folder123
```

### 3. Download Files

```bash
# Download regular file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1abc123xyz report.pdf

# Download Google Doc as PDF (auto-convert)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1googledoc123 report.pdf
```

### 4. Copy Files

```bash
# Copy with new name
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy 1abc123xyz --name 'Report Copy'

# Copy to different folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy 1abc123xyz --parent 1folder456
```

### 5. Move Files

```bash
# Move file to folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager move 1abc123xyz 1folder456
```

### 6. Create Folders

```bash
# Create folder in root
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager create-folder 'Q4 Reports'

# Create subfolder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager create-folder 'January' --parent 1reports456
```

### 7. Share Files

```bash
# Share as reader (default)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com

# Share as writer
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role writer

# Share as commenter without notification
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role commenter --no-notify
```

### 8. Get File Information

```bash
# Get detailed file info
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager info 1abc123xyz
```

### 9. Delete Files/Folders

```bash
# Delete a file or folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager delete 1abc123xyz
```

### 10. List Folder Contents

```bash
# List all files in a folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager list-folder 1folder123

# List with limit
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager list-folder 1folder123 --limit 50
```

### 11. Rename Files/Folders

```bash
# Rename a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager rename 1abc123xyz 'New Report Name'

# Rename a folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager rename 1folder123 'Q4 Reports'
```

## Commands Reference

| Command | Description | Required Args | Optional Args |
|---------|-------------|---------------|---------------|
| `search` | Search for files | - | `--query`, `--name`, `--mime-type`, `--limit` |
| `upload` | Upload file | `file_path` | `--parent`, `--mime-type` |
| `download` | Download file | `file_id`, `output_path` | `--convert-to` |
| `copy` | Copy file | `file_id` | `--name`, `--parent` |
| `move` | Move file | `file_id`, `folder_id` | - |
| `create-folder` | Create folder | `name` | `--parent` |
| `delete` | Delete file/folder | `file_id` | - |
| `share` | Share file | `file_id`, `email` | `--role`, `--no-notify` |
| `info` | Get file info | `file_id` | - |
| `list-folder` | List folder contents | `folder_id` | `--limit` |
| `rename` | Rename file/folder | `file_id`, `new_name` | - |

## Common MIME Types

| Type | MIME String |
|------|-------------|
| PDF | `application/pdf` |
| JPEG Image | `image/jpeg` |
| PNG Image | `image/png` |
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Folder | `application/vnd.google-apps.folder` |
| Word Document | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Excel Spreadsheet | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

## Permission Roles

| Role | Description |
|------|-------------|
| `reader` | Can view and download |
| `writer` | Can edit |
| `commenter` | Can comment but not edit |
| `owner` | Full control (transfer ownership) |

## How to Get File ID

From a Google Drive URL:
```
https://drive.google.com/file/d/1abc123xyz/view
                                ^^^^^^^^^^^
                                 File ID

https://drive.google.com/drive/folders/1folder456
                                        ^^^^^^^^^^
                                        Folder ID
```

Or use the search command to find files and get their IDs.

## Environment Variables

None required! The script automatically:
- Stores credentials in `~/.claude/credentials/`
- Manages authentication tokens
- Refreshes expired tokens

## Integration with Claude Code

When using this skill in Claude Code conversations:

1. **User mentions Drive operation:** "Search for reports in my Drive"
2. **Claude extracts details:** Operation type, search criteria, file IDs
3. **Script runs:** Automatic authentication and execution
4. **Results reported:** File listings, operation status, file IDs
5. **Handle errors:** Clear troubleshooting guidance if issues occur

## Output Examples

### Search Output
```
✅ Authenticated successfully
🔍 Searching for files...

✅ Found 2 file(s):

📄 Q4 Report Final.pdf
   ID: 1abc123xyz
   Type: application/pdf
   Size: 245.67 KB
   Link: https://drive.google.com/file/d/1abc123xyz/view

📄 Q4 Report Draft.docx
   ID: 1def456uvw
   Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
   Size: 123.45 KB
   Link: https://drive.google.com/file/d/1def456uvw/view
```

### Upload Output
```
✅ Authenticated successfully
📤 Uploading report.pdf...
✅ File uploaded successfully!
   Name: report.pdf
   ID: 1newfile123
   Link: https://drive.google.com/file/d/1newfile123/view
```

### Download Output
```
✅ Authenticated successfully
📥 Downloading file...
✅ File downloaded to: report.pdf
```

### Share Output
```
✅ Authenticated successfully
🔗 Sharing file...
✅ File shared successfully with user@example.com as writer!
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

### API not enabled
```bash
gcloud services enable drive.googleapis.com
```

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.claude/credentials/google_token.json
```

### Permission denied on run.sh
```bash
chmod +x ~/.claude/skills/google-drive-manager/scripts/run.sh
```

## Dependencies

Automatically installed by uv:
- `google-api-python-client` - Google Drive API
- `google-auth-httplib2` - Authentication
- `google-auth-oauthlib` - OAuth 2.0 flow

## Technical Details

### Smart Export
When downloading Google Workspace files, the script automatically exports to common formats:
- Google Docs → PDF
- Google Sheets → XLSX
- Google Slides → PPTX

You can override with `--convert-to` parameter.

### Query Syntax
Google Drive supports rich query syntax for advanced searches:
```
name contains 'report'
mimeType = 'application/pdf'
modifiedTime > '2024-01-01'
'me' in owners
trashed = false
```

Combine queries with `and` and `or` operators.

## Limitations

- Requires internet connection
- Subject to Google API quotas
- Large file operations may take time
- Shared drives not currently supported

## Security & Privacy

- OAuth 2.0 secure authentication
- Credentials stored locally in `~/.claude/credentials/`
- Only requests minimum required API scopes
- No logging or storage of file content
- All transfers use HTTPS

## Performance

- **Small files** (<10MB): Near instant
- **Medium files** (10-100MB): Few seconds
- **Large files** (100MB+): Minutes depending on network
- **Search operations**: Sub-second response
- Depends on: File size, network speed, API quotas

## See Also

- Full skill documentation: `SKILL.md`
- Related skills: `google-slides-translator`, `pdf-extractor`

## Support

For issues or questions:
1. Check `SKILL.md` for detailed documentation
2. Review troubleshooting section above
3. Ensure uv is installed
4. Verify Google OAuth credentials are set up
5. Check Drive API is enabled in your GCP project
