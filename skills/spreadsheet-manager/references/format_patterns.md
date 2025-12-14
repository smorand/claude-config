# Format Patterns Reference

Common format patterns for Google Sheets cell formatting.

## Number Formats

- `#,##0` - Thousands separator, no decimals
- `#,##0.0` - One decimal place
- `#,##0.00` - Two decimal places
- `0` - Integer without separator
- `0.00` - Two decimals without separator

## Currency Formats

- `$#,##0.00` - US Dollar
- `€#,##0.00` - Euro
- `£#,##0.00` - British Pound
- `¥#,##0` - Japanese Yen (no decimals)
- `"$"#,##0.00_);("$"#,##0.00)` - Currency with negative in parentheses

## Date Formats

- `yyyy-mm-dd` - ISO format (2025-01-15)
- `mm/dd/yyyy` - US format (01/15/2025)
- `dd/mm/yyyy` - European format (15/01/2025)
- `mmmm d, yyyy` - Long format (January 15, 2025)
- `mmm dd` - Short month/day (Jan 15)

## Time Formats

- `hh:mm:ss` - 24-hour with seconds
- `hh:mm` - 24-hour without seconds
- `h:mm AM/PM` - 12-hour format
- `[h]:mm:ss` - Elapsed time (can exceed 24 hours)

## Percentage Formats

- `0%` - Whole percent
- `0.0%` - One decimal
- `0.00%` - Two decimals
- `0.000%` - Three decimals

## Special Formats

- `@` - Text format (shows exactly as entered)
- `[Red]0;[Blue]-0` - Conditional coloring
- `0.00E+00` - Scientific notation
