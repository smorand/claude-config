# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Documentation Maintenance

**IMPORTANT**: Whenever you modify this skill (add features, change workflows, update scripts), you MUST update both:
- **SKILL.md**: User-facing documentation with detailed workflows and requirements
- **CLAUDE.md**: AI-facing documentation with architecture and implementation details

These files must stay synchronized to ensure consistent behavior across user interactions and AI operations.

## Overview

This is an xlsx skill for comprehensive Excel file creation, editing, and analysis. It provides workflows for working with Excel files using Python, supporting formulas, formatting, data analysis, and visualization. The skill includes a critical formula recalculation utility (`recalc.py`) that uses LibreOffice to evaluate formulas and detect errors.

## Key Architecture Components

### 1. recalc.py - Formula Recalculation Script
**Location**: `/recalc.py`

**Purpose**: Recalculates all Excel formulas using LibreOffice and scans for formula errors across all cells in all sheets.

**Key Features**:
- Auto-configures LibreOffice macro on first run (macOS and Linux)
- Scans **all cells** in all sheets (no row/column limits)
- Detects all Excel error types: `#VALUE!`, `#DIV/0!`, `#REF!`, `#NAME?`, `#NULL!`, `#NUM!`, `#N/A`
- Returns structured JSON with error locations and counts
- Platform-aware (handles macOS vs Linux differences)

**Usage**:
```bash
python recalc.py <excel_file> [timeout_seconds]
```

**Return Format**:
```json
{
  "status": "success" | "errors_found",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

**Implementation Details**:
- Macro location: `~/Library/Application Support/LibreOffice/4/user/basic/Standard/Module1.xba` (macOS) or `~/.config/libreoffice/4/user/basic/Standard/Module1.xba` (Linux)
- Macro name: `RecalculateAndSave` in `Standard.Module1`
- Uses `load_workbook(data_only=True)` to check calculated values
- Uses `load_workbook(data_only=False)` to count formulas
- Default timeout: 30 seconds
- Returns first 20 error locations per error type

### 2. SKILL.md - Comprehensive Workflow Documentation
**Location**: `/SKILL.md`

Contains detailed requirements, standards, and workflows for Excel operations. Key sections:

**Requirements for Outputs**:
- **Zero Formula Errors**: All deliverables must have zero Excel errors
- **Preserve Templates**: Match existing format when modifying files
- **Financial Model Standards**: Color coding (blue=inputs, black=formulas, green=links, red=external, yellow=attention)
- **Number Formatting**: Years as text, currency with units, zeros as "-", percentages with 1 decimal

**Python Workflows**:
- **pandas**: Data analysis, bulk operations, simple exports
- **openpyxl**: Formulas, complex formatting, Excel-specific features

**Critical Rule**: Always use Excel formulas, never hardcode calculated values in Python

## Common Development Tasks

### Working with Excel Files

**Read and analyze data**:
```python
import pandas as pd
df = pd.read_excel('file.xlsx')  # First sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets
```

**Create new Excel with formulas**:
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Revenue'
sheet['B2'] = '=SUM(A2:A10)'  # Use formulas, not hardcoded values

# Format cells
sheet['A1'].font = Font(bold=True, color='0000FF')  # Blue for inputs
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')  # Yellow background

wb.save('output.xlsx')
```

**Edit existing Excel**:
```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb['SheetName']
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

**Manage sheets/tabs**:
```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')

# Create new sheet
new_sheet = wb.create_sheet('NewSheet')

# Rename sheet
wb['OldName'].title = 'NewName'

# Delete sheet
del wb['SheetName']
# or: wb.remove(wb['SheetName'])

wb.save('modified.xlsx')
```

**Recalculate formulas (MANDATORY after creating/editing formulas)**:
```bash
python recalc.py output.xlsx
```

### Fixing Formula Errors

When `recalc.py` returns `"status": "errors_found"`:

1. Check `error_summary` for error types and locations
2. Common fixes:
   - `#REF!`: Fix invalid cell references (check column mapping, row offsets)
   - `#DIV/0!`: Add zero-check to denominators
   - `#VALUE!`: Fix data type mismatches
   - `#NAME?`: Fix unrecognized function names
3. Re-run `recalc.py` after fixes

### Formula Verification Checklist

**Before running recalc.py**:
- Test 2-3 sample formulas first
- Verify column mapping (column 64 = BL, not BK)
- Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)
- Check for NaN values with `pd.notna()`
- Verify denominators are not zero
- Confirm cross-sheet references use correct format (Sheet1!A1)

## Important Gotchas

### openpyxl Behavior
- Cell indices are **1-based** (row=1, column=1 = A1)
- `data_only=True` reads calculated values but **PERMANENTLY LOSES FORMULAS** if you save
- Formulas are stored as strings and not evaluated until `recalc.py` runs
- Use `read_only=True` for reading or `write_only=True` for large files

### LibreOffice Dependencies
- LibreOffice must be installed (assume it is)
- Command: `soffice`
- First run auto-configures the macro
- Timeout handling differs between macOS (gtimeout) and Linux (timeout)

### Formula Rules
- **NEVER** calculate in Python and hardcode results
- **ALWAYS** use Excel formulas (=SUM(), =AVERAGE(), etc.)
- Place assumptions in separate cells, reference them in formulas
- Document data sources for hardcoded inputs

## Code Style

**Python code**: Minimal and concise, no verbose comments or unnecessary prints
**Excel files**: Add comments to complex formulas and document data sources

## Dependencies

Required Python packages:
- `openpyxl` - Excel file manipulation with formula support
- `pandas` - Data analysis and simple Excel operations

System requirements:
- LibreOffice (with `soffice` command available)
