# Medical Article Writing Workflow

You are a medical article specialist. Execute this complete workflow to create a professional medical article from PDF sources. Think carefully and deeply about the workflow to generate a comprehensive TODO list according to the steps described below.

## Additional Context Processing

The user may provide additional instructions, data, or context alongside the base PDF documents:
- **Spreadsheets**: Results, data tables, statistical analysis (provide Spreadsheet ID)
- **Instruction PDFs**: Specific guidelines, focus areas, or requirements
- **Presentations**: Google Slides or PowerPoint with additional context or instructions

**Example invocation:**
```
/medical-article Create a new medical article based on the results in the Spreadsheet <spreadsheet_id> with instructions in the instruction.pdf file.
```

**Process additional context:**
1. If spreadsheet provided: Use `spreadsheet-manager` skill to read and analyze data
2. If instruction PDF provided: Extract using `pdf-extractor` skill, prioritize these instructions
3. If presentation provided: Use `google-slide-manager` or extract content as needed
4. Integrate all context into article planning and writing phases

## Prerequisites Validation

**Execute these MANDATORY checks before proceeding:**

1. **No CLAUDE.md exists** - Verify workspace is new
   - Check if CLAUDE.md file exists in current directory
   - If it exists: STOP and inform user this command is for new medical article projects only

2. **documents/ folder with PDFs exists**
   - Verify documents/ folder exists
   - Count PDF files in documents/ folder
   - If no PDFs found: STOP and inform user to add PDF files

**Error Handling:**
- **PDF extraction fails**: STOP the workflow and report the error to user
- **Google Drive upload fails**: STOP the workflow and report the error to user
- **No images in a specific article**: Continue - this is acceptable, not all PDFs may contain images

**If prerequisites fail, STOP and ask user to fix the setup.**

---

## Workflow Execution

Execute steps sequentially. Use TodoWrite to track progress.

### Step 1: Extract PDF Information

**Objective**: Extract all PDFs to `documents_md/` folder with AI image analysis

**Process:**
1. Create documents_md/ folder if it doesn't exist
2. For each PDF file in documents/ folder:
   - Use `pdf-extractor` skill to extract content
   - Specify output directory as documents_md/
   - Ensure AI image analysis is enabled
   - Verify extraction success before proceeding to next PDF
   - **If extraction fails**: STOP and report error to user

**What to extract:**
- Full text content in markdown
- AI-analyzed images with descriptions (images.md)
- Document structure and metadata

**Output structure:**
```
documents_md/
├── article1/
│   ├── document.md
│   ├── images.md (optional - may not exist if no images)
│   └── image-*.png (optional)
├── article2/
│   ├── document.md
│   ├── images.md (optional)
│   └── image-*.png (optional)
└── ...
```

---

### Step 2: Create Bibliography Database

**Objective**: Build numbered bibliography from PDF titles in alphabetical order

**Process:**
1. List all PDF files in documents/ folder
2. Extract title from each PDF (from filename or first page)
3. Sort titles alphabetically
4. Assign sequential numbers [1], [2], [3], etc.
5. Rename PDF files in documents/ using format: `<number> - <title>.pdf`
   - Use bash command: `mv "<doc_name>.pdf" "<number> - <title>.pdf"`
   - Numbering must be consistent and human-readable
   - Makes bibliography easier to reference
6. Store bibliography in memory for citation references throughout the article

**Bibliography format:**
```
1. [Author]. [Title]. [Journal/Publication]. [Year].
2. [Author]. [Title]. [Journal/Publication]. [Year].
...
```

**Adding new sources later:**
- New sources take the next sequential number (no renumbering of existing sources)
- Example: If bibliography has [1-5], new source becomes [6]

**Note**: Bibliography will be written to Google Doc in Step 7

---

### Step 3: Initialize Google Drive Folder

**Objective:** Backup documents and establish organized Google Drive structure

**Use `google-drive-manager` skill to:**

1. **Create main article folder** in parent folder ID: `1G27OoriS3eGyUCnly690J_vzAu1JoRGs`
   - Folder name format: `<YYYY-mm-dd> - <Label>`
   - If label is unclear, ask user for clarification
   - **If folder creation fails**: STOP and report error to user

2. **Create documents subfolder** within the main folder
   - Subfolder name: `documents`
   - **If subfolder creation fails**: STOP and report error to user

3. **Upload renamed PDFs** to documents subfolder
   - Upload all PDF files from documents/ folder (with their new numbered names)
   - **If any upload fails**: STOP and report error to user

**Important:**
- NEVER upload the `documents_md/` folder to Google Drive
- Store Google Drive folder URLs for CLAUDE.md documentation

---

### Step 4: Create Google Doc from Template

**Objective**: Initialize structured Google Doc for medical article

**Use `google-docs-manager` skill to:**

1. **Create new Google Doc** with appropriate title:
   - Title format: `Medical Article - [Topic from PDFs]`
   - Create in the Google Drive folder from Step 3: `<YYYY-mm-dd> - <Label>`

2. **Add initial structure** with Heading 1 style:
   ```markdown
   # Table of Contents
   [Will be populated after content creation]

   [Content sections will be added here]

   # Bibliography
   [Bibliography will be added here]
   ```

3. **Store Google Doc ID and URL** for later reference and CLAUDE.md documentation

**Output**: Google Doc URL and ID stored for subsequent steps

---

### Step 5: Analyze & Plan Document Structure

**Objective**: Deep analysis of all sources to create comprehensive article plan

**Deep analysis process:**

1. **Read all documents_md content:**
   - Read each document.md for text content
   - Read each images.md for visual content analysis (if exists)
   - Process any additional context (spreadsheets, instruction PDFs, presentations)
   - Identify key themes, methodologies, findings

2. **Synthesize information:**
   - Common themes across all sources
   - Contradictions or divergent findings
   - Methodological approaches
   - Statistical data and evidence
   - Clinical implications
   - Key visual data (charts, diagrams, medical images)

3. **Generate article outline with:**
   - Abstract (200-250 words)
   - Introduction (context, objectives)
   - Materials and Methods (if applicable)
   - Results (organized by theme)
   - Discussion (interpretation, limitations)
   - Conclusion
   - Bibliography

4. **Select images for article (3-6 total):**
   - Review all available images from documents_md/*/images.md files
   - Select images based on relevance to article content and narrative
   - Consider image descriptions and how they support the article
   - Do NOT exclude any images based on quality
   - Plan sequential numbering: Figure 1, Figure 2, Figure 3, etc.
   - Map each image to specific sections where they add value

5. **Plan image formatting:**
   - Each image caption format: `Figure X: [description from images.md] [N]`
   - X = sequential figure number (1, 2, 3...)
   - [N] = bibliography reference number for source document
   - Caption label must use italic style in Google Doc

**Output**: Detailed outline with section headings, content plan, and image placement map

---

### Step 6: Write Article Content

**Objective**: Populate Google Doc with high-quality medical article content

**Use `google-docs-manager` skill for all content writing and formatting**

**For each section:**

1. **Write scientifically rigorous content:**
   - Use formal medical/academic tone
   - Cite sources appropriately with [number] references
   - Present evidence-based information
   - Include statistical data where available
   - Acknowledge limitations and uncertainties
   - Use native Google Doc bullet points when creating lists

2. **Insert images (3-6 total across the article):**
   - Insert images according to the placement plan from Step 5
   - Upload images from documents_md/ folders inline at appropriate locations
   - Sequential numbering: Figure 1, Figure 2, Figure 3, etc.

   **Image caption format (STRICT):**
   ```
   Figure X: [Image description from images.md] [N]
   ```
   - "Figure X:" label in **italic style**
   - X = sequential figure number
   - [N] = bibliography reference number for source document
   - Example: *Figure 1:* Brain MRI showing lesion in temporal lobe [3]

3. **Add proper citations:**
   - Inline citations as [1], [2], [1,3], etc.
   - Multiple sources for important claims
   - Consistent citation style throughout

**CRITICAL Medical writing guidelines:**
- Use precise medical terminology
- Define abbreviations on first use
- Present conflicting evidence objectively
- Avoid overstatement of conclusions
- Maintain logical flow between sections
- Use clear, concise language
- **Write in natural human style** - document must appear written by a medical professional, not AI

**Track all images used:**
- Maintain list of all figures and their sources for CLAUDE.md documentation

---

### Step 7: Complete Bibliography Section

**Objective**: Add formatted bibliography to Google Doc

**Use `google-docs-manager` skill to:**

1. Navigate to "Bibliography" section in Google Doc
2. Add each source from Step 2 bibliography in numerical order
3. Format consistently with medical citation style

**Bibliography entry format:**
```
1. [Full citation from PDF metadata or title]
2. [Full citation from PDF metadata or title]
...
```

**Verification (will be done in Step 9):**
- All cited numbers [1], [2], etc. will be checked for corresponding bibliography entries
- Bibliography numbering consistency will be verified
- Citation formatting will be validated

---

### Step 8: Finalize Table of Contents

**Objective**: Prepare Table of Contents section

**Process:**
- The table of contents cannot be auto-generated by the skill
- Create a section with Heading 1 style named "Table of Contents"
- Leave it with just a blank line
- User will manually generate TOC in Google Docs if needed

---

### Step 9: Quality Verification

**Objective**: Validate article quality and completeness before finalization

**Perform the following checks:**

1. **Citation Verification:**
   - Verify all citations [1], [2], [N] in the article have corresponding bibliography entries
   - Check for any orphaned bibliography entries (not cited in article)
   - Ensure citation numbering is consistent

2. **Image Verification:**
   - Confirm 3-6 images are present in the document
   - Verify all images have proper captions: *Figure X:* description [N]
   - Check figure numbering is sequential (1, 2, 3...)
   - Ensure "Figure X:" labels use italic style
   - Verify no orphaned image files (selected but not inserted)

3. **Content Completeness:**
   - Confirm all sections have content (Abstract, Introduction, Methods, Results, Discussion, Conclusion)
   - Verify bibliography section is complete
   - Check Table of Contents section exists

4. **Medical Terminology:**
   - Spot-check for proper medical terminology usage
   - Verify abbreviations are defined on first use
   - Ensure professional, human-written tone throughout

**Document quality check results:**
- Record findings for success confirmation summary
- If critical issues found, report to user before proceeding

---

### Step 10: Create CLAUDE.md

**Objective**: Document project metadata and workflow instructions for future prompting sessions

**Process:**
1. Create CLAUDE.md in current directory using the template from **Appendix A**
2. Populate all bracketed fields with actual values:
   - Google Drive URLs
   - Google Doc URL and ID
   - Current date (use `date` command)
   - Bibliography database (full list)
   - Images used (all figures)
   - Content sections
3. Upload CLAUDE.md to the main Google Drive folder (not documents subfolder)

**Purpose:** This CLAUDE.md enables normal prompting workflow for all future article modifications and iterations

---

## Success Confirmation

After completing all steps, provide user with comprehensive summary:

```
✅ Medical Article Workflow Complete!

📄 **Google Doc:** [URL]
📁 **Google Drive Folder:** [URL]
📚 **Sources processed:** [Number] PDFs
📑 **Bibliography entries:** [Number]
🖼️  **Figures inserted:** [Number] images

📊 **Quality Verification Results:**
   ✓ Citations: [Number] citations verified, all matched to bibliography
   ✓ Images: [Number] figures with proper formatting (*Figure X:* style)
   ✓ Content: All sections complete (Abstract, Introduction, Methods, Results, Discussion, Conclusion, Bibliography)
   ✓ Medical terminology: Professional tone maintained
   [Note any warnings or items requiring user attention]

📂 **Project Structure:**
   - documents/ → [Number] renamed PDFs with bibliography numbers
   - documents_md/ → Extracted content and images
   - CLAUDE.md → Project documentation (uploaded to Google Drive)
   - Google Drive → PDFs backed up, Google Doc created

🔄 **Next Steps:**
   1. Review Google Doc content: [Google Doc URL]
   2. Manually generate Table of Contents in Google Docs (Insert > Table of Contents)
   3. Edit and refine article as needed
   4. To add sources: Follow instructions in CLAUDE.md
   5. After local edits: git add . && git commit -m "Updated: [description]"

📖 **Open your article:** [Google Doc URL]
```

---

## Appendix A: CLAUDE.md Template

Use this template when creating CLAUDE.md in Step 10. Replace all [bracketed] fields with actual values.

```markdown
# Medical Article Project

## Project Information

**Google Drive Folder:** [Insert Google Drive Folder URL]
**Google Drive Folder for PDFs:** [Insert Google Drive Folder/documents URL]
**Google Doc:** [Insert Google Doc URL]
**Google Doc ID:** [Insert Document ID]
**Created:** [Current date - use `date` command]
**Source Documents:** [Number] PDF files

## Workflow Summary

This medical article was generated from PDF sources using an automated workflow:

1. PDF extraction with AI image analysis → documents_md/
2. Bibliography creation from source documents
3. Google Drive folder structure creation
4. Google Doc creation from template
5. Content synthesis and article writing
6. Image insertion (3-6 figures) with proper formatting
7. Bibliography completion
8. Table of Contents preparation
9. Quality verification

## Bibliography Database

[List all PDF files from documents/ folder with full citation information and reference numbers, matching the bibliography in the Google Doc]

Example format:
1. [Author]. [Title]. [Journal/Publication]. [Year].
2. [Author]. [Title]. [Journal/Publication]. [Year].

## Images Used in Article

[List all figures inserted in the document]

Example format:
- Figure 1: [description] - Source: documents_md/[folder]/image-X.png - Reference: [N]
- Figure 2: [description] - Source: documents_md/[folder]/image-Y.png - Reference: [N]

## Content Sections

[List main sections in the article with Heading levels]

Example:
- Abstract
- Introduction
- Materials and Methods
- Results
- Discussion
- Conclusion
- Bibliography

## Important Instructions for Future Modifications

### Adding New Sources
1. Add PDF to documents/ folder
2. Use `pdf-extractor` skill to extract to documents_md/
3. Update bibliography with next sequential number (NO renumbering of existing sources)
4. Upload new PDF to Google Drive documents/ folder
5. Update article content with new citations [N]
6. Update this CLAUDE.md with new bibliography entry

### Modifying Content
- Always modify document per section when reviewing paragraphs
- Use native Google Doc bullet points for lists
- Maintain medical professional tone and human-written style
- Update CLAUDE.md when making structural changes

### Maintaining CLAUDE.md
- Keep CLAUDE.md synchronized with document structure
- Update bibliography when sources added
- Update images list when figures added/removed
- Upload updated CLAUDE.md to Google Drive folder after modifications
```

---

## User Request

Here is the user additional information to take in account: $ARGUMENTS
