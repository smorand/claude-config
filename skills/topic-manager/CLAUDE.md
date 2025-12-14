# Topic Manager - AI Instructions

## Critical Rules for Topic Management

### Topic Folder Structure (MUST UNDERSTAND FIRST)

**Every topic has this exact structure in Google Drive**:
```
Topics/
└── {Topic Name}/
    ├── {Topic Name}         # Google Doc (the main topic document)
    ├── Minutes/             # Meeting recordings, transcripts, notes
    ├── Prez/                # Presentations, slides, schemas, diagrams
    ├── Documents/           # Supporting documents AND emails (.pdf, .eml)
    └── One pager/           # Executive summaries, briefings
```

**Upload Protocol - CRITICAL**:
1. **ALWAYS** locate the topic's root folder first using `google-drive-manager`
2. **ALWAYS** upload to the appropriate subfolder **WITHIN that topic folder**
3. **NEVER** upload to root Topics folder or wrong topic's folder
4. **CREATE subfolder if it doesn't exist** (Minutes, Prez, Documents, One pager)

**File Type to Subfolder Mapping**:
- Audio/Video of meetings → `{Topic Name}/Minutes/`
- Meeting notes/transcripts → `{Topic Name}/Minutes/`
- PowerPoint/PDF presentations → `{Topic Name}/Prez/`
- Mermaid diagrams (.mmd, .svg) → `{Topic Name}/Prez/`
- Schemas, architecture images → `{Topic Name}/Prez/`
- **Emails (.eml files)** → `{Topic Name}/Documents/`
- PDF documents, contracts, specifications → `{Topic Name}/Documents/`
- Executive summaries → `{Topic Name}/One pager/`

### Structure Preservation is PARAMOUNT

When updating Google Docs, **NEVER** break the document structure. This is the #1 rule.

**Correct Insertion Points**:
1. **Minutes**: Insert at the TOP of the Minutes section (immediately after "# Minutes" heading)
   - Newest minutes always appear first
   - Use `## Date - Meeting Title` format
   - Then `### a) Attendees`, `### b) Summary`, `### c) Decisions/Actions`, `### d) Minutes`

2. **Actions**: Insert at the END of the Actions section (before the "# Risks" heading)
   - Each action is `## Action Title`
   - With `### Owner`, `### Description`, `### Risks`, `### Logs`

3. **Action Logs**: Add to the specific action's Logs subsection
   - Use `#### Date` for each log entry
   - Add content immediately after the date heading
   - Reference the meeting/source

4. **Risks**: Insert at the END of the Risks section (before the "# Minutes" heading)
   - Each risk is `## Risk Title`
   - With `### Description` and `### Mitigation actions`

5. **Presentation Updates**: Modify the existing Presentation section inline
   - Don't create a new Presentation section
   - Add to existing content

### Never Use Approximate Heading Levels

❌ **WRONG**: Using bold text instead of headings
❌ **WRONG**: Skipping heading levels (H1 to H3 without H2)
❌ **WRONG**: Using wrong heading level (H3 for action title instead of H2)

✅ **CORRECT**: Exact heading levels as specified in Template v2
✅ **CORRECT**: Maintaining the strict hierarchy

### Read Before Write

**ALWAYS**:
1. Read the entire Google Doc first using `google-docs-manager`
2. Understand the current structure
3. Identify exact insertion points
4. Plan the update to preserve structure
5. Then execute the update

### Confirmation Protocol

**Ask for confirmation when**:
- Adding >3 new items (actions, risks, minutes)
- Making structural changes
- Identifying cross-topic impacts (especially for one-to-ones)
- Uncertain about interpretation of content

**Don't ask when**:
- Simple action log update
- Single minute addition
- User explicitly said to proceed

### Content Extraction Priority

1. **Transcription First**: For audio/video, always transcribe fully before summarizing
   - **Meeting date**: Extract from recording date in the filename
2. **OCR When Needed**: Don't skip images - extract text via OCR
3. **Email Threading**: Understand full email thread context, not just latest message
   - **Meeting date**: Extract from email's Date header
   - **CRITICAL**: Each email = ONE minute entry (treat like a meeting)
   - Then extract info from email to update Actions/Risks/Presentation
4. **Attachment Processing**: Extract and process ALL attachments
5. **Application Codes**: Always identify SNSVCxxxxxxx codes and link to systems

### Email Processing Rules (CRITICAL)

**When processing emails (.eml files)**:

1. **ONE Email = ONE Minute Entry**
   - Each .eml file creates exactly one minute entry in the Minutes section
   - Treat the email like a meeting record

2. **Date Source**:
   - Use email's Date header as the meeting date (not received date, not sent date from filename)

3. **Two-Phase Processing**:
   - **Phase 1**: Create the minute entry with:
     - Date from email header
     - Subject as meeting title
     - To/Cc as attendees
     - Email content in d) Minutes (link to uploaded .eml file)
   - **Phase 2**: Extract information from email to:
     - Create new actions (in Actions section)
     - Update existing actions (add logs)
     - Create new risks (in Risks section)
     - Update Presentation/Description if relevant

4. **Upload Location**:
   - .eml file → `{Topic Name}/Documents/` folder
   - Email attachments → appropriate subfolders (Prez, Documents, Minutes)

5. **Linking**:
   - Link the uploaded .eml file in the minute entry's d) Minutes subsection

### Workflow Orchestration

**Correct Sequence for Updates**:
1. Locate topic's root folder (`google-drive-manager`)
2. Locate/create appropriate subfolders (Minutes, Prez, Documents, One pager)
3. Upload source files to correct subfolders **WITHIN topic folder** (`google-drive-manager`):
   - See "File Type to Subfolder Mapping" above
   - **Emails MUST go to Documents/ subfolder**
4. Extract content using appropriate skills:
   - Video → `video-creator` (extract audio) → `speech-to-text` [date from filename]
   - Audio → `speech-to-text` [date from filename]
   - PDF/PPT → `pdf-extractor`
   - Email → `email-extractor` [date from email Date header]
   - Images → `pdf-extractor` with OCR
5. Read current Google Doc (`google-docs-manager`)
6. Analyze all extracted content (apply Email Processing Rules if applicable)
7. Propose changes to user
8. Update Google Doc (`google-docs-manager`)
9. Confirm completion with links to uploaded files

### Application Code Tracking

**Format**: `SNSVCxxxxxxx` where xxxxxxx is a 7-digit number

**Always**:
- Search for this pattern in all content
- Add to Presentation section if found
- Link topics to IT systems via these codes
- Can be 0, 1, or multiple per topic

### Schema and Diagram Handling

**When topics include schemas, diagrams, or architecture images**:

1. **Upload Both Source and Rendered Files**:
   - If `.mmd` (Mermaid) source exists: Upload both `.mmd` and `.svg` files to `Prez/` folder
   - If only `.svg` exists: Upload `.svg` to `Prez/` folder
   - Other formats (PNG, JPG, etc.): Upload to `Prez/` folder

2. **Make Images Public for Google Docs**:
   - After uploading to Drive, make the image file publicly accessible
   - Set permissions: `type: anyone, role: reader`
   - Get the public Drive URL: `https://drive.google.com/uc?export=view&id=FILE_ID`

3. **Embed in Google Doc**:
   - Use `google-docs-manager` skill's `insert-image` command
   - Insert image directly into the Presentation section of the Google Doc
   - Add appropriate legend describing the schema/diagram
   - Format: `Figure X: [Description]` in italic below the image

4. **Workflow Example**:
   ```bash
   # 1. Upload schema files to Prez folder
   ~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager upload schemas/architecture.svg --parent PREZ_FOLDER_ID

   # 2. Make image public (share with anyone)
   ~/.claude/skills/google-drive-manager/scripts/run.sh drive_manager share-anyone FILE_ID --role reader

   # 3. Insert into Google Doc with legend
   ~/.claude/skills/google-docs-manager/scripts/run.sh docs_manager insert-image DOC_ID \
       "https://drive.google.com/uc?export=view&id=FILE_ID" \
       --legend "Figure 1: System Architecture"
   ```

5. **Location in Document**:
   - Insert schema images in the Presentation section
   - Place after the description text
   - Before the Application References subsection

6. **Important Notes**:
   - **NEVER** reference local file paths in Google Docs
   - **ALWAYS** use publicly accessible Drive URLs
   - Keep `.mmd` source files in Prez folder for future editing
   - Update both source and rendered files if schema changes

### One-to-One Special Handling

When updating a one-to-one topic:
1. **Identify cross-topic mentions**: Look for references to other topics/projects
2. **Ask user**: "This mentions [Topic X] - should I also update that topic?"
3. **Update both if confirmed**: Add cross-references in both directions
4. **No Presentation section**: One-to-ones only have "Next topics" and "Minutes"

### Opening Topics in Browser

**When user asks to "open <label> topic"**:
1. Locate the topic's Google Doc using `google-drive-manager`
2. Get the Google Doc URL
3. Clearly instruct the user to run: `open <url_google_doc_file>`
   - This terminal command opens the Google Doc in the default browser
   - Example: `open https://docs.google.com/document/d/1ABC...xyz/edit`

**Important**: Always provide the exact `open` command with the full URL, ready to copy and paste.

### Topic Creation Protocol

**When creating a new topic**:
1. Create topic folder in Notes (Google Drive ID: `16VBlrwK2FAmIfzqN1g9h-sCkQ4YuHz8x`)
2. **Immediately create all four subfolders** within the topic folder:
   - `Minutes/`
   - `Prez/`
   - `Documents/`
   - `One pager/`
3. Create Google Doc from Template v2 using `google-docs-manager`
4. Name the Google Doc with the same name as the topic folder

**Never skip subfolder creation** - all four must exist from the start.

### Error Recovery

**If topic not found**:
- Ask: "Topic '[name]' not found. Would you like me to create it?"

**If document structure is corrupted**:
- Alert user: "The document structure appears malformed. I can attempt to fix it or you can restructure manually. What would you prefer?"

**If upload fails**:
- Retry once
- If still fails: "Upload failed for [file]. Please check permissions/connectivity."

**If extraction fails**:
- Note in summary: "Could not extract content from [file] - please verify file integrity"
- Ask if user can provide information manually

### Common Mistakes to Avoid

❌ Creating duplicate sections (e.g., two "Presentation" sections)
❌ Mixing heading levels (e.g., H4 before H3)
❌ Forgetting to link uploaded files in the document
❌ Summarizing without full transcription
❌ Ignoring email attachments
❌ Not identifying action items from content
❌ Forgetting to reference meeting in action logs
❌ Breaking chronological order (minutes newest first)
❌ **Forgetting to cleanup local files after successful upload**

### Quality Checklist

Before confirming completion, verify:
- [ ] All source files uploaded to correct **subfolders within topic folder**
- [ ] Emails uploaded to `{Topic Name}/Documents/` (NOT root, NOT other folders)
- [ ] All content fully extracted (transcribed/OCR'd/parsed)
- [ ] Document structure preserved perfectly
- [ ] All new sections use correct heading levels
- [ ] Minutes inserted at top of Minutes section
- [ ] Actions inserted at end of Actions section
- [ ] Action logs include date and meeting reference
- [ ] All uploaded files linked in document
- [ ] Application codes identified and added
- [ ] Cross-topic impacts identified (for one-to-ones)
- [ ] User confirmation obtained (if needed)
- [ ] **Local source files cleaned up (removed from disk)**
- [ ] Completion summary includes all links to uploaded files and confirms cleanup

### Template v2 Reference

When creating new topics, use the Template v2 from `google-docs-manager` skill which includes:
- All required heading sections
- Proper hierarchy
- Placeholder text
- Correct formatting

The template ensures consistency across all topics.
