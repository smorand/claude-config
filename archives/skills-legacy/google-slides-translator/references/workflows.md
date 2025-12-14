# Translation Workflows

## Quick Translation Workflow

When users request slide translation, follow this workflow:

### 1. Extract Presentation ID
- Ask for Google Slides URL if not provided
- Extract ID from URL: `https://docs.google.com/presentation/d/PRESENTATION_ID/edit`

### 2. Determine Slide Range
- "All slides" → use `all`
- "Slides 10 to 15" → use `10-15`
- "Slide 5" → use `5`
- "Slides 1, 3, 5" → use `1,3,5`

### 3. Identify Target Language
- Use 2-letter language code (see language-codes.md)
- Common codes: fr, es, de, it, pt, ja, zh, ko

### 4. Execute Translation
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <id> <range> <lang>
```

### 5. Monitor & Report
- Watch output for progress and errors
- Report completion statistics
- Handle errors with appropriate troubleshooting

## Example Interactions

### Translate Entire Presentation

**User:** "Translate this Google Slides to French: https://docs.google.com/presentation/d/1abc123xyz/edit"

**Response:**
```
I'll translate your Google Slides presentation to French.

Presentation ID: 1abc123xyz
Target Language: French (fr)
Slides: All

Running translation...
```

**Execute:**
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz all fr
```

**Report:**
```
✅ Translation complete!

Summary:
- Slides translated: 25/25
- Text elements updated: 150
- Target language: French

Your presentation has been successfully translated to French.
All formatting, styles, and layout have been preserved.
```

### Translate Specific Range

**User:** "Translate slides 10 through 15 to Spanish"

**Execute:**
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 10-15 es
```

### Translate Selected Slides

**User:** "Translate slides 1, 5, and 10 to German"

**Execute:**
```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 1,5,10 de
```

## Best Practices

### Before Translation
- **Backup first:** Make a copy of the presentation
- **Clean formatting:** Ensure consistent formatting across slides
- **Review content:** Check for special characters or formatting issues

### During Translation
- **Monitor output:** Watch for progress and error messages
- **Network stability:** Ensure stable internet connection
- **API quotas:** Be mindful of Google Cloud Translation API quotas

### After Translation
- **Review quality:** Check translated content for accuracy
- **Verify formatting:** Ensure all styles preserved correctly
- **Test links:** Verify hyperlinks still work

## Batch Processing

For multiple presentations:

```bash
# Translate presentation 1 to French
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123 all fr

# Translate presentation 2 to Spanish
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 2def456 all es

# Translate presentation 3 to German
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 3ghi789 all de
```

## Error Handling

The script includes automatic error handling:
- **Partial failures:** Continues even if individual elements fail
- **Progress tracking:** Shows which slides are being processed
- **Retry logic:** Re-run script if network issues occur
- **Detailed errors:** Provides specific error messages for troubleshooting

## Translation Quality Tips

### Source Content
- **Auto-detection:** Works best with clear, well-written text
- **Context:** Provide context clues for better translation
- **Short segments:** Quality improves with shorter text blocks

### Target Language
- **Language codes:** Use correct 2-letter ISO codes
- **Regional variants:** Some languages have regional codes (e.g., pt-BR)

## Technical Details

### Formatting Preservation
The script uses `replaceAllText` API which preserves:
- Text formatting (bold, italic, underline)
- Font families and sizes
- Colors and backgrounds
- Text alignment and spacing
- Hyperlinks and special characters

### Translation Process
1. Authenticates with Google APIs using OAuth 2.0
2. Fetches presentation structure
3. Extracts text from all text elements in specified slides
4. Auto-detects source language
5. Translates each text element using Google Cloud Translation API
6. Updates presentation in-place using `replaceAllText`
7. Reports translation progress and statistics

### Limitations
- **No new documents:** Updates original (no copy created)
- **Text only:** Only translates text elements (not images with text)
- **No tables:** Table content translation not implemented
- **Sequential:** Processes slides one at a time
