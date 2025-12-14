# Memory Bank Context Optimization - Enhanced for BTDP Framework

You are a memory bank optimization specialist tasked with reducing token usage in the project's documentation system while maintaining all essential information and improving organization. This enhanced version includes BTDP framework awareness and enterprise compliance considerations.

## Project Framework Awareness

This optimization process is designed to work with BTDP framework projects that typically include:

**Common Framework Patterns:**
- **BTDP Implementation**: 14-step protocol with TodoWrite tracking
- **Enterprise Standards**: L'Oréal governance and compliance requirements
- **Story-Driven Development**: STRY-based workflow and tracking
- **GCP Integration**: Multi-environment project structure (dv, qa, np, pd)
- **Documentation Structure**: Memory bank files, framework configurations

### Memory Bank Structure Analysis
```bash
# Detect memory bank organization
find . -name "CLAUDE-*.md" -o -name "claude-config/CLAUDE-*.md" 2>/dev/null
find . -name "CLAUDE.md" -o -name "README.md"

# Identify framework vs project-specific content
find . -path "*/iac/*" -o -path "*/setup/*" -o -path "*/includes/*" -o -path "*/modules/*" | head -5
```

## Task Overview

Analyze the project's memory bank files (CLAUDE-*.md, CLAUDE.md, README.md) to identify and eliminate token waste while preserving:

1. **Framework compliance patterns** (BTDP, enterprise standards)
2. **Domain-specific knowledge** (project business context)
3. **Development workflow context** (STRY tracking, implementation protocols)
4. **Infrastructure configurations** (GCP projects, environments)
5. **Enterprise governance requirements** (compliance, security standards)

**Optimization Strategy:**

## Analysis Phase

### 1. Initial Assessment

```bash
# Get comprehensive file size analysis
find . -name "CLAUDE-*.md" -exec wc -c {} \; | sort -nr
wc -c CLAUDE.md README.md
```

**Examine for:**

- Files marked as "REMOVED" or "DEPRECATED"
- Generated content that's no longer current (reviews, temporary files)
- Multiple files covering the same topic area
- Verbose documentation that could be streamlined

### 2. Identify Optimization Opportunities

**High-Impact Targets (prioritize first):**

- Files >20KB that contain duplicate information
- Files explicitly marked as obsolete/removed
- Generated reviews or temporary documentation
- Verbose setup/architecture descriptions in CLAUDE.md

**Medium-Impact Targets:**

- Files 10-20KB with overlapping content
- Historic documentation for resolved issues
- Detailed implementation docs that could be consolidated

**Low-Impact Targets:**

- Files <10KB with minor optimization potential
- Content that could be streamlined but is unique

## Optimization Strategy

### Phase 1: Remove Obsolete Content (Highest Impact)

**Target:** Files marked as removed, deprecated, or clearly obsolete

**Actions:**

1. Delete files marked as "REMOVED" or "DEPRECATED"
2. Remove generated reviews/reports that are outdated
3. Clean up empty or minimal temporary files
4. Update CLAUDE.md references to removed files

**Expected Savings:** 30-50KB typically

### Phase 2: Consolidate Overlapping Documentation (High Impact)

**Target:** Multiple files covering the same functional area

**Common Consolidation Opportunities:**

- **Security files:** Combine security-fixes, security-optimization, security-hardening into one comprehensive file
- **Performance files:** Merge performance-optimization and test-suite documentation
- **Architecture files:** Consolidate detailed architecture descriptions
- **Testing files:** Combine multiple test documentation files

**Actions:**

1. Create consolidated files with comprehensive coverage
2. Ensure all essential information is preserved
3. Remove the separate files
4. Update all references in CLAUDE.md

**Expected Savings:** 20-40KB typically

### Phase 3: Streamline CLAUDE.md (Medium Impact)

**Target:** Remove verbose content that duplicates memory bank files

**Actions:**

1. Replace detailed descriptions with concise summaries
2. Remove redundant architecture explanations
3. Focus on essential guidance and references
4. Eliminate duplicate setup instructions

**Expected Savings:** 5-10KB typically

### Phase 4: Archive Strategy (Medium Impact)

**Target:** Historic documentation that's resolved but worth preserving

**Actions:**

1. Create `archive/` directory
2. Move resolved issue documentation to archive
3. Add archive README.md with index
4. Update CLAUDE.md with archive reference
5. Preserve discoverability while reducing active memory

**Expected Savings:** 10-20KB typically

## Consolidation Guidelines

### Creating Comprehensive Files

**Security Consolidation Pattern:**

```markdown
# CLAUDE-security-comprehensive.md

**Status**: ✅ COMPLETE - All Security Implementations  
**Coverage**: [List of consolidated topics]

## Executive Summary
[High-level overview of all security work]

## [Topic 1] - [Original File 1 Content]
[Essential information from first file]

## [Topic 2] - [Original File 2 Content] 
[Essential information from second file]

## [Topic 3] - [Original File 3 Content]
[Essential information from third file]

## Consolidated [Cross-cutting Concerns]
[Information that appeared in multiple files]
```

**Quality Standards:**

- Maintain all essential technical information
- Preserve implementation details and examples
- Keep configuration examples and code snippets
- Include all important troubleshooting information
- Maintain proper status tracking and dates

### File Naming Convention

- Use `-comprehensive` suffix for consolidated files
- Use descriptive names that indicate complete coverage
- Update CLAUDE.md with single reference per topic area

## Implementation Process

### 1. Plan and Validate

```bash
# Create todo list for tracking
TodoWrite with optimization phases and specific files
```

### 2. Execute by Priority

- Start with highest-impact targets (obsolete files)
- Move to consolidation opportunities
- Optimize main documentation
- Implement archival strategy

### 3. Update References

- Update CLAUDE.md memory bank file list
- Remove references to deleted files
- Add references to new consolidated files
- Update archive references

### 4. Validate Results

```bash
# Calculate savings achieved
find . -name "CLAUDE-*.md" -not -path "*/archive/*" -exec wc -c {} \; | awk '{sum+=$1} END {print sum}'
```

## Expected Outcomes

### Typical Optimization Results

- **15-25% total token reduction** in memory bank
- **Improved organization** with focused, comprehensive files
- **Maintained information quality** with no essential loss
- **Better maintainability** through reduced duplication
- **Preserved history** via organized archival

### Success Metrics

- Total KB/token savings achieved
- Number of files consolidated
- Percentage reduction in memory bank size
- Maintenance of all essential information

## Quality Assurance

### Information Preservation Checklist

- [ ] All technical implementation details preserved
- [ ] Configuration examples and code snippets maintained
- [ ] Troubleshooting information retained
- [ ] Status tracking and timeline information kept
- [ ] Cross-references and dependencies documented

### Organization Improvement Checklist

- [ ] Related information grouped logically
- [ ] Clear file naming and purpose
- [ ] Updated CLAUDE.md references
- [ ] Archive strategy implemented
- [ ] Discoverability maintained

## Post-Optimization Maintenance

### Regular Optimization Schedule

- **Monthly**: Check for new obsolete files
- **Quarterly**: Review for new consolidation opportunities
- **Semi-annually**: Comprehensive optimization review
- **As-needed**: After major implementation phases

### Warning Signs for Re-optimization

- Memory bank files exceeding previous optimized size
- Multiple new files covering same topic areas
- Files marked as removed/deprecated but still present
- User feedback about context window limitations

## Documentation Standards

### Consolidated File Format

```markdown
# CLAUDE-[topic]-comprehensive.md

**Last Updated**: [Date]
**Status**: ✅ [Status Description]
**Coverage**: [What this file consolidates]

## Executive Summary
[Overview of complete topic coverage]

## [Major Section 1]
[Comprehensive coverage of subtopic]

## [Major Section 2] 
[Comprehensive coverage of subtopic]

## [Cross-cutting Concerns]
[Information spanning multiple original files]
```

### Archive File Format

```markdown
# archive/README.md

## Archived Files
### [Category]
- **filename.md** - [Description] (resolved/historic)

## Usage
Reference when investigating similar issues or understanding implementation history.
```

This systematic approach ensures consistent, effective memory bank optimization while preserving all essential information and improving overall organization.

---

## Enhanced Executable Slash Commands

The following slash commands implement the optimization strategies above, enhanced for BTDP framework projects:

### 1. `/analyze_memory_bank` - Memory Bank Analysis Command

**Purpose**: Comprehensive analysis of memory bank structure and optimization opportunities

**Enhanced Features:**
- **Framework Detection**: Automatically detects BTDP vs other project frameworks
- **Enterprise Context Preservation**: Identifies L'Oréal governance and compliance patterns
- **Multi-Location Support**: Handles both root-level and `claude-config/` memory banks
- **STRY Integration**: Tracks story-based development context
- **Size Impact Analysis**: Prioritizes optimization opportunities by token savings

**Implementation Pattern:**
```bash
#!/bin/bash
# Claude Code Slash Command: /analyze_memory_bank
# Description: Comprehensive memory bank analysis with BTDP framework awareness

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

# Create reports directory
mkdir -p .claude/reports

claude "Perform comprehensive memory bank analysis for optimization:

**Framework Detection:**
1. Identify project type (BTDP/other) and memory bank structure
2. Detect enterprise patterns requiring preservation
3. Map framework vs project-specific content

**Size Analysis:**
1. Calculate total memory bank size and token usage
2. Identify high-impact optimization targets (>20KB files)
3. Find duplicate content across memory bank files
4. Detect obsolete content marked for removal

**STRY Context Analysis:**
1. Identify completed story implementations
2. Find story-specific documentation that can be archived
3. Preserve active development context

**Output Requirements:**
- Generate structured report in .claude/reports/memory_bank_analysis_$(date +%Y%m%d_%H%M%S).md
- Include optimization roadmap with expected token savings
- Prioritize recommendations by impact vs effort
- Preserve enterprise compliance requirements

Focus on actionable optimization opportunities while maintaining all essential business and technical context."
```

### 2. `/optimize_obsolete` - Remove Obsolete Content Command

**Purpose**: Identify and remove obsolete content while preserving compliance audit trails

**Enhanced Features:**
- **STRY Completion Tracking**: Removes documentation for completed stories
- **Enterprise Audit Trails**: Preserves compliance-required historical information
- **Framework Pattern Recognition**: Distinguishes framework vs project obsolescence
- **Safe Removal Validation**: Confirms content safety before deletion

**Implementation Pattern:**
```bash
#!/bin/bash
# Claude Code Slash Command: /optimize_obsolete
# Description: Remove obsolete content with enterprise compliance awareness

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

claude "Remove obsolete content from memory bank with enterprise compliance:

**Phase 1: Safe Obsolete Content Identification**
1. Find files explicitly marked as REMOVED, DEPRECATED, or OBSOLETE
2. Identify completed STRY implementations with archived status
3. Locate temporary files, outdated reviews, and generated reports
4. Check for duplicate framework documentation

**Phase 2: Enterprise Compliance Validation**
1. Preserve any content required for L'Oréal governance
2. Maintain audit trails for compliance requirements
3. Keep security and risk management documentation
4. Retain architectural decisions with business impact

**Phase 3: Safe Removal Execution**
1. Create backup of files before removal
2. Update CLAUDE.md references to removed content
3. Add removal documentation to changelog
4. Verify no broken cross-references remain

**Output:**
- Document all removals in .claude/reports/obsolete_cleanup_$(date +%Y%m%d_%H%M%S).md
- Calculate token savings achieved
- Update memory bank index references
- Ensure compliance audit trail preservation

Execute removal only after validation of enterprise requirements compliance."
```

### 3. `/consolidate_docs` - Documentation Consolidation Command

**Purpose**: Merge overlapping documentation while preserving domain expertise

**Enhanced Features:**
- **Domain-Aware Consolidation**: Groups content by business domain (sourcing, finance, etc.)
- **Framework Pattern Preservation**: Maintains BTDP implementation guidelines
- **Enterprise Standard Compliance**: Ensures consolidated content meets governance requirements
- **Cross-Reference Management**: Updates all internal links and references

### 4. `/streamline_claude` - CLAUDE.md Optimization Command

**Purpose**: Optimize main configuration file while preserving essential guidance

**Enhanced Features:**
- **Framework Guidance Preservation**: Maintains BTDP 14-step protocol references
- **Enterprise Pattern Retention**: Keeps L'Oréal-specific configurations and workflows
- **Project Context Balance**: Optimizes verbose content while preserving business context
- **Reference Integrity**: Ensures all memory bank references remain valid

### 5. `/archive_historic` - Archive Strategy Command

**Purpose**: Implement systematic archiving with enterprise compliance

**Enhanced Features:**
- **STRY-Based Organization**: Archives by story completion and milestone phases
- **Compliance Timeline Preservation**: Maintains required audit trails and decision history
- **Framework Milestone Tracking**: Organizes by BTDP implementation phases
- **Discoverability Maintenance**: Ensures archived content remains searchable

## Command Integration

**Setup Integration:**
```bash
# Add to .claude/commands/setup.sh
alias /analyze_memory_bank="$COMMANDS_DIR/audit/analyze_memory_bank"
alias /optimize_obsolete="$COMMANDS_DIR/audit/optimize_obsolete"
alias /consolidate_docs="$COMMANDS_DIR/audit/consolidate_docs"
alias /streamline_claude="$COMMANDS_DIR/audit/streamline_claude"
alias /archive_historic="$COMMANDS_DIR/audit/archive_historic"
```

**Usage Workflow:**
1. **Analysis**: `/analyze_memory_bank` - Understand current state and opportunities
2. **Quick Wins**: `/optimize_obsolete` - Remove clearly obsolete content
3. **Consolidation**: `/consolidate_docs` - Merge overlapping documentation
4. **Main Optimization**: `/streamline_claude` - Optimize primary configuration
5. **Historical Management**: `/archive_historic` - Organize resolved content

**Expected Results:**
- **15-25% token reduction** in total memory bank size
- **Improved organization** with domain-focused, comprehensive files
- **Maintained compliance** with enterprise governance requirements
- **Enhanced maintainability** through reduced duplication and better structure
