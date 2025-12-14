# SQL Generation Skill

Optimized SQL specialist for BigQuery in L'Oréal BTDP environment.

## Structure

```
sql-generation/
├── SKILL.md                          # Main skill (179 lines) - Quick reference
└── references/                       # Detailed documentation
    ├── coding-rules.md              # Complete SQL standards (462 lines)
    ├── scenario-adhoc.md            # Ad-hoc analysis patterns (473 lines)
    ├── scenario-materialized.md     # Materialized views (542 lines)
    ├── scenario-dataprep.md         # MERGE patterns (559 lines)
    ├── time-queries.md              # Time-based queries (560 lines)
    └── discovery.md                 # RAG & SDDS tools (585 lines)
```

## Quick Start

The main **SKILL.md** provides:
- MANDATORY coding rules (uppercase, joins, no SELECT *)
- Scenario selection guide (ad-hoc vs materialized vs data prep)
- Discovery workflow (RAG and SDDS tools)
- Quick optimization checklist
- Links to detailed references

## Optimization Summary

**Before**: 459 lines in single file
**After**: 179 lines main + 3,181 lines in detailed references

### Key Improvements

1. **Focused Main Skill** (179 lines):
   - Essential MANDATORY rules at top
   - Quick scenario decision tree
   - Concise examples
   - Links to detailed guides

2. **Comprehensive References**:
   - Complete coding standards with examples
   - Scenario-specific deep dives
   - Time-based query patterns
   - Discovery tool workflows

3. **Easy Navigation**:
   - SKILL.md for quick reference during queries
   - Reference files for detailed implementation
   - Clear structure by topic/scenario

## Usage Pattern

1. **Start with SKILL.md** - Review mandatory rules and select scenario
2. **Reference detailed guides** - Follow scenario-specific patterns
3. **Use discovery tools** - Find tables/schemas before writing SQL
4. **Apply time-query patterns** - Never hardcode dates
5. **Validate and optimize** - Follow coding rules checklist

## Mandatory Rules (Always Apply)

1. **UPPERCASE keywords** - All SQL keywords must be uppercase
2. **Explicit JOINs** - INNER JOIN, LEFT OUTER JOIN (full keywords)
3. **No SELECT *** - Always specify columns explicitly
4. **Dynamic dates** - Never hardcode dates, use DATE_SUB/CURRENT_DATE

See [SKILL.md](SKILL.md) for complete quick reference.
