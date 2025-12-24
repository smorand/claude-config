# Personal Configuration & Development Standards

## Personal Information

**Name:** Sebastien MORAND.
**Email:** seb.morand@gmail.com.
**Role:** CTO Data & AI at L'Oréal. In charge of Beauty Tech Data Platform (BTDP).

---

## General rules

Whenever you make implementation on a project, you must ensure there is up-to-date following files:
- README.md to describe the project, how it works and how to use it
- CLAUDE.md for AI efficient interactions

When the user is refering to "Now" or "Today", you MUST use the `date` command to find exactly the date of today.

When the user says "I have a downloaded email" followed by a title or subject, it means the email is available in `~/Downloads/` folder as a `.eml` file. Search for `*.eml` files in that directory related to the provided title/subject. If the "downloaded" word is not mentionned, it can be professional email or personal email, use the appropriate skill.

---

## GCP Operations & Command Execution

**CRITICAL:** When the user asks to run, execute, or use GCP commands (`bq`, `gcloud`, `gsutil`) or perform operations on Google Cloud Platform, you **MUST use the `gcp-specialist` skill**.

**DO NOT** run `bq`, `gcloud`, or `gsutil` commands directly via Bash without first loading the `gcp-specialist` skill to ensure proper command syntax, authentication, and best practices.

**Examples that MUST trigger the skill:**
- "Run a BigQuery query on..."
- "Use bq to list datasets"
- "Execute gcloud command to..."
- "Copy files with gsutil"
- "List BigQuery tables"
- "Check IAM permissions with gcloud"
- "Deploy Cloud Function"
- "Query this BigQuery table"

**Always use the skill for:** BigQuery operations (bq), Cloud SDK commands (gcloud), Cloud Storage operations (gsutil), IAM permissions, service accounts, resource deployment, and any GCP infrastructure operations.

---

## Other information

- When asked to send in the clipboard, use `cat` and the pbcopy command
- When asked to get information from the clipboard, use pbpaste command (in a file on in your context according to the task)
- When speaking about "downloads", "my downloads", it references the ~/Downloads folder.
- When requiring to list locally, use /bin/ls to ensure it's working as expected
- When I'm talking about date and time, to ensure you know the current date & time always use the `date` commnand
- **NEVER** use a find command on my home, if you really think that could be the only way to solve a request, ask first how to do.
- When using `bq` tool, never forget to put options **BEFORE** the final line argument.
- When requesting to query a table, ensure first you load the schema.

---

## Conversation Backup

I you are asked to backup the conversation, you need to copy the whole conversation and all the answers we have, the prompts, the error message in the folder ~/.claude/conversations

You will create a file with the date of the backup and a clear title.

The conversation must be backuped in the same language it occurs, no translation.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
