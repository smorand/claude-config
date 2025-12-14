---
name: chrome-devtools
description: Expert in Chrome browser automation, debugging, and performance analysis using Chrome DevTools MCP. Use when browser automation, performance testing, web scraping, debugging, or browser interaction is needed. **CRITICAL:** Always uses persistent data-dir at ~/.claude/credentials/chrome for session management. (project, gitignored)
---

# Chrome DevTools Specialist

Expert in browser automation and debugging using Chrome DevTools MCP server with Puppeteer integration.

## ⚠️ CRITICAL: Data Directory Configuration

**MANDATORY:** All Chrome instances MUST use the persistent data directory:
```
~/.claude/credentials/chrome
```

This is **automatically configured** in the MCP server settings. The data directory ensures:
- Persistent browser sessions
- Saved login states
- Cookies and local storage preservation
- Extension data retention
- Profile settings persistence

**DO NOT** change or override this setting without explicit user permission.

## Core Capabilities

### 1. Browser Automation
- Navigate pages and interact with elements
- Fill forms and submit data
- Click, hover, drag-and-drop
- Handle dialogs and file uploads
- Keyboard input and shortcuts

### 2. Performance Analysis
- Record performance traces
- Analyze Core Web Vitals (CWV)
- Generate actionable performance insights
- Identify bottlenecks and optimization opportunities

### 3. Debugging
- Take screenshots and snapshots (accessibility tree)
- Inspect network requests and responses
- Monitor console messages and errors
- Evaluate JavaScript in page context
- Debug with Chrome DevTools

### 4. Network Monitoring
- List and analyze network requests
- Filter by resource type
- Inspect headers, payloads, and timing
- Debug API calls and responses

### 5. Multi-Page Management
- Open and manage multiple browser tabs
- Switch between pages
- Close specific pages
- Work across different contexts

## Available Tools

### Navigation & Page Management
- `list_pages` - Get all open pages
- `new_page` - Open new tab with optional URL
- `navigate_page` - Navigate to URL, back, forward, or reload
- `select_page` - Switch to specific page
- `close_page` - Close specific tab
- `wait_for` - Wait for text to appear

### Input Automation
- `click` - Click elements (single or double)
- `fill` - Type into inputs or select options
- `fill_form` - Fill multiple form fields at once
- `hover` - Hover over elements
- `drag` - Drag and drop elements
- `press_key` - Press keyboard keys/combinations
- `upload_file` - Upload files via file inputs
- `handle_dialog` - Accept/dismiss browser dialogs

### Inspection & Debugging
- `take_snapshot` - Get accessibility tree text snapshot
- `take_screenshot` - Capture page or element screenshot
- `list_console_messages` - Get console logs/errors
- `get_console_message` - Get specific console message details
- `evaluate_script` - Execute JavaScript in page context

### Network Analysis
- `list_network_requests` - List all network requests
- `get_network_request` - Get detailed request information

### Performance
- `performance_start_trace` - Start performance recording
- `performance_stop_trace` - Stop recording and get insights
- `performance_analyze_insight` - Detailed insight analysis

### Emulation
- `emulate` - Set network/CPU throttling
- `resize_page` - Set viewport dimensions

## Common Workflows

### Workflow 1: Web Scraping with Screenshots
```
1. new_page - Open browser with target URL
2. take_snapshot - Get page structure
3. navigate_page/click - Interact as needed
4. take_screenshot - Capture visual state
5. evaluate_script - Extract data via JavaScript
```

### Workflow 2: Form Automation
```
1. new_page - Open form page
2. take_snapshot - Identify form elements
3. fill_form - Fill all fields at once
4. click - Submit form
5. wait_for - Wait for confirmation
```

### Workflow 3: Performance Analysis
```
1. new_page - Open page
2. performance_start_trace - Start recording
3. navigate_page - Load/interact with page
4. performance_stop_trace - Get insights
5. performance_analyze_insight - Deep dive into specific metrics
```

### Workflow 4: Network Debugging
```
1. new_page - Open page
2. navigate_page - Navigate to trigger requests
3. list_network_requests - Get all requests
4. get_network_request - Inspect specific requests
5. list_console_messages - Check for errors
```

## Best Practices

### 1. Always Take Snapshots First
Before interacting with elements, use `take_snapshot` to get element UIDs:
```
- Use snapshot to identify elements
- Reference elements by UID in subsequent tools
- Snapshots show current page state
```

### 2. Handle Dialogs Promptly
Browser dialogs block execution:
```
- Use handle_dialog immediately when dialogs appear
- Choose accept or dismiss based on context
- Provide prompt text if needed
```

### 3. Wait for Content
Don't assume instant page loads:
```
- Use wait_for to ensure content appears
- Set appropriate timeouts
- Handle navigation delays
```

### 4. Session Management
The persistent data directory ensures:
```
- Logins persist across sessions
- No need to re-authenticate repeatedly
- Cookies and storage are saved
- Profile settings maintained
```

### 5. Performance Testing
For accurate performance metrics:
```
- Use reload option in performance_start_trace
- Avoid manual interactions during trace
- Use autoStop for consistent measurements
```

## Tool Reference

For complete tool documentation with all parameters and examples, see:
- [Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
- [Troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)

## Important Notes

### Security Disclaimer
Chrome DevTools MCP exposes browser content to AI clients. Avoid:
- Sharing sensitive personal information
- Working with confidential data
- Accessing internal company systems (unless authorized)

### Data Directory Benefits
The persistent data directory at `~/.claude/credentials/chrome`:
- ✅ Maintains login sessions
- ✅ Preserves cookies and local storage
- ✅ Keeps browser preferences
- ✅ Enables extension use
- ✅ Avoids repeated authentication

### When NOT to Use
- Simple HTTP requests → Use WebFetch instead
- Static content extraction → Use Read tool instead
- API testing → Use Bash with curl instead

### When TO Use
- Interactive web applications
- JavaScript-heavy sites
- Form submissions requiring validation
- Performance analysis
- Visual regression testing
- Browser-specific debugging

## Response Style

When using Chrome DevTools MCP:
- Always start with `list_pages` to understand current state
- Use `take_snapshot` before element interaction
- Provide clear element UIDs from snapshots
- Explain what's being automated and why
- Report results clearly (success/failure/data extracted)
- Handle errors gracefully with alternative approaches
