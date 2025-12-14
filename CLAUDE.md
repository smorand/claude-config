# Personal Configuration & Development Standards

## Personal Information

**Name:** Sebastien MORAND.
**Email:** sebastien.morand@loreal.com.
**Role:** CTO Data & AI at L'Oréal. In charge of Beauty Tech Data Platform (BTDP).
**ADM Identity:** sebastien.morand-adm@loreal.com (for sensitive GCP operations).
**L'Oréal GCP Organization ID:** 1090299993982.

---

## General rules

Whenever you make implementation on a project, you must ensure there is up-to-date following files:
- README.md to describe the project, how it works and how to use it
- CLAUDE.md for AI efficient interactions

When the user is refering to "Now" or "Today", you MUST use the `date` command to find exactly the date of today.

When the user says "I have a downloaded email" followed by a title or subject, it means the email is available in `~/Downloads/` folder as a `.eml` file. Search for `*.eml` files in that directory related to the provided title/subject. If the "downloaded" word is not mentionned, it can be professional email or personal email, use the appropriate skill.

---

## BTDP Masterdata & Resource Retrieval

**CRITICAL:** When the user asks to search, find, query, or get information about BTDP/L'Oréal resources (GCP projects, datasets, tables, groups, applications, repositories, domains, IT organizations, people, services, SKUs, APIs), you **MUST use the `btdp-it-masterdata-retrieval` skill**.

**DO NOT** filesystem commands (find, ls, grep) or direct bash commands (bq, gcloud) to search for BTDP resources without first loading the `btdp-it-masterdata-retrieval` skill and get the appropriate search protocol.

**Examples that MUST trigger the skill:**
- "Search for the project btdp sec"
- "Find the dataset for sales data"
- "What is the table for Global Spend"
- "Show me the group for data team"
- "Get the application for inventory"
- "List projects with btdp in the name"

Always use the skill for:** projects, datasets, tables, groups, applications, repositories, domains, IT organizations, people/users, services, SKUs, APIs, lineage queries.

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
- When you want to delete a file or a folder, use the `trash` command. **NEVER** use the `rm` command.
- When requested to run an API, if the method is "GET" then never put the header Content-Type. And if the target is api.loreal.net, then use the GCP access token except if said otherwise.
- When using `bq` tool, never forget to put options **BEFORE** the final line argument.
- When I say "Copy my password" or "Get my password", it means I want you to run `cat ~/.gcp/pwd|pbcopy` command
- When requesting to query a table, ensure first you load the schema.
- When a table in itg-btdppublished-gbl-ww is empty in production, check the current identity with `gcloud` command. If it's my ADM account, switch back to my standard account.

---

## Conversation Backup

I you are asked to backup the conversation, you need to copy the whole conversation and all the answers we have, the prompts, the error message in the folder ~/.claude/conversations

You will create a file with the date of the backup and a clear title.

The conversation must be backuped in the same language it occurs, no translation.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
error: cannot format -: Cannot parse: 5:0: **Name:** Sebastien MORAND.
