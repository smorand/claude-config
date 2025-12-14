# Topic Manager Skill

## Overview

The Topic Manager skill enables Claude to manage professional topics stored as structured Google Drive folders and Google Docs. It provides comprehensive management of meeting minutes, actions, risks, and related documentation.

## What This Skill Does

### Core Capabilities

1. **Create Topics**: Sets up new topic folders with proper structure (Prez, Emails, Records subfolders) and creates structured Google Docs using Template v2

2. **Update Topics**: Processes various inputs (meeting recordings, presentations, emails, documents) to:
   - Transcribe audio/video recordings
   - Extract content from presentations and PDFs
   - Parse email threads and attachments
   - Add structured meeting minutes
   - Track actions with owners and logs
   - Document risks with mitigation strategies

3. **Summarize Topics**: Provides comprehensive overviews including:
   - Topic description and related applications (SNSVC codes)
   - Active actions and their status
   - Outstanding risks
   - Recent meeting summaries

4. **Manage Actions**: Updates action items with timestamped logs and meeting references

5. **One-to-One Management**: Special handling for one-on-one meeting topics with cross-topic impact identification

## Topic Structure

Each topic is a Google Drive folder containing:
```
Topic_Name/
├── Topic_Name          # Structured Google Doc
├── Prez/              # Presentations (PowerPoint, PDF, images)
├── Emails/            # Email backups (.eml files)
└── Records/           # Audio/video meeting recordings
```

## Document Structure (Template v2)

The Google Doc follows a strict hierarchical structure:
- **Title**: Topic name
- **Heading 1**: Table of Content
- **Heading 1**: Presentation (description, application links)
- **Heading 1**: Actions (each with owner, description, risks, logs)
- **Heading 1**: Risks (each with description and mitigation)
- **Heading 1**: Minutes (chronological, most recent first)

## Supported Input Formats

- **Audio**: mp3, ogg, wav, etc.
- **Video**: mp4, mov, avi, etc. (audio extracted)
- **Presentations**: PowerPoint, PDF
- **Documents**: PDF, images (OCR)
- **Emails**: .eml files with attachments
- **Text**: Direct user input for minutes

## Integration Points

This skill orchestrates multiple other skills:
- `google-drive-manager` - File and folder operations
- `google-docs-manager` - Document creation and updates
- `speech-to-text` - Audio/video transcription
- `video-creator` - Audio extraction from video
- `pdf-extractor` - Content extraction from PDFs and images
- `email-extractor` - Email parsing and attachment handling

## Usage Examples

### Create a New Topic
```
User: Create a new topic called "Cloud Migration Strategy"
```

### Update with Meeting Recording
```
User: Update the Cloud Migration topic with this meeting recording
```

### Add Email Information
```
User: Update the API Modernization topic using the planning meeting email
```

### Summarize a Topic
```
User: Summarize the Data Platform Roadmap topic
```

### Update an Action
```
User: Update the "Security Review" action in the Cloud Migration topic - phase 1 completed
```

## Key Features

- **Structure Preservation**: Maintains strict document hierarchy when updating
- **Comprehensive Extraction**: Transcribes audio, extracts text from PDFs, parses email threads
- **Smart Analysis**: Identifies actions, risks, decisions, and attendees from content
- **Cross-Topic Awareness**: Identifies when one-to-one meetings impact other topics
- **Application Tracking**: Links topics to IT systems via SNSVC codes
- **Chronological Management**: Minutes newest first, action logs timestamped

## Storage Location

All topics are stored in the Google Drive `Notes` folder (ID: `16VBlrwK2FAmIfzqN1g9h-sCkQ4YuHz8x`)

## Best Practices

1. Always confirm before making substantial updates (>3 changes)
2. Upload all source materials to appropriate folders
3. Extract maximum value from each content type
4. Preserve document structure with exact heading levels
5. Link all uploaded documents in the Google Doc
6. Identify and track application references (SNSVCxxxxxxx)
7. Cross-reference related topics when updating one-to-ones

## Special Cases

### One-to-One Topics
Simplified structure with only:
- Next topics (bullet points for discussion)
- Minutes (with potential cross-topic impacts)

The skill identifies when one-to-one minutes affect other topics and prompts for confirmation.
