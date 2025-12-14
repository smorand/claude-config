# PDF Extractor Reference Documentation

This directory contains detailed reference documentation for the PDF extractor skill.

## Quick Navigation

### Core References

**[Script Usage & Arguments](script-usage.md)** - 397 lines
- Complete run.sh command syntax and parameters
- All command-line arguments explained with examples
- Path requirements and best practices
- Batch processing examples
- Output path behavior
- Environment variables
- Error handling

**[Output Format](output-format.md)** - 555 lines
- Output directory structure
- document.md format and features
- images.md catalog format and structure
- Image classification types (photo, diagram, chart, etc.)
- Image file naming conventions
- Filtering and searching techniques
- File size expectations
- Integration with other tools

**[Workflows](workflows.md)** - 592 lines
- 10 common workflow examples with step-by-step instructions
- Summarizing PDFs with image context
- Filtering images by type
- Analyzing PDF structure
- Temporary analysis with cleanup
- Batch processing multiple PDFs
- Financial report extraction
- Technical documentation processing
- Research paper analysis
- Presentation content extraction
- Document comparison

**[Authentication](authentication.md)** - 584 lines
- Complete GCP and Vertex AI setup guide
- Installation instructions for gcloud CLI
- Authentication methods (ADC vs service accounts)
- IAM permissions and roles
- Region selection guide
- Comprehensive troubleshooting
- Security best practices
- Multi-project configuration
- Cost monitoring

**[Advanced Usage](advanced.md)** - 778 lines
- Custom extraction settings and parameters
- Image analysis customization
- Performance tuning and optimization
- Parallel processing
- Caching strategies
- Integration with other tools (Python, shell, web APIs)
- Custom output formats (HTML, JSON, CSV)
- Monitoring and logging
- Error recovery and retry logic
- Cost estimation

## Documentation Structure

```
references/
├── README.md              # This file - navigation guide
├── script-usage.md        # How to run the script
├── output-format.md       # What you get after extraction
├── workflows.md           # How to accomplish common tasks
├── authentication.md      # How to set up GCP/Vertex AI
└── advanced.md            # Customization and optimization
```

## When to Use Each Reference

### I want to...

**Run the script:**
→ Start with [script-usage.md](script-usage.md)
- Basic usage examples
- Command-line arguments
- Path requirements

**Understand the output:**
→ See [output-format.md](output-format.md)
- File structure
- Content formats
- How to filter images

**Accomplish a specific task:**
→ Check [workflows.md](workflows.md)
- 10 common workflows
- Step-by-step guides
- Use case examples

**Set up authentication:**
→ Follow [authentication.md](authentication.md)
- Initial setup guide
- Troubleshooting auth errors
- Security configuration

**Customize or optimize:**
→ Explore [advanced.md](advanced.md)
- Performance tuning
- Custom settings
- Integration examples

## Quick References

### Most Common Commands

```bash
# Basic extraction
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/document.pdf

# Custom output location
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/doc.pdf ~/analysis

# Temporary analysis
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor ~/Downloads/temp.pdf --cleanup
```

See [script-usage.md](script-usage.md) for more examples.

### Most Common Filters

```bash
# Find charts
grep -A 15 "**Type:** chart" images.md

# Exclude decorative images
grep -v "banner\|logo" images.md

# Find images with text
grep -B 5 "**Contains Text:** Yes" images.md
```

See [output-format.md](output-format.md) for more filtering techniques.

### Most Common Issues

**"PDF file not found"**
→ Use absolute paths (see [script-usage.md](script-usage.md))

**Authentication errors**
→ Run `gcloud auth application-default login` (see [authentication.md](authentication.md))

**Slow performance**
→ Check parallel processing options (see [advanced.md](advanced.md))

## Total Documentation

- **Main SKILL.md:** 270 lines (quick reference)
- **Reference docs:** 2,906 lines (detailed guides)
- **Total:** 3,176 lines of documentation

## Getting Started

1. **New users:** Start with main [SKILL.md](../SKILL.md) for overview
2. **First run:** Check [authentication.md](authentication.md) for setup
3. **Daily use:** Bookmark [script-usage.md](script-usage.md) and [workflows.md](workflows.md)
4. **Advanced users:** Explore [advanced.md](advanced.md) for customization

## Contributing

To update documentation:
1. Edit the relevant reference file
2. Keep examples practical and tested
3. Maintain consistent formatting
4. Update this README if adding new sections
