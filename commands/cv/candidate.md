---
description: Add a new candidate CV to the tracking system using cv-manager skill
---

# Add Candidate CV

You must use the **cv-manager** skill to process this candidate CV and add it to the tracking system.

## Input Requirements

The user will provide a CV document file path. This is the candidate's CV that needs to be processed.

## Your Task

1. **Invoke the cv-manager skill** to handle the "Add a CV" workflow
2. The cv-manager skill will:
   - Extract text from the CV document
   - Analyze and draft job title and description
   - Present the draft to me for review
   - Upload the CV to Google Drive
   - Insert the candidate entry into the tracking document
   - Clean up local files

## Important Notes

- **MUST use the cv-manager skill** - This is not a manual task
- The cv-manager skill knows the complete workflow and validation requirements
- Follow all approval steps defined in the cv-manager skill workflow
- The skill will handle all Google Drive and Google Docs operations

**Trigger the cv-manager skill now to process the candidate CV.**
