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

### Drive Manager Binary (gdrive)

**Location:** `~/.claude/skills/google-drive-manager/scripts/gdrive`

**Binary:** Go-based command-line tool for Google Drive operations. No Python installation required.

**Source Code:** `~/projects/new/gdrive/` (see CLAUDE.md for build instructions)

**Usage:**
```bash
# Search files
~/.claude/skills/google-drive-manager/scripts/gdrive search QUERY [--type TYPE] [--max N]

# File operations
~/.claude/skills/google-drive-manager/scripts/gdrive file copy SOURCE_PATH [NEW_NAME] [--parent DEST_PATH]
~/.claude/skills/google-drive-manager/scripts/gdrive file delete FILE_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive file download FILE_PATH [--output LOCAL_PATH]
~/.claude/skills/google-drive-manager/scripts/gdrive file info FILE_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive file move SOURCE_PATH DEST_FOLDER_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive file rename FILE_PATH NEW_NAME
~/.claude/skills/google-drive-manager/scripts/gdrive file upload LOCAL_PATH [--parent DEST_FOLDER_PATH]
~/.claude/skills/google-drive-manager/scripts/gdrive file share FILE_PATH EMAIL [--role ROLE]
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public FILE_PATH [--role ROLE]
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions FILE_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-permission FILE_PATH PERMISSION_ID
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public FILE_PATH

# Folder operations
~/.claude/skills/google-drive-manager/scripts/gdrive folder create FOLDER_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive folder list FOLDER_PATH
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload LOCAL_DIR [--parent DEST_PATH]
~/.claude/skills/google-drive-manager/scripts/gdrive folder download FOLDER_PATH [--output LOCAL_DIR]
```

**Path Format:**
- Paths use forward slashes: `My Drive/Documents/Reports`
- File IDs also work: `1abc123xyz`
- All paths are resolved automatically

**Examples:**
```bash
# Search for files
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 Report"
~/.claude/skills/google-drive-manager/scripts/gdrive search "budget 2024" --max 20
~/.claude/skills/google-drive-manager/scripts/gdrive search Passeport --type image,pdf
~/.claude/skills/google-drive-manager/scripts/gdrive search "My Project" --type folder

# Upload and download
~/.claude/skills/google-drive-manager/scripts/gdrive file upload document.pdf --parent "My Drive/Documents"
~/.claude/skills/google-drive-manager/scripts/gdrive file download "My Drive/Reports/Q4.pdf" --output ~/Downloads/

# Copy and move
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "My Drive/Report.pdf" "Report Copy.pdf"
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" --parent "My Drive/Archive"
~/.claude/skills/google-drive-manager/scripts/gdrive file move "Report.pdf" "My Drive/Documents"

# Folder operations
~/.claude/skills/google-drive-manager/scripts/gdrive folder create "My Drive/Projects/2024/Q4"
~/.claude/skills/google-drive-manager/scripts/gdrive folder list "My Drive/Documents"
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/projects/myapp --parent "My Drive/Backups"

# Permissions
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role writer
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Presentation.pptx" --role reader
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "Report.pdf"
```

**How It Works:**
- Pure Go binary with no dependencies
- Uses OAuth2 for authentication
- Credentials stored at `~/.credentials/google_credentials.json`
- Token cached at `~/.credentials/google_token.json`
- Fast and lightweight

**Operations:**

1. **Search**: Find files by name or type with filters (supports shortcuts: image, audio, video, prez, doc, spreadsheet, txt, pdf, folder)
2. **File Upload**: Upload local files to Drive with optional parent folder
3. **File Download**: Download files from Drive (auto-converts Google Workspace files)
4. **File Copy**: Create copies with optional renaming and destination folder
5. **File Move**: Move files between folders
6. **File Rename**: Rename files without moving them
7. **File Delete**: Delete files or folders
8. **File Info**: Get detailed metadata including path, size, type, owners
9. **File Share**: Share with specific users (reader/writer/commenter roles)
10. **Share Public**: Make files accessible to anyone with the link
11. **Permissions**: List all permissions on a file
12. **Remove Permission**: Remove specific permission by ID
13. **Remove Public**: Remove public access
14. **Folder Create**: Create folder paths (like mkdir -p)
15. **Folder List**: List folder contents
16. **Folder Upload**: Upload entire directories recursively
17. **Folder Download**: Download entire folders recursively

## Prerequisites

### System Requirements
- **GCP Project** with Drive API enabled
- **Google OAuth Credentials** stored in `~/.credentials/`
- **gdrive binary** (pre-compiled, included in scripts folder)

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
   - Save to `~/.credentials/google_credentials.json`

3. **First-time Authentication:**
   ```bash
   # Create credentials directory
   mkdir -p ~/.credentials

   # Copy downloaded credentials
   cp ~/Downloads/client_secret_*.json ~/.credentials/google_credentials.json

   # Run any command - will open browser for OAuth consent
   ~/.claude/skills/google-drive-manager/scripts/gdrive search test

   # Token saved to ~/.credentials/google_token.json for future use
   ```

4. **Subsequent Runs:**
   - Token automatically refreshed when expired
   - No browser interaction needed
   - Seamless authentication

### Installation
**No installation required!** The gdrive binary is:
- Pre-compiled and ready to use
- Standalone with no dependencies
- Fast and lightweight
- Cross-platform compatible

## Common Workflows

### 1. Search for Files

```bash
# Search by name
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 Report"

# Search with type filter
~/.claude/skills/google-drive-manager/scripts/gdrive search report --type pdf

# Search with max results
~/.claude/skills/google-drive-manager/scripts/gdrive search "budget 2024" --max 20

# Search for multiple types
~/.claude/skills/google-drive-manager/scripts/gdrive search contract --type doc,pdf
```

**Output:**
```
Searching for: Q4 Report

📄 Q4 Report Final
   ID: 1abc123xyz
   Type: application/pdf
   Modified: 2024-12-15

📄 Q4 Report Draft
   ID: 1def456uvw
   Type: application/vnd.google-apps.document
   Modified: 2024-12-14
```

### 2. Upload Files

```bash
# Upload to root
~/.claude/skills/google-drive-manager/scripts/gdrive file upload report.pdf

# Upload to specific folder
~/.claude/skills/google-drive-manager/scripts/gdrive file upload report.pdf --parent "My Drive/Documents"

# Upload entire folder
~/.claude/skills/google-drive-manager/scripts/gdrive folder upload ~/myproject --parent "My Drive/Backups"
```

### 3. Download Files

```bash
# Download by path
~/.claude/skills/google-drive-manager/scripts/gdrive file download "My Drive/Reports/Q4.pdf"

# Download by ID
~/.claude/skills/google-drive-manager/scripts/gdrive file download 1abc123xyz --output ~/Downloads/report.pdf

# Download entire folder
~/.claude/skills/google-drive-manager/scripts/gdrive folder download "My Drive/Projects/MyApp" --output ~/Downloads/
```

### 4. Copy Files

```bash
# Copy with new name
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" "Report Copy.pdf"

# Copy to different folder
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "Report.pdf" --parent "My Drive/Archive"

# Copy with both new name and location
~/.claude/skills/google-drive-manager/scripts/gdrive file copy "My Drive/Report.pdf" "Q4 Report Copy.pdf" --parent "My Drive/Archive"
```

### 5. Move and Rename Files

```bash
# Move file to folder
~/.claude/skills/google-drive-manager/scripts/gdrive file move "Report.pdf" "My Drive/Documents"

# Rename file
~/.claude/skills/google-drive-manager/scripts/gdrive file rename "Report.pdf" "Final Report.pdf"
```

### 6. Share Files

```bash
# Share as reader (default)
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com

# Share as writer
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role writer

# Share as commenter
~/.claude/skills/google-drive-manager/scripts/gdrive file share "Report.pdf" user@example.com --role commenter
```

### 7. Manage File Permissions

```bash
# List all permissions for a file
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"
```

**Output:**
```
Permissions for: Report.pdf

🌐 Anyone with the link - reader
   ID: anyoneWithLink

👤 john@example.com - writer
   ID: 12345678901234567890

👤 owner@example.com - owner
   ID: 11111111111111111111
```

**Share with anyone (make public):**
```bash
# Reader access (default)
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Report.pdf"

# Writer access
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "Report.pdf" --role writer
```

**Remove public access:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "Report.pdf"
```

**Remove specific permission:**
```bash
# First, list permissions to get the permission ID
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "Report.pdf"

# Then remove the specific permission using its ID
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-permission "Report.pdf" 12345678901234567890
```

## Best Practices

### File Search
- **Use type filters:** Use shortcuts (image, pdf, doc, folder) for faster filtering
- **Limit results:** Use --max to control the number of results (default 50)
- **Specific queries:** More specific search terms return better results
- **Multiple types:** Combine types with commas: `--type pdf,doc`

### File Upload/Download
- **Use paths:** Paths are easier to read than file IDs
- **Parent folders:** Organize uploads with --parent flag
- **Folder operations:** Use folder upload/download for entire directories
- **Auto-convert:** Google Workspace files automatically convert on download

### File Management
- **Search first:** Find files with search before operating on them
- **Use info:** Get detailed file information including full path
- **Verify deletes:** Check file info before deleting
- **Paths vs IDs:** Both work, but paths are more readable

### Permission Management
- **List first:** Check current permissions before making changes
- **Permission IDs:** Note the ID when removing specific access
- **Public access:** Be careful with share-public - anyone with link can access
- **Role selection:** Choose appropriate role (reader/writer/commenter)

### Performance
- **Binary speed:** Go binary is fast and lightweight
- **No dependencies:** No Python or package installation needed
- **Token caching:** Authentication tokens are cached and auto-refreshed
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
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search "Q4 report" --type pdf
```

**Report results:**
```
Found: Q4 Report Final.pdf (ID: 1abc123xyz)

Downloading...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file download 1abc123xyz --output ~/Downloads/q4_report.pdf
```

**Final response:**
```
✅ Downloaded Q4 Report Final.pdf to ~/Downloads/q4_report.pdf
```

### Example 2: Upload and Share

**User:** "Upload presentation.pptx and share it with team@example.com as editor"

**Response:**
```
I'll upload presentation.pptx to Google Drive and share it with team@example.com.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file upload presentation.pptx
```

**Then share (using the file path or ID from upload):**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share "presentation.pptx" team@example.com --role writer
```

**Final response:**
```
✅ Uploaded presentation.pptx
✅ Shared with team@example.com as editor
```

### Example 3: Find File Location

**User:** "Where is 'La révolution française' located in my Drive?"

**Response:**
```
I'll search for the file and show you its location.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search "révolution" --type doc
```

**Report results:**
```
Found: La révolution française et l'empire de 1729-1815

Getting details...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file info 10JCVDuzryv3n2jnFpQHaGUrATGVe8MTX0QKfbHId7Z8
```

**Final response:**
```
File: La révolution française et l'empire de 1729-1815
Type: Google Docs
Path: Shared with me / La révolution française et l'empire de 1729-1815
Owner: morand.amira

This file is shared with you by morand.amira.
```

### Example 4: Manage File Permissions

**User:** "Make my presentation public so anyone can view it, then show me who has access"

**Response:**
```
I'll make your presentation accessible to anyone with the link.
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive search presentation --type prez --max 5
```

**Report results:**
```
Found: presentation.pptx

Making it public...
```

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file share-public "presentation.pptx" --role reader
```

**Then list permissions:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file permissions "presentation.pptx"
```

**Final response:**
```
✅ File is now public!

Permissions:
🌐 Anyone with the link - reader
👤 owner@example.com - owner

Anyone with the link can now view your presentation.
```

**User follow-up:** "Actually, remove the public access"

**Execute:**
```bash
~/.claude/skills/google-drive-manager/scripts/gdrive file remove-public "presentation.pptx"
```

**Response:**
```
✅ Public access removed! The file is now private.
```

## Troubleshooting

### "Google OAuth credentials not found"
```bash
# Create credentials directory
mkdir -p ~/.credentials

# Download OAuth credentials from Google Cloud Console
# Save to ~/.credentials/google_credentials.json
```

The binary will provide instructions if credentials are missing.

### "Permission denied" errors
```bash
# Ensure Drive API is enabled
gcloud services enable drive.googleapis.com

# Verify OAuth scopes in credentials
# OAuth client should be configured for Desktop application type
```

### "File not found"
- Verify file path or ID is correct
- Try searching for the file first
- Ensure you have access to the file
- Check that file is not deleted or in trash

### "Insufficient permissions" when managing permissions
- You can only manage permissions on files you own
- Files shared with you cannot have their permissions modified
- Contact the file owner if you need to change permissions

### "Quota exceeded"
- Check Google Cloud Console for quota limits
- Consider requesting quota increase for high-volume operations
- Implement delays between batch operations

### Re-authenticate
```bash
# Delete token to trigger new OAuth flow
rm ~/.credentials/google_token.json

# Run any command to re-authenticate
~/.claude/skills/google-drive-manager/scripts/gdrive search test
```

### Binary execution issues
```bash
# Ensure binary has execute permissions
chmod +x ~/.claude/skills/google-drive-manager/scripts/gdrive

# Check binary works
~/.claude/skills/google-drive-manager/scripts/gdrive --help
```

## Technical Details

### Type Shortcuts

The binary supports convenient type shortcuts:
- `image` - All image types (JPEG, PNG, GIF, etc.)
- `audio` - Audio files
- `video` - Video files
- `prez` - Presentations (Google Slides, PowerPoint)
- `doc` - Documents (Google Docs, Word)
- `spreadsheet` - Spreadsheets (Google Sheets, Excel)
- `txt` - Text files
- `pdf` - PDF files
- `folder` - Folders

You can also use explicit MIME types like `image/jpeg`, `application/pdf`.

### Path Resolution

The binary automatically resolves paths:
- `My Drive/Documents/Report.pdf` - Full path
- `Documents/Report.pdf` - Relative to My Drive
- `1abc123xyz` - Direct file ID
- Supports both forward slashes and spaces in names

### Smart Export

When downloading Google Workspace files, automatic conversion:
- Google Docs → PDF
- Google Sheets → XLSX
- Google Slides → PPTX

### Permission Roles

Available roles for sharing:
- `reader` - Can view and download
- `writer` - Can edit
- `commenter` - Can comment but not edit
- `owner` - Full control (transfer ownership)

## Security & Privacy

- **OAuth authentication:** Secure OAuth 2.0 flow
- **Local credentials:** Stored in `~/.credentials/`
- **Token caching:** Automatic refresh when expired
- **No data storage:** Binary doesn't log or store file content
- **HTTPS:** All API calls use secure HTTPS

## Dependencies

**None!** The gdrive binary is:
- Standalone executable
- No runtime dependencies
- No Python, Node.js, or other runtimes needed
- Built with Go for maximum portability

## Response Approach

To accomplish Drive management tasks:

1. Identify the specific operation requested
2. Gather required parameters (file IDs, paths, etc.)
3. Search for files if IDs not provided
4. Execute the appropriate command
5. Monitor output for progress and errors
6. Report results with relevant file information
7. Handle errors with appropriate troubleshooting steps
