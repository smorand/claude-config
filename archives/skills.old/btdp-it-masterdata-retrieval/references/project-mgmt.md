# Project Management (Stories, Epics, Sprints, Enhancements)

## User Stories

### Get Stories (Filtered)

```python
mcp__mcprelay__itbm_get_stories(
    # Exact match filters
    product_name=None,              # Exact product name
    application_service_name=None,  # Exact application service name
    application_service_number=None, # Exact service number (SNSVCxxxxxxx)
    user_story_number=None,         # Exact story number (STRYxxxxxxx)
    epic_name=None,                 # Exact epic name
    epic_number=None,               # Exact epic number (EPICxxxxxxx)

    # Contains filters (partial match)
    title=None,                     # Story title/short_description
    assignment_group=None,          # Single value or list
    app_service_number=None,        # CMDB CI number (SNSVCxxxxxxx)
    app_service_name=None,          # CMDB CI name
    product=None,                   # Product name
    service_name=None,              # Enhancement's app service name
    theme=None,                     # Theme
    sprint=None,                    # Sprint name

    # Priority filter (1-5 or list)
    priority=None,  # 1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning

    # Story points range
    min_story_points=None,
    max_story_points=None,

    # State filter (1-7 or list)
    state=None,  # 1=Draft, 2=Ready, 3=WIP, 4=Ready for Testing, 5=Testing, 6=Complete, 7=Cancel

    # Date filters (ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
    created_before=None,
    created_after=None,
    updated_before=None,
    updated_after=None,
    time_zone="Europe/Paris",

    # Pagination
    limit=50  # Max: 50, default: 50
)
```

**Examples:**
```python
# Get stories for a specific epic
itbm_get_stories(epic_number="EPIC0001234", limit=50)

# Get high priority stories in progress
itbm_get_stories(priority="2", state=3, limit=30)

# Get stories by assignment group
itbm_get_stories(
    assignment_group="IT-GLOBAL-GCP-BTDP-DATA",
    state=[2, 3, 4],  # Ready, WIP, Ready for Testing
    limit=50
)

# Get recent stories
itbm_get_stories(
    created_after="2025-01-01",
    state=[3, 4, 5],  # WIP, Testing, Complete
    limit=50
)

# Get stories by product
itbm_get_stories(
    product="BTDP",
    state=[2, 3],
    priority=["1", "2"],  # Critical and High
    limit=50
)

# Get stories with story points
itbm_get_stories(
    min_story_points=5,
    max_story_points=13,
    state=3  # WIP
)

# Get stories by sprint
itbm_get_stories(sprint="Sprint 2025-01", limit=50)

# Search by title
itbm_get_stories(title="data migration", limit=20)
```

### Get Single Story

```python
mcp__mcprelay__itbm_get_story(
    sys_id_or_number="<story_number>"  # STRYxxxxxxx or sys_id
)
```

**Example:**
```python
itbm_get_story(sys_id_or_number="STRY0001234")
```

**State Values:**
- `1` = Draft
- `2` = Ready
- `3` = Work In Progress
- `4` = Ready For Testing
- `5` = Testing
- `6` = Complete
- `7` = Cancel

**Priority Values:**
- `1` = Critical
- `2` = High
- `3` = Moderate
- `4` = Low
- `5` = Planning

---

## Epics

### Get Epics (Filtered)

```python
mcp__mcprelay__itbm_get_epics(
    # Exact match
    epic_number=None,           # EPICxxxxxxx format
    state=None,                 # Single value or list
    level=None,                 # Epic level

    # Contains filters
    title=None,                 # Epic title/short_description
    product_name=None,          # Product name
    assignment_group=None,      # Single value or list
    theme=None,                 # Theme
    parent_epic=None,           # Parent epic

    # Completion percentage
    percent_complete_min=None,  # 0-100
    percent_complete_max=None,  # 0-100

    # Date filters (ISO format)
    start_date_after=None,
    start_date_before=None,
    end_date_after=None,
    end_date_before=None,
    time_zone="Europe/Paris",

    # Pagination
    limit=50  # Max: 100, default: 50
)
```

**Examples:**
```python
# Get active epics
itbm_get_epics(state="In Progress", limit=50)

# Get epics by product
itbm_get_epics(product_name="BTDP", limit=50)

# Get epics by completion percentage
itbm_get_epics(
    percent_complete_min=50,
    percent_complete_max=90
)

# Get epics starting in date range
itbm_get_epics(
    start_date_after="2025-01-01",
    start_date_before="2025-03-31"
)

# Get epics by assignment group
itbm_get_epics(
    assignment_group=["IT-GLOBAL-GCP-BTDP-DATA", "IT-GLOBAL-GCP-BTDP-PLATFORM"],
    state="In Progress"
)

# Search by title
itbm_get_epics(title="data platform", limit=20)

# Get top-level epics
itbm_get_epics(level="1", limit=50)
```

### Get Single Epic

```python
mcp__mcprelay__itbm_get_epic(
    sys_id_or_number="<epic_number>"  # EPICxxxxxxx or sys_id
)
```

### Search Epic Stories (SDDS)

```python
mcp__mcprelay__itbm_search_epic_story(
    # Partial match filters
    number=None,                # Epic number
    short_description=None,     # Epic name/description
    product=None,               # Product
    assignment_group=None,      # Assignment group
    theme=None,                 # Theme
    business_process=None,      # Business process

    # Exact match
    state=None,                 # Epic state
    priority=None,              # Priority
    rag_status=None,            # RAG status (Red/Amber/Green)
    active=None,                # "true"/"false"

    # Pagination
    limit=50  # Max: 100, default: 50
)
```

---

## Sprints

### Get Sprints (Filtered)

```python
mcp__mcprelay__itbm_get_sprints(
    # Exact match
    sprint_number=None,         # Sprint number
    state=None,                 # Single value or list

    # Contains filters
    title=None,                 # Sprint title/short_description
    assignment_group=None,      # Single value or list
    release=None,               # Release

    # Points range
    story_points_min=None,
    story_points_max=None,
    team_points_min=None,
    team_points_max=None,
    actual_points_min=None,
    actual_points_max=None,

    # Date filters (ISO format)
    start_date_after=None,
    start_date_before=None,
    end_date_after=None,
    end_date_before=None,
    opened_after=None,
    opened_before=None,
    time_zone="Europe/Paris",

    # Pagination
    limit=50  # Max: 100, default: 50
)
```

**Examples:**
```python
# Get active sprints
itbm_get_sprints(state="Active", limit=50)

# Get sprints by assignment group
itbm_get_sprints(
    assignment_group="IT-GLOBAL-GCP-BTDP-DATA",
    state=["Active", "Planned"]
)

# Get sprints in date range
itbm_get_sprints(
    start_date_after="2025-01-01",
    end_date_before="2025-12-31"
)

# Get sprints by story points
itbm_get_sprints(
    story_points_min=50,
    story_points_max=100
)

# Search by title
itbm_get_sprints(title="2025", limit=50)
```

### Get Single Sprint

```python
mcp__mcprelay__itbm_get_sprint(
    sys_id_or_number="<sprint_number>"  # Sprint number or sys_id
)
```

---

## Enhancements

### Search Enhancements

```python
mcp__mcprelay__itbm_search_enhancement(
    # Partial match filters
    number=None,                # Enhancement number
    short_description=None,     # Description
    requester=None,             # Requester
    country=None,               # Country
    service=None,               # Application service
    product=None,               # Product
    release=None,               # Release
    assignment_group=None,      # Assignment group
    assigned_to=None,           # Assigned to
    epic=None,                  # Epic
    theme=None,                 # Theme

    # Exact match
    enhancement_type=None,      # Enhancement type
    priority=None,              # Priority
    state=None,                 # State
    substate=None,              # Substate
    committee_decision=None,    # Committee decision
    rag_status=None,            # RAG status
    active=None,                # "true"/"false"

    # Pagination
    limit=50  # Max: 100, default: 50
)
```

**Examples:**
```python
# Get active enhancements
itbm_search_enhancement(active="true", state="In Progress")

# Get enhancements by service
itbm_search_enhancement(
    service="BTDP Data Platform",
    state=["New", "In Progress"]
)

# Get enhancements by priority
itbm_search_enhancement(priority="Critical", limit=50)

# Get enhancements by assignment group
itbm_search_enhancement(
    assignment_group="IT-GLOBAL-GCP-BTDP-DATA",
    state="In Progress"
)

# Search by description
itbm_search_enhancement(short_description="data migration")
```

---

## Assignment Groups

### Search Assignment Groups

```python
mcp__mcprelay__itbm_search_assignment_group(
    # Partial match
    name=None,                  # Group name
    manager=None,               # Group manager
    it_organization=None,       # IT organization
    location=None,              # Location
    email=None,                 # Group email
    parent=None,                # Parent group

    # Exact match
    group_type=None,            # Group type
    category=None,              # Category
    active=None,                # "true"/"false"

    # Pagination
    limit=50  # Max: 100, default: 50
)
```

**Examples:**
```python
# Find BTDP groups
itbm_search_assignment_group(name="BTDP", active="true")

# Find groups by manager
itbm_search_assignment_group(manager="sebastien.morand")

# Find groups by IT org
itbm_search_assignment_group(it_organization="Data & AI")
```

---

## SQL Fallback

### Story Table

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.story_v1`

```sql
SELECT
    number,
    short_description,
    priority,
    state,
    story_points,
    assignment_group,
    product,
    epic,
    sprint,
    sys_created_on,
    sys_updated_on
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.story_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
  AND state IN ('2', '3', '4')  -- Ready, WIP, Ready for Testing
ORDER BY sys_updated_on DESC
LIMIT 100
```

### Epic Table

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.epic_v1`

```sql
SELECT
    number,
    short_description,
    state,
    product,
    assignment_group,
    percent_complete,
    planned_start_date,
    planned_end_date
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.epic_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
ORDER BY sys_updated_on DESC
LIMIT 50
```

### Enhancement Table

**Table:** `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_055_itbm_eu_pd.enhancement_v1`

```sql
SELECT
    number,
    short_description,
    state,
    priority,
    service,
    assignment_group,
    sys_created_on
FROM `itg-btdppublished-gbl-ww-pd.btdp_ds_c1_055_itbm_eu_pd.enhancement_v1`
WHERE REGEXP_CONTAINS(LOWER(short_description), r'<pattern>')
  AND state != 'Closed'
ORDER BY priority ASC, sys_updated_on DESC
LIMIT 50
```

---

## Best Practices

1. **Use specific filters** to reduce result size (limit=50 recommended)
2. **Filter by state** to exclude closed/cancelled items
3. **Use date ranges** for recent activity (created_after, updated_after)
4. **Filter by assignment group** for team-specific queries
5. **Get single item** when you have the number (STRY/EPIC/sprint number)
6. **SQL fallback** for complex queries or regexp on descriptions
7. **Use lists** for multiple states/priorities/groups
