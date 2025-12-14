# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CV Manager is a skill for managing candidate CVs and interview records in a structured Google Drive/Docs system. It handles three main workflows:
1. Adding CVs (upload, extract info, create tracking entry)
2. Adding interviews (transcribe, structure notes, append to candidate)
3. Summarizing candidates (retrieve and format all candidate data)

## Architecture

### Workflow Pattern
All workflows follow a validation-before-insertion pattern:
1. Process input (extract text, transcribe audio, etc.)
2. Generate structured content
3. **Present to user for approval** (critical step - never skip)
4. Insert into Google Docs tracking document
5. Clean up local files

### Data Storage
- **CVs:** Google Drive folder `1n5sMW4L_NHpnIFVogRD2I3jPvKk2WQUw`
- **Interview files:** Google Drive folder `1fRRtK3TPxbTDSPw_KufOrYLHMNuelLp0`
- **Tracking document:** Google Doc `1M83HrxnWIOYUGk_jtaaLS_eo5_-sIlHmi_1ZAwCdRWI`

### Document Structure Hierarchy
The tracking document uses strict Google Docs heading levels:
- **H1:** Document title "CVs" (only one)
- **H2:** "Table of content" + each candidate name
- **H3:** "Presentation" + "Interview" (per candidate)
- **H4:** Interview date (one per interview)
- **H5:** "Attendees" + "Summary" (per interview)

New candidates are always inserted after "Table of content".

## Commands

### Run Python Scripts
```bash
scripts/run.sh <script_name> [args...]
```
- Automatically loads `.env` files from multiple locations (skill, skills/, .claude/)
- Uses `uv` for isolated Python environments
- Scripts are in `scripts/src/`

### Extract CV Text
```bash
scripts/run.sh extract_cv <file_path>
```
- Supports PDF files only (use `pdf-extractor` skill for complex PDFs)
- Outputs extracted text to stdout

## Key Implementation Details

### Workflow 1: Add CV
1. Extract text using `extract_cv.py` or `pdf-extractor` skill
2. Analyze and draft job title + 100-200 word description
3. **Get user approval** on content
4. Upload CV to Drive using `google-drive-manager` skill (Folder ID: `1n5sMW4L_NHpnIFVogRD2I3jPvKk2WQUw`)
5. Use `google-docs-manager` skill to insert into tracking document after "Table of content"
6. Remove local file with `rm`

### Workflow 2: Add Interview
1. If audio provided, use `speech-to-text` skill to transcribe
2. Upload audio/attachments to Interview Files folder via `google-drive-manager`
3. Extract date, attendees, and draft summary (2 paragraphs: overall assessment + detailed discussion)
4. **Present attendees list for user confirmation**
5. **Get user approval** on complete entry
6. Use `google-docs-manager` skill to append to candidate's Interview section
7. Remove local files with `rm`

**Critical:** Attendees are plain text (not bullets). Summary has two distinct paragraphs.

### Workflow 3: Summarize Candidate
1. Use `google-docs-manager` skill to read tracking document
2. Find candidate's H2 section
3. Extract all Presentation + Interview data
4. Generate comprehensive summary with interview history
5. Present to user with CV link

## Integration Points

- **google-docs-manager:** Primary tool for reading/writing tracking document
- **google-drive-manager:** Upload interview files and alternative Drive operations
- **pdf-extractor:** Complex PDF extraction when `extract_cv.py` fails
- **speech-to-text:** Transcribe interview audio recordings
- **email-extractor:** Extract CVs from email attachments

## Validation Rules

- Always get formal user approval before inserting into tracking document
- Never skip the validation step - user reviews all content first
- Respect document structure hierarchy strictly (H2-H5)
- One candidate = one H2 section with one Presentation + one Interview section
- Multiple interviews per candidate allowed (multiple H4 under Interview H3)
- Attendees: plain text only, no bullets
- Summary: exactly 2 paragraphs (assessment first, then discussion)

## Authentication

Uses Google OAuth credentials from `~/.claude/credentials/google/token.json` with scopes:
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/drive.file`
- `https://www.googleapis.com/auth/documents`

## Dependencies

See `scripts/pyproject.toml`:
- Google API libraries (auth, drive, docs)
- PyPDF2 for PDF extraction
- python-dotenv for environment management
- openai (for potential future enhancements)

## SKILL.md Management

**CRITICAL:** The `SKILL.md` file is the primary interface for Claude Code to understand when and how to invoke this skill. It contains AI-optimized trigger patterns and workflow instructions.

### When to Update SKILL.md

Update `SKILL.md` when:
- User requests modifications to skill behavior or workflows
- New capabilities are added to the skill
- Trigger patterns need to be refined
- Workflow steps change or are optimized
- Integration with other skills changes

### Update Process

**MANDATORY STEPS:**
1. **ALWAYS ask user for approval BEFORE modifying SKILL.md**
2. Present proposed changes clearly
3. Wait for user confirmation
4. Only after approval, update SKILL.md with AI-optimized content
5. Ensure trigger patterns in description are clear and comprehensive
6. Test that the updated content will help Claude Code properly invoke the skill

**Never update SKILL.md without explicit user approval.**
