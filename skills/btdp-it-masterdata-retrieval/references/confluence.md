# Confluence

## Search Confluence

### Basic Search

```python
mcp__atlassian__confluence_search(
    query="<search_query>",          # Text or CQL query
    limit=10,                        # Max: 50, default: 10
    spaces_filter=None               # Comma-separated space keys
)
```

**Simple Text Search Examples:**
```python
# Basic text search (uses siteSearch with fallback to text)
confluence_search(query="project documentation", limit=10)

# Search with limit
confluence_search(query="meeting notes", limit=20)

# Filter by spaces
confluence_search(
    query="technical specs",
    spaces_filter="DEV,TECH",
    limit=15
)
```

### CQL Search Examples

**CQL (Confluence Query Language) provides advanced filtering**

```python
# Basic CQL search
confluence_search(query='type=page AND space=DEV', limit=10)

# Personal space search (quote space keys starting with ~)
confluence_search(query='space="~username"', limit=10)

# Search by title
confluence_search(query='title~"Meeting Notes"', limit=10)

# Site search (semantic)
confluence_search(query='siteSearch ~ "important concept"', limit=10)

# Text search (full-text)
confluence_search(query='text ~ "important concept"', limit=10)

# Recent content
confluence_search(query='created >= "2023-01-01"', limit=20)

# Content with label
confluence_search(query='label=documentation', limit=10)

# Recently modified
confluence_search(query='lastModified > startOfMonth("-1M")', limit=10)

# Content modified this year
confluence_search(
    query='creator = currentUser() AND lastModified > startOfYear()',
    limit=20
)

# Content you contributed to recently
confluence_search(
    query='contributor = currentUser() AND lastModified > startOfWeek()',
    limit=15
)

# Watched content
confluence_search(
    query='watcher = "user@domain.com" AND type = page',
    limit=10
)

# Exact phrase search
confluence_search(
    query='text ~ "\\"Urgent Review Required\\"" AND label = "pending-approval"',
    limit=10
)

# Title wildcards
confluence_search(
    query='title ~ "Minutes*" AND (space = "HR" OR space = "Marketing")',
    limit=10
)

# Multiple spaces with date filter
confluence_search(
    query='(space = "DEV" OR space = "TECH") AND created > "2024-01-01"',
    limit=20
)
```

**CQL Tips:**
- Personal space keys starting with `~` must be quoted: `space="~username"`
- Use `siteSearch ~` for semantic search (mimics WebUI search)
- Use `text ~` for full-text search
- Use `title ~` for title matching with wildcards (`*`)
- Quote special identifiers, reserved words, and strings with special chars
- Date functions: `startOfMonth()`, `startOfYear()`, `startOfWeek()`
- Current user: `currentUser()`, `contributor`, `watcher`

---

## Get Page Content

### By Page ID

```python
mcp__atlassian__confluence_get_page(
    page_id="<page_id>",              # Numeric ID from URL
    include_metadata=True,            # Include metadata (default: True)
    convert_to_markdown=True          # Convert to markdown (default: True)
)
```

**Example:**
```python
# Get page by ID (from URL: .../pages/123456789/Page+Title)
confluence_get_page(page_id="123456789")

# Get raw HTML (for macros not visible in markdown)
confluence_get_page(
    page_id="123456789",
    convert_to_markdown=False  # CAUTION: increases token usage
)

# Get content only (no metadata)
confluence_get_page(
    page_id="123456789",
    include_metadata=False
)
```

### By Title and Space

```python
mcp__atlassian__confluence_get_page(
    title="<exact_title>",
    space_key="<space_key>",
    include_metadata=True,
    convert_to_markdown=True
)
```

**Example:**
```python
# Get page by title and space
confluence_get_page(
    title="Project Requirements",
    space_key="DEV"
)
```

**Notes:**
- `page_id` takes precedence over `title` + `space_key`
- Markdown conversion is recommended (HTML increases token usage)
- Metadata includes creation date, last update, version, labels

---

## Get Child Pages

```python
mcp__atlassian__confluence_get_page_children(
    parent_id="<parent_page_id>",
    expand="version",                 # Fields to expand (default: "version")
    limit=25,                         # Max: 50, default: 25
    include_content=False,            # Include page content (default: False)
    convert_to_markdown=True,         # If include_content=True
    start=0                           # Pagination offset (0-based)
)
```

**Examples:**
```python
# Get child pages (metadata only)
confluence_get_page_children(parent_id="123456789")

# Get child pages with content
confluence_get_page_children(
    parent_id="123456789",
    include_content=True,
    limit=10
)

# Pagination
confluence_get_page_children(
    parent_id="123456789",
    start=25,
    limit=25
)
```

---

## Get Comments

```python
mcp__atlassian__confluence_get_comments(
    page_id="<page_id>"
)
```

**Example:**
```python
confluence_get_comments(page_id="123456789")
```

---

## Get Labels

```python
mcp__atlassian__confluence_get_labels(
    page_id="<page_id>"
)
```

**Example:**
```python
confluence_get_labels(page_id="123456789")
```

---

## Add Label

```python
mcp__atlassian__confluence_add_label(
    page_id="<page_id>",
    name="<label_name>"
)
```

**Example:**
```python
confluence_add_label(page_id="123456789", name="documentation")
```

---

## Create Page

```python
mcp__atlassian__confluence_create_page(
    space_key="<space_key>",          # e.g., "DEV", "TECH"
    title="<page_title>",
    content="<page_content>",
    parent_id=None,                   # Optional parent page ID
    content_format="markdown",        # "markdown", "wiki", or "storage"
    enable_heading_anchors=False      # Markdown only
)
```

**Examples:**
```python
# Create markdown page
confluence_create_page(
    space_key="DEV",
    title="New Documentation Page",
    content="# Header\n\nContent here...",
    content_format="markdown"
)

# Create as child page
confluence_create_page(
    space_key="DEV",
    title="Sub Page",
    content="# Content",
    parent_id="123456789"
)

# Create with wiki markup
confluence_create_page(
    space_key="DEV",
    title="Wiki Page",
    content="h1. Header\n\nContent...",
    content_format="wiki"
)

# Enable heading anchors (markdown)
confluence_create_page(
    space_key="DEV",
    title="Page with Anchors",
    content="# Section 1\n\n# Section 2",
    content_format="markdown",
    enable_heading_anchors=True
)
```

**Content Formats:**
- `markdown` - Standard Markdown (default)
- `wiki` - Confluence wiki markup
- `storage` - Confluence storage format (HTML-based)

---

## Update Page

```python
mcp__atlassian__confluence_update_page(
    page_id="<page_id>",
    title="<new_title>",
    content="<new_content>",
    is_minor_edit=False,
    version_comment=None,
    parent_id=None,                   # New parent page ID
    content_format="markdown",
    enable_heading_anchors=False
)
```

**Examples:**
```python
# Update page content
confluence_update_page(
    page_id="123456789",
    title="Updated Title",
    content="# Updated Content"
)

# Minor edit with comment
confluence_update_page(
    page_id="123456789",
    title="Page Title",
    content="# Content",
    is_minor_edit=True,
    version_comment="Fixed typo"
)

# Move page (change parent)
confluence_update_page(
    page_id="123456789",
    title="Page Title",
    content="# Content",
    parent_id="987654321"
)
```

---

## Delete Page

```python
mcp__atlassian__confluence_delete_page(
    page_id="<page_id>"
)
```

**Example:**
```python
confluence_delete_page(page_id="123456789")
```

---

## Add Comment

```python
mcp__atlassian__confluence_add_comment(
    page_id="<page_id>",
    content="<comment_content>"  # Markdown format
)
```

**Example:**
```python
confluence_add_comment(
    page_id="123456789",
    content="This looks good. Approved!"
)
```

---

## Search Users

```python
mcp__atlassian__confluence_search_user(
    query="<cql_query>",
    limit=10  # Max: 50, default: 10
)
```

**Example:**
```python
# Search by full name
confluence_search_user(query='user.fullname ~ "First Last"', limit=10)
```

---

## Best Practices

1. **Use siteSearch for discovery** - mimics WebUI search behavior
2. **Use text search for precision** - full-text search on content
3. **Filter by spaces** to reduce noise
4. **Use CQL for advanced filtering** - dates, labels, contributors
5. **Get page by ID when known** - faster than title + space lookup
6. **Convert to markdown by default** - reduces token usage vs HTML
7. **Include metadata** for context (dates, version, labels)
8. **Use child pages** for hierarchical content
9. **Add labels** for categorization and filtering
10. **Use version comments** when updating pages for audit trail

## Common Use Cases

### Find recent documentation
```python
confluence_search(
    query='type=page AND label=documentation AND lastModified > startOfMonth("-1M")',
    limit=20
)
```

### Find my recent contributions
```python
confluence_search(
    query='contributor = currentUser() AND lastModified > startOfWeek()',
    limit=15
)
```

### Find pages in multiple spaces
```python
confluence_search(
    query='(space = "DEV" OR space = "TECH") AND created > "2024-01-01"',
    limit=20
)
```

### Get page hierarchy
```python
# Get parent page
parent = confluence_get_page(page_id="123456789")

# Get all children
children = confluence_get_page_children(parent_id="123456789", limit=50)
```
