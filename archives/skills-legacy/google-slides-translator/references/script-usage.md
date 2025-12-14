# Script Usage Reference

## Command Pattern

```bash
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides <presentation_id> <slide_range> <target_lang>
```

## Arguments

### presentation_id
The unique identifier from the Google Slides URL.

Example URL: `https://docs.google.com/presentation/d/1abc123xyz/edit`
Presentation ID: `1abc123xyz`

### slide_range
Specifies which slides to translate.

**Formats:**
- `all` - Translate all slides in the presentation
- `5` - Translate only slide 5
- `10-15` - Translate slides 10 through 15 (inclusive)
- `1,3,5` - Translate slides 1, 3, and 5
- `2-4,6-8` - Translate slides 2-4 and 6-8 (multiple ranges)

### target_lang
Two-letter language code for the target language (see language-codes.md for full list).

## Examples

```bash
# Translate all slides to French
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz all fr

# Translate slides 10-15 to Spanish
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 10-15 es

# Translate specific slides to German
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 1,5,10 de

# Translate multiple ranges to Italian
~/.claude/skills/google-slides-translator/scripts/run.sh translate_slides 1abc123xyz 2-4,6-8 it
```

## How run.sh Works

The `run.sh` script uses `uv` for automatic dependency management:

1. **Auto-creates virtual environment** (`.venv`) on first run
2. **Installs dependencies** from `pyproject.toml`
3. **Executes Python script** with complete isolation
4. **No manual setup required** - just run the script

First run may take a few seconds to set up. Subsequent runs are instant.

## Output Format

```
✅ Authenticated successfully
📊 Translating slides in presentation: 1abc123xyz
🌍 Target language: fr
📄 Slide range: all
📝 Presentation: My Presentation Title
📊 Total slides: 25
🎯 Translating 25 slide(s): [1, 2, 3, ..., 25]

🔄 Processing slide 1...
  ✅ Translated element g1234abc...
  ✅ Translated element g5678def...
  📊 Slide 1: 2 elements translated

[... continues for all slides ...]

✅ Translation complete!
📊 Slides translated: 25/25
📝 Total text elements translated: 150
```

## Performance Notes

- **Large presentations:** 50+ slides may take several minutes
- **Network dependent:** Speed depends on internet connection to Google APIs
- **Sequential processing:** Slides processed one at a time
- **Progress tracking:** Real-time output shows current slide being processed
