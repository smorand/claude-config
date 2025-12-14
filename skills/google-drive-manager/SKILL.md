---
name: google-drive-manager
description: Expert in Google Drive file management. Use when searching, copying, moving, uploading, downloading, sharing, or managing files and folders in Google Drive.
---

# Google Drive Manager Skill

Expert in managing Google Drive files and folders with comprehensive operations including search, copy, move, upload, download, share, and delete.

## Core Capabilities

- Search files by name, query, or MIME type
- Upload files to Google Drive
- Download files from Google Drive (with smart export for Google Workspace files)
- Copy files with optional renaming and parent folder
- Move files between folders
- Create and delete folders
- Share files with specific permissions (users, groups, or anyone with the link)
- List, add, and remove file permissions
- Get detailed file information including full path hierarchy
- List folder contents (browse files and subfolders inside any folder)
- Rename files and folders

## When to Use This Skill

Use this skill when users request:
- "Search for files named 'report' in Google Drive"
- "Upload this document to my Drive"
- "Download the file with ID xyz123"
- "Copy this spreadsheet to another folder"
- "Move this file to the Reports folder"
- "Create a new folder called 'Q4 Reports'"
- "Share this file with user@example.com as editor"
- "Get information about this Drive file"
- "Where is this file located?" or "Show me the path of this file" (use info command)
- "In which folder is this file located?" or "What's the folder path for this file?" (use info command)
- "Who has access to this file?" or "List permissions for this file"
- "Make this file public" or "Share with anyone who has the link"
- "Remove public access" or "Make this file private again"
- "Remove user@example.com access to this file"
- "List all files in this folder" or "Show me what's in folder XYZ"
- "Rename this file to..." or "Change the folder name to..."

**IMPORTANT:** When the user provides only a document/file title without a file ID (e.g., "check document XYZ", "look at the v3 file", "compare with report ABC"), ALWAYS use this skill to search for the file first to get its file ID before performing any operations with other skills (like google-docs-manager).

## Available Tools

### Drive Manager Script

**Location:** `~/.claude/skills/google-drive-manager/scripts/`

**Structure:**
```
~/.claude/skills/google-drive-manager/scripts/
├── run.sh                  # Generic script runner
├── pyproject.toml          # Python dependencies
├── .venv/                  # Auto-created virtual environment
└── src/
    └── drive_manager.py    # Python Drive manager script
```

**Usage:**
```bash
# Search files
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search [--query QUERY] [--name NAME] [--mime-type TYPE] [--limit N]

# Upload file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload <file_path> [--parent FOLDER_ID] [--mime-type TYPE]

# Download file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download <file_id> <output_path> [--convert-to MIME_TYPE]

# Copy file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy <file_id> [--name NEW_NAME] [--parent FOLDER_ID]

# Move file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager move <file_id> <folder_id>

# Create folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager create-folder <name> [--parent FOLDER_ID]

# Delete file/folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager delete <file_id>

# Share file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share <file_id> <email> [--role ROLE] [--no-notify]

# Get file info (includes path hierarchy)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager info <file_id>

# List file permissions
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions <file_id>

# Remove a specific permission
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-permission <file_id> <permission_id>

# Share with anyone who has the link
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone <file_id> [--role ROLE]

# Remove public access
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-public <file_id>

# List folder contents
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager list-folder <folder_id> [--limit N]

# Rename file or folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager rename <file_id> <new_name>
```

**Examples:**
```bash
# Search for files
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'report' --limit 10

# Upload a document
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload document.pdf --parent 1abc123xyz

# Download a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1abc123xyz output.pdf

# Copy a file with new name
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy 1abc123xyz --name 'Copy of Report'

# Move file to folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager move 1abc123xyz 1folder456

# Create a folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager create-folder 'Q4 Reports'

# Delete a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager delete 1abc123xyz

# Share with write access
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role writer

# Get file details (includes path)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager info 1abc123xyz

# List permissions
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions 1abc123xyz

# Share with anyone (public link)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone 1abc123xyz --role reader

# Remove public access
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-public 1abc123xyz

# Remove specific permission
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-permission 1abc123xyz permission_id_123

# List folder contents
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager list-folder 1folder123 --limit 50

# Rename a file or folder
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager rename 1abc123xyz 'New Report Name'
```

**How It Works:**
The `run.sh` script uses `uv` to:
- Automatically create an isolated virtual environment (`.venv`)
- Install dependencies from `pyproject.toml`
- Execute the Python script with complete isolation
- No manual installation or setup required

**Operations:**

1. **Search**: Find files using Google Drive query syntax, name matching, or MIME type filtering (includes files shared with you)
2. **Upload**: Upload local files to Drive with optional parent folder specification
3. **Download**: Download files with smart export for Google Workspace documents (Docs, Sheets, Slides)
4. **Copy**: Create copies of files with optional renaming and parent folder
5. **Move**: Move files between folders
6. **Create Folder**: Create new folders with optional parent
7. **Delete**: Delete files or folders
8. **Share**: Share files with specific users and permission roles
9. **Info**: Get detailed file metadata including owners, permissions, timestamps, and full path hierarchy (shows "My Drive" or "Shared with me")
10. **Permissions**: List all permissions for a file (users, groups, domains, or public access)
11. **Remove Permission**: Remove a specific permission by permission ID
12. **Share Anyone**: Share file with anyone who has the link (public access)
13. **Remove Public**: Remove public access from a file
14. **List Folder**: List all files and folders inside a specific folder (ordered by folders first, then alphabetically)
15. **Rename**: Rename a file or folder without moving it

## Prerequisites

### System Requirements
- **uv** - Python package manager (https://docs.astral.sh/uv/)
- **GCP Project** with Drive API enabled
- **Google OAuth Credentials** stored in `~/.claude/credentials/`
- Python 3.8+ (managed by uv)

### Google Cloud Setup

1. **Enable Drive API:**
   ```bash
   gcloud services enable drive.googleapis.com
   ```

2. **Create OAuth Credentials:**
   - Go to Google Cloud Console (https://console.cloud.google.com/)
   - Navigate to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID (Desktop application type)
   - Download credentials as JSON file
   - Save to `~/.claude/credentials/google_credentials.json`

3. **First-time Authentication:**
   ```bash
   # Create credentials directory
   mkdir -p ~/.claude/credentials

   # Copy downloaded credentials
   cp ~/Downloads/client_secret_*.json ~/.claude/credentials/google_credentials.json

   # Run any command - will open browser for OAuth consent
   ~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'test'

   # Token saved to ~/.claude/credentials/google_token.json for future use
   ```

4. **Subsequent Runs:**
   - Token automatically refreshed when expired
   - No browser interaction needed
   - Seamless authentication

### Installation
**No manual installation required!** The `run.sh` script automatically:
1. Creates an isolated virtual environment (`.venv`)
2. Installs all dependencies from `pyproject.toml`
3. Runs the script with proper isolation

The first run may take a few seconds to set up the environment. Subsequent runs are instant.

## Common Workflows

### 1. Search for Files

```bash
# Search by name
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'Q4 Report'

# Search by MIME type
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --mime-type 'application/pdf' --limit 20

# Advanced query
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --query "name contains 'report' and modifiedTime > '2024-01-01'"
```

**Output:**
```
✅ Authenticated successfully
🔍 Searching for files...

✅ Found 3 file(s):

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

# Download Google Sheet as Excel
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1googlesheet123 spreadsheet.xlsx --convert-to 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
```

### 4. Copy Files

```bash
# Simple copy
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager copy 1abc123xyz

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

### 6. Share Files

```bash
# Share as reader (default)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com

# Share as writer
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role writer

# Share as commenter without notification
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1abc123xyz user@example.com --role commenter --no-notify
```

### 7. Manage File Permissions

```bash
# List all permissions for a file
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions 1abc123xyz
```

**Output:**
```
✅ Authenticated successfully
🔐 Getting file permissions...

✅ Permissions for file:

🌐 Anyone with the link
   Role: reader
   Permission ID: anyoneWithLink

👤 User: John Doe (john@example.com)
   Role: writer
   Permission ID: 12345678901234567890

👤 User: Jane Smith (jane@example.com)
   Role: reader
   Permission ID: 09876543210987654321

👤 User: Owner (owner@example.com)
   Role: owner
   Permission ID: 11111111111111111111
```

**Share with anyone (make public):**
```bash
# Reader access (default)
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone 1abc123xyz

# Writer access
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone 1abc123xyz --role writer
```

**Remove public access:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-public 1abc123xyz
```

**Remove specific permission:**
```bash
# First, list permissions to get the permission ID
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions 1abc123xyz

# Then remove the specific permission using its ID
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-permission 1abc123xyz 09876543210987654321
```

## Best Practices

### File Search
- **Use specific queries:** More specific queries return more relevant results
- **Limit results:** Use --limit to control the number of results
- **MIME types:** Filter by MIME type for specific file types (PDF, images, etc.)
- **Shared files:** Search now includes files "Shared with me" thanks to `includeItemsFromAllDrives=True`
- **Search shared files only:** Use query `sharedWithMe=true` to only show shared files
- **Search by owner:** Use query `'owner.email' in owners` to find files by specific owner

### File Upload/Download
- **Parent folders:** Organize files by specifying parent folders during upload
- **Smart export:** Download Google Workspace files automatically exports to common formats (PDF, XLSX, PPTX)
- **Batch operations:** Use shell loops for batch uploads/downloads

### File Management
- **Get file ID:** Use search to find file IDs before performing operations
- **Verify before delete:** Always verify file information before deleting
- **Share carefully:** Review permission roles before sharing
- **Find file location:** Use the `info` command to see file details including the full path hierarchy
- **Navigate hierarchy:** The `info` command shows paths for both "My Drive" and "Shared with me" files

### Permission Management
- **List first:** Always use `permissions` command to see current access before making changes
- **Permission IDs:** Copy the permission ID when removing specific access
- **Public access:** Be careful when using `share-anyone` - it makes the file accessible to anyone with the link
- **Remove public:** Use `remove-public` to quickly revoke public access
- **Owner files only:** You can only manage permissions on files you own (not files shared with you)

### Performance
- **Search limits:** Keep search limits reasonable for faster results
- **Large files:** Upload/download of large files may take time
- **API quotas:** Be mindful of Google Drive API quotas for high-volume operations

## How to Respond to Drive Requests

When users request Drive operations:

1. **Identify the operation:**
   - Search, upload, download, copy, move, share, delete, info, permissions, remove-permission, share-anyone, or remove-public

2. **Gather required parameters:**
   - File IDs (from search or provided by user)
   - File paths (for upload/download)
   - Folder IDs (for move/parent operations)
   - Email addresses (for sharing)

3. **Run the appropriate command:**
   - Execute the script with proper arguments
   - Monitor output for progress and errors
   - Report results to user

4. **Handle file IDs:**
   - If user doesn't provide file ID, search first
   - Extract ID from Drive URLs if provided
   - Confirm file details before destructive operations

5. **Handle errors:**
   - Check authentication if OAuth errors occur
   - Verify file IDs if not found
   - Confirm API access if permission errors occur

## Example Interactions

### Example 1: Search and Download

**User:** "Find the Q4 report PDF and download it"

**Response:**
```
I'll search for the Q4 report PDF in your Google Drive.

Searching...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'Q4 report' --mime-type 'application/pdf'
```

**Report results:**
```
Found 1 matching file:
- Q4 Report Final.pdf (ID: 1abc123xyz, Size: 245.67 KB)

Downloading to q4_report.pdf...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager download 1abc123xyz q4_report.pdf
```

**Final response:**
```
✅ Successfully downloaded Q4 Report Final.pdf to q4_report.pdf
```

### Example 2: Upload and Share

**User:** "Upload presentation.pptx and share it with team@example.com as editor"

**Response:**
```
I'll upload presentation.pptx to Google Drive and share it with team@example.com.

Uploading...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload presentation.pptx
```

**Extract file ID from output, then share:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share 1newfile123 team@example.com --role writer
```

**Final response:**
```
✅ Successfully uploaded presentation.pptx
✅ Shared with team@example.com as editor

File link: https://drive.google.com/file/d/1newfile123/view
```

### Example 3: Find File Location

**User:** "Where is 'La révolution française' located in my Drive?"

**Response:**
```
I'll search for the file and show you its location.

Searching...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --query "'morand.amira' in owners and name contains 'révolution'"
```

**Report results:**
```
Found 1 matching file:
- La révolution française et l'empire de 1729-1815 (ID: 10JCVDuzryv3n2jnFpQHaGUrATGVe8MTX0QKfbHId7Z8)
  Shared by: morand.amira

Getting file information...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager info 10JCVDuzryv3n2jnFpQHaGUrATGVe8MTX0QKfbHId7Z8
```

**Final response:**
```
✅ File Information:
   Name: La révolution française et l'empire de 1729-1815
   Type: Google Docs
   Owners: morand.amira
   Path: Shared with me / La révolution française et l'empire de 1729-1815

This file is shared with you by morand.amira and is located at the root of "Shared with me".
```

### Example 4: Manage File Permissions

**User:** "Make my presentation public so anyone can view it, then show me who has access"

**Response:**
```
I'll make your presentation accessible to anyone with the link and show you the permissions.

Searching for your presentation...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager search --name 'presentation' --query "'me' in owners" --limit 5
```

**Report results:**
```
Found: presentation.pptx (ID: 1abc123xyz)

Making it public...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone 1abc123xyz --role reader
```

**Then list permissions:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager permissions 1abc123xyz
```

**Final response:**
```
✅ File is now public! Here are all the permissions:

🌐 Anyone with the link - Reader
👤 You (owner@example.com) - Owner

Anyone with the link can now view your presentation.
Link: https://drive.google.com/file/d/1abc123xyz/view
```

**User follow-up:** "Actually, remove the public access"

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager remove-public 1abc123xyz
```

**Response:**
```
✅ Public access removed! The file is now private again.
```

## Troubleshooting

### "Google OAuth credentials not found"
```bash
# Create credentials directory
mkdir -p ~/.claude/credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.claude/credentials/google_credentials.json
```

The script will provide detailed instructions if credentials are missing.

### "Permission denied" errors
```bash
# Ensure Drive API is enabled
gcloud services enable drive.googleapis.com

# Verify OAuth scopes in credentials
# Should include:
# - https://www.googleapis.com/auth/drive
# - https://www.googleapis.com/auth/drive.file
```

### "File not found"
- Verify file ID is correct
- Ensure you have access to the file
- Check that file is not deleted or in trash

### "Insufficient permissions" when listing/managing permissions
- You can only view and manage permissions on files you own
- Files shared with you cannot have their permissions modified by you
- Contact the file owner if you need to change permissions on a shared file

### "Quota exceeded"
- Check Google Cloud Console for quota limits
- Consider requesting quota increase for high-volume operations
- Implement rate limiting for batch operations

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.claude/credentials/google_token.json
# Run any command to re-authenticate
```

### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with homebrew
brew install uv
```

## Technical Details

### MIME Types

Common MIME types for filtering:
- PDF: `application/pdf`
- Images: `image/jpeg`, `image/png`
- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Google Slides: `application/vnd.google-apps.presentation`
- Folders: `application/vnd.google-apps.folder`

### Query Syntax

Google Drive supports rich query syntax:
```
name contains 'report'
mimeType = 'application/pdf'
modifiedTime > '2024-01-01'
'me' in owners
trashed = false
```

### Smart Export

When downloading Google Workspace files, the script automatically exports to common formats:
- Google Docs → PDF
- Google Sheets → XLSX
- Google Slides → PPTX

You can override with `--convert-to` parameter.

### Permission Roles

Available roles for sharing:
- `reader` - Can view and download
- `writer` - Can edit
- `commenter` - Can comment but not edit
- `owner` - Full control (transfer ownership)

## Security & Privacy

- **OAuth authentication:** Uses secure OAuth 2.0 flow
- **Local credentials:** Stores credentials in `~/.claude/credentials/`
- **API access:** Only requests minimum required scopes
- **No logging:** Script does not log or store file content
- **Secure transfer:** All transfers use HTTPS

## Dependencies

Automatically installed by uv:
- `google-api-python-client` - Google Drive API client
- `google-auth-httplib2` - Authentication transport
- `google-auth-oauthlib` - OAuth 2.0 flow

## Response Approach

To accomplish Drive management tasks:

1. Identify the specific operation requested
2. Gather required parameters (file IDs, paths, etc.)
3. Search for files if IDs not provided
4. Execute the appropriate command
5. Monitor output for progress and errors
6. Report results with relevant file information
7. Handle errors with appropriate troubleshooting steps
