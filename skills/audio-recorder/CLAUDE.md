# Audio Recorder - AI Instructions

## Critical Rules for Audio Recording

### Always Use the Script

**NEVER** run sox commands directly. **ALWAYS** use the provided script:

```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh {start|stop|status} [label]
```

The script handles:
- PID tracking
- Clean shutdown
- Stale process cleanup
- Label sanitization
- Status extraction

### Understanding User Intent

**Map these user phrases to operations**:

| User Says | Operation | Command |
|-----------|-----------|---------|
| "Start recording" | Start with "Unknown" label | `record.sh start` |
| "Record this" | Start with "Unknown" label | `record.sh start` |
| "Start recording one2one Jean" | Start with label | `record.sh start "one2one Jean"` |
| "Record team meeting" | Start with label | `record.sh start "team meeting"` |
| "Stop recording" | Stop | `record.sh stop` |
| "Done recording" | Stop | `record.sh stop` |
| "Am I recording?" | Check status | `record.sh status` |
| "What am I recording?" | Check status | `record.sh status` |
| "Recording status" | Check status | `record.sh status` |
| "How long have I been recording?" | Check status | `record.sh status` |

### Label Extraction from Context

**Extract labels intelligently**:

✅ **GOOD**: Extract meaningful labels
- "Start recording one2one with Marcelo" → `one2one_Marcelo`
- "Record my team standup" → `team_standup`
- "Start recording the steering committee" → `steering_committee`
- "Record quarterly review" → `quarterly_review`

❌ **BAD**: Don't use generic labels when context is available
- "Start recording one2one with Marcelo" → ~~`Unknown`~~
- "Record the meeting" → Consider asking: "What meeting are you recording?"

### Status Response Formatting

When the user asks about recording status, **parse and present the information clearly**:

**Script Output**:
```
✓ Recording in progress (PID: 12345)

Label: one2one Marcelo
Started: 2025-11-11 at 14:30:45
Duration: 15m 32s

Full path: /Users/sebastien.morand/Downloads/Records/2025-11-11_14:30:45_one2one_Marcelo.ogg
Current size: 2.3M
```

**Your Response**:
```
Yes, you're currently recording:

📝 Label: one2one Marcelo
⏰ Started: 14:30:45 (running for 15m 32s)
💾 File size: 2.3M

File: ~/Downloads/Records/2025-11-11_14:30:45_one2one_Marcelo.ogg
```

### Automatic Stop Before Start

**Important**: When starting a new recording while one is running, the script **automatically stops the old recording first**. This is expected behavior.

**Your Response Should Reflect This**:
```
User: Start recording new meeting
Assistant: Stopping current recording "one2one Marcelo" first...
          Recording stopped successfully.

          Starting new recording: new_meeting
          Recording started (PID: 12347)
```

### Contextual Stopping

**If user says "done" or "finished" during a conversation about recording**, interpret as stop command:

```
User: Start recording team standup
Assistant: Recording started: team_standup.ogg

[... conversation continues ...]

User: Done
Assistant: [Checks if recording active, if so stops it]
          Recording stopped successfully.
```

**But be careful**:
- Only stop if recording is active
- Only stop if context clearly indicates they mean recording
- If unsure, ask: "Do you want me to stop the recording?"

### Error Handling

**If sox not installed**:
```
Error: sox: command not found

Please install sox to use recording:
brew install sox
```

**If microphone permission denied**:
```
Error: Cannot open audio device

Please grant microphone permissions:
System Preferences → Security & Privacy → Privacy → Microphone
```

**If stale PID detected**:
```
Detected a stale recording process. Cleaning up and starting fresh...
Recording started: [filename]
```

### Integration Workflow Patterns

#### Pattern 1: Record and Update Topic

```
User: Start recording one2one Jean
Assistant: Recording started: 2025-11-11_15:30:22_one2one_Jean.ogg (PID: 12345)

[... conversation ...]

User: Stop recording
Assistant: Recording stopped successfully.

User: Update my one 2 one with Jean topic using this recording
Assistant: [Invokes topic-manager skill]
          [Uploads recording to topic's Records folder]
          [Transcribes using speech-to-text skill]
          [Updates topic with minutes]
```

**Key**: Keep track of the most recent recording filename to use when updating topics.

#### Pattern 2: Status Check During Recording

```
User: Start recording team meeting
Assistant: Recording started: 2025-11-11_10:00:00_team_meeting.ogg (PID: 12345)

[... 15 minutes pass ...]

User: How long have I been recording?
Assistant: [Runs record.sh status]
          You've been recording "team meeting" for 15m 32s (started at 10:00:00)
          Current file size: 2.3M
```

#### Pattern 3: Quick Replace

```
User: Am I recording?
Assistant: [Runs record.sh status]
          Yes, you're recording "old meeting" (started 90m ago, 5.2M)

User: Start recording new meeting
Assistant: [Script automatically stops old, starts new]
          Stopped "old meeting" recording.
          Started new recording: new_meeting.ogg (PID: 12347)
```

### Best Practices

1. **Always run status before stop**: Prevents "no recording" errors
2. **Extract labels from context**: Don't default to "Unknown" unnecessarily
3. **Confirm after start/stop**: Always show the filename and PID (start) or success message (stop)
4. **Parse status output**: Present it in a user-friendly format
5. **Track recent files**: Remember the latest recording for topic updates

### Common Mistakes to Avoid

❌ Running sox directly instead of using the script
❌ Forgetting to extract label from user's message
❌ Not checking status before attempting operations
❌ Not informing user when automatically stopping old recording
❌ Using generic responses instead of parsing script output
❌ Not tracking the recording filename for later use

### Quality Checklist

Before responding to recording requests, verify:

- [ ] Used the script (`record.sh`), not direct sox command
- [ ] Extracted label from user message if provided
- [ ] Checked status before stop (if appropriate)
- [ ] Parsed script output and formatted user-friendly response
- [ ] Confirmed operation with filename/PID/status
- [ ] Tracked filename for potential topic updates
- [ ] Handled errors appropriately with helpful messages

### Script Path Reference

**Always use the full path**:
```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh
```

**Never use**:
- `record.sh` (may not be in PATH)
- `./record.sh` (wrong working directory)
- Direct sox commands

### Context Awareness

**Be smart about context**:

If the user is in the middle of a meeting discussion and says:
- "Let me start recording" → Extract meeting context for label
- "I need to capture this" → Start recording with context-based label
- "Can you record this for me?" → Start recording

If there's no clear context:
- Ask: "What would you like me to label this recording?"
- Or use "Unknown" as fallback

### List Recordings Format

**When the user asks to list recordings**, present the results in a table format with the following columns:

| File name | Size | Date | Time | Label | In progress |
|-----------|------|------|------|-------|-------------|
| 2025-11-11_15:53:11_test4.ogg | 751K | 2025-11-11 | 15:53:11 | test4 | false |
| 2025-11-11_15:44:04_test3.ogg | 4.2M | 2025-11-11 | 15:44:04 | test3 | false |
| 2025-11-11_15:39:21_Production_Test.ogg | 2.0M | 2025-11-11 | 15:39:21 | Production Test | false |
| 2025-11-11_15:38:48_Unknown.ogg | 249K | 2025-11-11 | 15:38:48 | Unknown | false |
| 2025-11-11_15:36:25_test.ogg | 999K | 2025-11-11 | 15:36:25 | test | false |

**Key points**:
- Extract Date and Time from the filename (format: YYYY-MM-DD_HH:MM:SS)
- Extract Label from the filename (convert underscores back to spaces)
- Mark "In progress" as `true` for the currently recording file, `false` for all others
- Sort by most recent first (newest at top)
- Include total count at the bottom

**Example with active recording**:

| File name | Size | Date | Time | Label | In progress |
|-----------|------|------|------|-------|-------------|
| 2025-11-11_15:53:11_one2one_Jean.ogg | 850K | 2025-11-11 | 15:53:11 | one2one Jean | true |
| 2025-11-11_15:44:04_test3.ogg | 4.2M | 2025-11-11 | 15:44:04 | test3 | false |
| 2025-11-11_15:39:21_Production_Test.ogg | 2.0M | 2025-11-11 | 15:39:21 | Production Test | false |

**Total: 3 recordings (1 active)**

### Response Templates

**Start Success**:
```
Recording started: [filename]
PID: [pid]
```

**Start with Auto-Stop**:
```
Stopping current recording "[old_label]" first...
Recording stopped successfully.

Starting new recording: [filename]
Recording started (PID: [new_pid])
```

**Stop Success**:
```
Recording stopped successfully.
File: [filename]
```

**Status Active**:
```
Yes, you're currently recording:

📝 Label: [label]
⏰ Started: [time] (running for [duration])
💾 File size: [size]

File: [full_path]
```

**Status Inactive**:
```
No recording is currently active.
```

This ensures consistent, helpful responses for all recording operations.
