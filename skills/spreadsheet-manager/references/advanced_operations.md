# Advanced Operations

Additional spreadsheet operations beyond the core script.

## Sheet Management

Create sheet:
```bash
# Get spreadsheet metadata first to find sheet structure
# Then use Sheets API batchUpdate with addSheet request
```

Delete/rename sheets, row/column operations: Use `batchUpdate` with appropriate requests.

## Style Copying

Copy formatting from template range to target range using `copyPaste` request with `PASTE_FORMAT` type.

## Borders

Apply borders using `updateBorders` request with style (SOLID/DASHED/DOTTED), width, and color.

## Conditional Formatting

Use `addConditionalFormatRule` request with boolean or gradient rules.

## Data Validation

Create dropdowns and validation rules with `setDataValidation` request.

## Named Ranges

Define named ranges for formulas with `addNamedRange` request.

## Protected Ranges

Lock cells/sheets using `addProtectedRange` request.

## Charts

Create charts with `addChart` request specifying chart type and data ranges.

## Pivot Tables

Create pivot tables with `updateCells` and pivot table specifications.

## Filters

Apply filters with `setBasicFilter` request.

## Version Management

Use Drive API revisions endpoint to list/restore versions.

##Export to Excel

Use Drive API `export` with MIME type `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`.

All operations use the batchUpdate method for efficiency. Combine multiple requests in single API call.
