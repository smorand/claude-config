---
description: Add an interview record for a candidate using cv-manager skill
---

# Add Interview Record

You must use the **cv-manager** skill to process this interview and add it to the candidate's tracking entry.

## Input Requirements

The user will provide:
- **Candidate name** (required)
- **Interview content** which can be:
  - Name of a recording file (audio/video from `~/.logs/` directory)
  - Manual written information in text format (personal conclusions and notes)
  - **Both recording and manual notes**

## Priority Rules

**CRITICAL:** When both recording and manual written information are provided:
- **Manual written information takes ABSOLUTE PRIORITY** - these are the user's conclusions and personal notes
- The recording should be used as supplementary context only
- The manual notes represent the user's final thoughts and must be preserved verbatim in the summary

## Your Task

1. **Invoke the cv-manager skill** to handle the "Add an Interview" workflow
2. The cv-manager skill will:
   - Verify the candidate exists
   - Process recording (if provided) using speech-to-text
   - Upload interview files to Google Drive backup
   - Extract interview date and attendees
   - Draft interview summary giving **absolute priority to manual written information**
   - Present the draft to the user for validation
   - Insert the interview entry into the tracking document
   - Clean up local files

## Important Notes

- **MUST use the cv-manager skill** - This is not a manual task
- The cv-manager skill knows the complete workflow and validation requirements
- **Manual notes are significantly more important** than transcribed recordings
- Follow all approval steps defined in the cv-manager skill workflow
- The skill will handle all Google Drive and Google Docs operations

**Trigger the cv-manager skill now to process the interview.**
