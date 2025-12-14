# Common Workflows

Detailed workflows and use cases for PDF extraction and analysis.

## Workflow 1: Summarize PDF Document with Image Context

**Goal:** Extract and summarize PDF content including both text and visual elements

### Steps

1. **Extract PDF with AI image analysis**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/report.pdf
   ```

2. **Read text content**
   ```bash
   cat ~/Downloads/report/document.md
   ```

3. **Review image catalog**
   ```bash
   cat ~/Downloads/report/images.md
   ```

4. **Filter relevant images** (optional)
   ```bash
   # Find charts and data visualizations
   grep -A 15 "**Type:** chart" ~/Downloads/report/images.md
   grep -A 15 "**Type:** graph" ~/Downloads/report/images.md

   # Exclude decorative elements
   grep -v "banner\|logo\|icon" ~/Downloads/report/images.md
   ```

5. **Combine insights**
   - Summarize text from document.md
   - Include key findings from charts/diagrams in images.md
   - Filter out decorative elements (banners, logos)
   - Provide comprehensive summary with both text and visual context

### Use Cases

- Executive summaries of reports
- Research paper analysis
- Financial report reviews
- Presentation content extraction
- Document understanding for Q&A

### Expected Output

**Summary includes:**
- Main text content themes
- Key data from charts and graphs
- Important diagrams explained
- Tables and data points
- Filtered view without decorative elements

## Workflow 2: Extract and Filter Relevant Images

**Goal:** Find and filter specific types of images (charts, diagrams, etc.)

### Steps

1. **Extract PDF to analysis directory**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/presentation.pdf ~/analysis
   ```

2. **Review image catalog**
   ```bash
   cat ~/analysis/presentation/images.md
   ```

3. **Find specific image types**
   ```bash
   # Find all charts
   grep -B 2 "**Type:** chart" ~/analysis/presentation/images.md

   # Find all diagrams
   grep -B 2 "**Type:** diagram" ~/analysis/presentation/images.md

   # Find all tables
   grep -B 2 "**Type:** table" ~/analysis/presentation/images.md
   ```

4. **Exclude decorative images**
   ```bash
   # Remove banners and logos from view
   grep -v "banner\|logo" ~/analysis/presentation/images.md

   # Find only data visualizations
   grep -E "chart|graph|table|diagram" ~/analysis/presentation/images.md
   ```

5. **Extract image file names**
   ```bash
   # Get list of chart files
   grep -B 2 "**Type:** chart" ~/analysis/presentation/images.md | grep "Path:" | sed 's/.*`\(.*\)`.*/\1/'

   # Copy filtered images to separate folder
   mkdir ~/analysis/charts
   grep -B 2 "**Type:** chart" ~/analysis/presentation/images.md | grep "Path:" | sed 's/.*`\(.*\)`.*/\1/' | \
       while read img; do cp ~/analysis/presentation/"$img" ~/analysis/charts/; done
   ```

### Use Cases

- Extract only data visualizations
- Find technical diagrams
- Identify images with embedded text for OCR
- Filter out marketing/branding elements
- Locate specific visual content types
- Create image subsets for specific purposes

### Filter Examples

**Data visualizations only:**
```bash
grep -E "Type:** (chart|graph|table)" images.md
```

**Technical content:**
```bash
grep -E "Type:** (diagram|screenshot|table)" images.md
```

**Photos and realistic images:**
```bash
grep -E "Type:** (photo|illustration)" images.md
```

**Images with text:**
```bash
grep -B 5 "**Contains Text:** Yes" images.md
```

## Workflow 3: Analyze PDF Structure with Visual Content

**Goal:** Understand document structure, organization, and visual element distribution

### Steps

1. **Extract PDF**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Documents/document.pdf
   ```

2. **Extract document structure**
   ```bash
   # Get table of contents from headings
   grep "^#" ~/Documents/document/document.md

   # Example output:
   # # Document Title
   # ## Chapter 1: Introduction
   # ### Section 1.1
   # ### Section 1.2
   # ## Chapter 2: Analysis
   ```

3. **Count visual elements by type**
   ```bash
   grep "**Type:**" ~/Documents/document/images.md | sort | uniq -c

   # Example output:
   #    5 **Type:** banner
   #   12 **Type:** chart
   #    8 **Type:** diagram
   #    3 **Type:** logo
   #    6 **Type:** table
   #    2 **Type:** photo
   ```

4. **Map images to document sections**
   ```bash
   # Find which sections contain data visualizations
   grep -n "^##" ~/Documents/document/document.md > sections.txt
   grep -n "!\[image\]" ~/Documents/document/document.md > images.txt
   ```

5. **Identify key data visualizations**
   ```bash
   # Find all charts and their contexts
   grep -A 15 "chart\|graph\|table" ~/Documents/document/images.md
   ```

### Use Cases

- Document structure analysis
- Content inventory
- Visual element distribution
- Section organization review
- Data visualization mapping
- Content type analysis

### Analysis Outputs

**Structure Report:**
- Number of sections/chapters
- Heading hierarchy
- Total images count
- Images per section
- Visual element types distribution

**Visual Content Analysis:**
- Data visualization count
- Technical diagrams count
- Decorative elements count
- Images with text
- Photo/illustration count

## Workflow 4: Temporary Analysis with Cleanup

**Goal:** Analyze PDF content without keeping extracted files

### Steps

1. **Extract with cleanup flag**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/temp_doc.pdf --cleanup
   ```

2. **The script automatically:**
   - Extracts text to document.md
   - Analyzes all images with AI
   - Creates images.md catalog
   - Displays complete content
   - **Deletes output directory**

3. **Content is displayed but not saved**
   - View content during execution
   - No files remain after completion
   - Useful for one-time analysis

### Use Cases

- Quick document review
- Temporary content analysis
- Disk space conservation
- Batch processing without storage
- One-time information extraction
- Ephemeral analysis tasks

### Advanced: Save Output Separately

```bash
# Save displayed content to file while using cleanup
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc.pdf --cleanup > /tmp/analysis.txt

# Content deleted from default location, but saved in custom file
cat /tmp/analysis.txt
```

## Workflow 5: Batch Process Multiple PDFs

**Goal:** Extract content from multiple PDFs systematically

### Basic Batch Processing

```bash
# Process all PDFs in directory (default paths)
for pdf in ~/Downloads/*.pdf; do
    echo "Processing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf"
done

# Result: Each PDF extracted to folder in same directory
# ~/Downloads/doc1/ ~/Downloads/doc2/ etc.
```

### Centralized Batch Processing

```bash
# Process all PDFs to central location
for pdf in ~/Downloads/*.pdf; do
    echo "Processing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" ~/analysis
done

# Result: All extractions in ~/analysis/
# ~/analysis/doc1/ ~/analysis/doc2/ etc.
```

### Batch with Cleanup and Logging

```bash
# Process PDFs, save summaries, cleanup extractions
for pdf in ~/Downloads/*.pdf; do
    echo "=== Processing: $pdf ===" >> ~/analysis/batch_log.txt
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" --cleanup >> ~/analysis/batch_log.txt 2>&1
    echo "" >> ~/analysis/batch_log.txt
done

# Result: All content in log file, no extraction folders kept
```

### Selective Batch Processing

```bash
# Process only PDFs matching pattern
for pdf in ~/Downloads/*report*.pdf; do
    echo "Processing: $pdf"
    ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor "$pdf" ~/reports
done
```

### Parallel Batch Processing

```bash
# Process multiple PDFs in parallel (use with caution - API rate limits)
find ~/Downloads -name "*.pdf" -type f | parallel -j 4 \
    '~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor {} ~/analysis'

# Processes 4 PDFs at a time
```

### Use Cases

- Process entire directories
- Centralize extractions
- Create analysis archives
- Systematic document processing
- Bulk content extraction

## Workflow 6: Extract Data from Financial Reports

**Goal:** Extract and analyze financial data, charts, and tables

### Steps

1. **Extract financial report**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/Q4_Report.pdf ~/finance
   ```

2. **Find financial charts**
   ```bash
   # Find all charts and graphs
   grep -A 15 "**Type:** chart" ~/finance/Q4_Report/images.md
   grep -A 15 "**Type:** graph" ~/finance/Q4_Report/images.md
   ```

3. **Find financial tables**
   ```bash
   grep -A 15 "**Type:** table" ~/finance/Q4_Report/images.md
   ```

4. **Extract numerical data from text**
   ```bash
   # Find currency amounts
   grep -E '\$[0-9,]+' ~/finance/Q4_Report/document.md

   # Find percentages
   grep -E '[0-9]+%' ~/finance/Q4_Report/document.md
   ```

5. **Combine insights**
   - Text-based financial metrics
   - Chart descriptions (revenue trends, growth, etc.)
   - Table data (detailed breakdowns)
   - Exclude decorative elements (logos, banners)

### Use Cases

- Quarterly report analysis
- Annual report review
- Financial statement extraction
- Investment analysis
- Budget report processing

## Workflow 7: Extract Technical Documentation

**Goal:** Extract technical diagrams, architecture, and documentation

### Steps

1. **Extract technical PDF**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Documents/architecture.pdf ~/tech_docs
   ```

2. **Find technical diagrams**
   ```bash
   # Find all diagrams
   grep -A 15 "**Type:** diagram" ~/tech_docs/architecture/images.md

   # Find screenshots
   grep -A 15 "**Type:** screenshot" ~/tech_docs/architecture/images.md
   ```

3. **Identify flowcharts and process flows**
   ```bash
   grep -i "flowchart\|workflow\|process" ~/tech_docs/architecture/images.md
   ```

4. **Extract code blocks** (if any)
   ```bash
   # Find code sections in document
   grep -A 10 '```' ~/tech_docs/architecture/document.md
   ```

5. **Map diagrams to sections**
   ```bash
   # Find which sections contain diagrams
   grep -n "^##" ~/tech_docs/architecture/document.md
   grep -n "!\[image\].*diagram" ~/tech_docs/architecture/document.md
   ```

### Use Cases

- System architecture extraction
- API documentation processing
- Technical specification analysis
- Workflow documentation
- Process diagram extraction

## Workflow 8: Research Paper Analysis

**Goal:** Extract and analyze academic/research papers

### Steps

1. **Extract research paper**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/research_paper.pdf ~/research
   ```

2. **Get paper structure**
   ```bash
   # Extract headings (Abstract, Introduction, Methods, Results, etc.)
   grep "^#" ~/research/research_paper/document.md
   ```

3. **Find research figures**
   ```bash
   # Find charts (results, data visualizations)
   grep -A 15 "**Type:** chart" ~/research/research_paper/images.md

   # Find diagrams (methodologies, models)
   grep -A 15 "**Type:** diagram" ~/research/research_paper/images.md

   # Find tables (data tables)
   grep -A 15 "**Type:** table" ~/research/research_paper/images.md
   ```

4. **Extract key sections**
   ```bash
   # Extract abstract
   sed -n '/^# Abstract/,/^#/p' ~/research/research_paper/document.md

   # Extract conclusions
   sed -n '/^# Conclusion/,/^#/p' ~/research/research_paper/document.md
   ```

5. **Analyze visual data**
   - Review experimental results charts
   - Understand methodology diagrams
   - Analyze data tables
   - Filter out journal branding

### Use Cases

- Academic paper review
- Literature analysis
- Research data extraction
- Methodology understanding
- Results visualization review

## Workflow 9: Presentation Content Extraction

**Goal:** Extract slide content and visuals from presentations

### Steps

1. **Extract presentation**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/presentation.pdf ~/presentations
   ```

2. **Review slide structure**
   ```bash
   # Each slide often becomes a section
   grep "^#" ~/presentations/presentation/document.md
   ```

3. **Filter slide content**
   ```bash
   # Exclude title slides, logos, decorative banners
   grep -v "banner\|logo" ~/presentations/presentation/images.md

   # Find actual content (charts, diagrams, photos)
   grep -E "Type:** (chart|diagram|photo|table)" ~/presentations/presentation/images.md
   ```

4. **Extract key visuals**
   ```bash
   # Find data slides
   grep -A 15 "**Type:** chart" ~/presentations/presentation/images.md

   # Find concept slides
   grep -A 15 "**Type:** diagram" ~/presentations/presentation/images.md
   ```

5. **Reconstruct narrative**
   - Combine text content
   - Include key visual descriptions
   - Maintain slide order
   - Exclude branding elements

### Use Cases

- Meeting presentation review
- Slide deck analysis
- Presentation content extraction
- Key points identification
- Visual content cataloging

## Workflow 10: Document Comparison

**Goal:** Compare content across multiple PDF versions or documents

### Steps

1. **Extract all versions**
   ```bash
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc_v1.pdf ~/comparison
   ~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc_v2.pdf ~/comparison
   ```

2. **Compare text content**
   ```bash
   # Use diff to compare documents
   diff ~/comparison/doc_v1/document.md ~/comparison/doc_v2/document.md

   # Or use a better diff tool
   git diff --no-index ~/comparison/doc_v1/document.md ~/comparison/doc_v2/document.md
   ```

3. **Compare image counts**
   ```bash
   # Count images in each version
   wc -l ~/comparison/doc_v1/images.md
   wc -l ~/comparison/doc_v2/images.md
   ```

4. **Compare image types**
   ```bash
   # Compare image type distribution
   grep "**Type:**" ~/comparison/doc_v1/images.md | sort | uniq -c
   grep "**Type:**" ~/comparison/doc_v2/images.md | sort | uniq -c
   ```

5. **Identify changes**
   - Text additions/deletions
   - New/removed images
   - Changed visualizations
   - Updated data

### Use Cases

- Document version comparison
- Change tracking
- Update analysis
- Content evolution review
- Revision identification

## Best Practices for Workflows

### General Guidelines

1. **Use full paths** - Always use absolute paths for PDFs
2. **Check output first** - Review extraction before processing
3. **Filter early** - Remove decorative elements early in workflow
4. **Combine data sources** - Use both document.md and images.md
5. **Save intermediate results** - Keep filtered outputs for reference

### Performance Tips

1. **Use cleanup for temporary work** - Save disk space
2. **Batch similar operations** - Process multiple PDFs together
3. **Choose nearby region** - Use closest GCP region for speed
4. **Monitor API costs** - Track Vertex AI usage for large batches
5. **Cache results** - Don't re-extract unless needed

### Organization Tips

1. **Use custom output dirs** - Centralize related extractions
2. **Name outputs clearly** - Use descriptive folder names
3. **Create analysis projects** - Group related PDFs together
4. **Document workflows** - Save commands and scripts
5. **Archive results** - Keep important extractions organized
