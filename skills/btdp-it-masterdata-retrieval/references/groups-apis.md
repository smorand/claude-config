# Google Groups & APIs

## Google Groups

### Search Groups (Regexp)

**Best for:** Exact pattern matching on group names/emails

```python
mcp__mcprelay__groups_search_groups(
    search_term="<regexp_pattern>"  # Regexp pattern for names and emails
)
```

**Examples:**
```python
# Find all BTDP groups
groups_search_groups(search_term=".*BTDP.*")

# Find specific zone groups
groups_search_groups(search_term="IT-GLOBAL-GCP-.*")

# Find data-related groups
groups_search_groups(search_term=".*DATA.*")

# Find development environment groups
groups_search_groups(search_term=".*-DV@loreal.com$")
```

**Pattern Tips:**
- Use `.*` for wildcard matching
- Use `^` and `$` for start/end anchors
- Use `(option1|option2)` for alternatives
- Case-sensitive by default

### Search Similar Groups (Semantic)

**Best for:** Natural language search using embeddings

```python
mcp__mcprelay__groups_search_similar_groups(
    search_term="<natural_language>",
    limit=10  # Max results (default: 10)
)
```

**Examples:**
```python
# Find groups by description
groups_search_similar_groups("data platform team", limit=10)

# Find groups by purpose
groups_search_similar_groups("development access", limit=5)

# Find groups by domain
groups_search_similar_groups("consumer data domain", limit=10)
```

**Returns:** List with `group_email` and `similarity_score`

### Get Group Details

```python
mcp__mcprelay__groups_get_group(
    group_email="<group_email>"  # e.g., IT-GLOBAL-GCP-BTDP_DATASRV-DV@loreal.com
)
```

**Example:**
```python
groups_get_group(group_email="IT-GLOBAL-GCP-BTDP_DATASRV_USECASE-DV@loreal.com")
```

**Returns:** Name, description, owners, email, status, etc.

### Get Group Members

```python
mcp__mcprelay__groups_get_members(
    group_name="<group_email>"  # Always email format, @loreal.com
)
```

**Example:**
```python
groups_get_members(group_name="IT-GLOBAL-GCP-BTDP-DATA@loreal.com")
```

**Returns:** List of member emails (users and service accounts)

### Add Members

```python
mcp__mcprelay__groups_add_members(
    group_name="<group_email>",
    members=["email1@loreal.com", "email2@loreal.com"]  # Users or service accounts
)
```

**Example:**
```python
groups_add_members(
    group_name="IT-GLOBAL-GCP-BTDP-DATA@loreal.com",
    members=["sebastien.morand@loreal.com"]
)
```

### Remove Members

```python
mcp__mcprelay__groups_remove_members(
    group_name="<group_email>",
    members=["email1@loreal.com", "email2@loreal.com"]
)
```

**Example:**
```python
groups_remove_members(
    group_name="IT-GLOBAL-GCP-BTDP-DATA@loreal.com",
    members=["user.to.remove@loreal.com"]
)
```

### Get Group Owners

```python
mcp__mcprelay__groups_get_group_owners(
    group_email="<group_email>"
)
```

**Example:**
```python
groups_get_group_owners(group_email="IT-GLOBAL-GCP-BTDP-DATA@loreal.com")
```

### Add Group Owners

```python
mcp__mcprelay__groups_add_group_owners(
    group_email="<group_email>",
    owners=["email1@loreal.com", "email2@loreal.com"]
)
```

**Example:**
```python
groups_add_group_owners(
    group_email="IT-GLOBAL-GCP-BTDP-DATA@loreal.com",
    owners=["new.owner@loreal.com"]
)
```

### Remove Group Owners

```python
mcp__mcprelay__groups_remove_group_owners(
    group_email="<group_email>",
    owners=["email1@loreal.com"]
)
```

### Check User Membership

```python
mcp__mcprelay__groups_is_user_member(
    group_email="<group_email>",
    user_email="<user_email>"
)
```

**Example:**
```python
groups_is_user_member(
    group_email="IT-GLOBAL-GCP-BTDP-DATA@loreal.com",
    user_email="sebastien.morand@loreal.com"
)
```

**Returns:** Boolean

### Create Group

```python
mcp__mcprelay__groups_create_group(
    name="<group_name>",        # Without @loreal.com suffix
    description="<description>",
    owners=["email1@loreal.com"],
    members=["email1@loreal.com", "email2@loreal.com"],
    zone="<IT_ZONE>"           # Required: see zones below
)
```

**Available Zones:**
- `AMER`, `APAC`, `APMENA`, `BTA`, `CDO`, `CORP`, `DATA`, `DGRH`
- `EMEA`, `EU`, `INFRA`, `IT-GLOBAL`, `NEO`, `OO`, `OPSFIN`
- `RNI`, `SEC`, `TECH`, `TR`, `TREAS`

**Final Format:** `{zone}-GCP-{name}@loreal.com`

**Example:**
```python
groups_create_group(
    name="BTDP_MYTEAM-DV",
    description="BTDP My Team Development Access",
    owners=["sebastien.morand@loreal.com"],
    members=["user1@loreal.com", "user2@loreal.com"],
    zone="IT-GLOBAL"
)
# Creates: IT-GLOBAL-GCP-BTDP_MYTEAM-DV@loreal.com
```

### Delete Group

```python
mcp__mcprelay__groups_delete_group(
    group_email="<group_email>"
)
```

**Example:**
```python
groups_delete_group(group_email="IT-GLOBAL-GCP-OLD_GROUP@loreal.com")
```

---

## APIs (L'Oréal API Portal)

### List All APIs

```python
mcp__mcprelay__apis_list_apis()
```

**Returns:** List of all APIs with metadata

### Get API Information

```python
mcp__mcprelay__apis_get_api_information(
    api_name="<api_name>"
)
```

**Example:**
```python
apis_get_api_information(api_name="btdp-notifications-api")
```

**Returns:** API information and metadata

### Get API Specification

```python
mcp__mcprelay__apis_get_api_spec(
    api_name="<api_name>"
)
```

**Example:**
```python
apis_get_api_spec(api_name="btdp-notifications-api")
```

**Returns:** Swagger/OpenAPI specification (JSON format)

### Search APIs (Regexp)

```python
mcp__mcprelay__apis_search_api(
    regexp_pattern="<pattern>"  # Regexp pattern on API names
)
```

**Examples:**
```python
# Find BTDP APIs
apis_search_api(regexp_pattern=".*btdp.*")

# Find notification APIs
apis_search_api(regexp_pattern=".*notification.*")

# Find data APIs
apis_search_api(regexp_pattern=".*data.*")
```

**Returns:** List of matching API information

---

## Group Naming Convention

**Format:** `{ZONE}-GCP-{NAME}@loreal.com`

**Examples:**
- `IT-GLOBAL-GCP-BTDP_DATASRV_USECASE-DV@loreal.com`
- `IT-GLOBAL-GCP-BTDP-DATA@loreal.com`
- `DATA-GCP-CONSUMER_DOMAIN-PD@loreal.com`

**Environment Suffixes:**
- `-DV` - Development
- `-QA` - Quality Assurance
- `-NP` - Non-Production
- `-PD` - Production

**Naming Guidelines:**
- Use underscores `_` for multi-word names
- Include environment suffix for env-specific groups
- Use descriptive names indicating purpose
- Follow zone prefix conventions

---

## Best Practices

### Groups
1. **Search with regexp** for exact pattern matching
2. **Search similar** for natural language discovery
3. **Check membership** before adding members
4. **Get group details** to verify before modifications
5. **Use IT-GLOBAL zone** for cross-zone groups
6. **Include environment suffix** for env-specific access

### APIs
1. **List all** for discovery
2. **Search with regexp** for filtered results
3. **Get spec** for detailed API schema and endpoints
4. **Get information** for API metadata and documentation links

### Common Patterns
```python
# Find all production groups for a service
groups_search_groups(search_term=".*BTDP.*-PD@loreal.com$")

# Find all development groups
groups_search_groups(search_term=".*-DV@loreal.com$")

# Find groups in specific zone
groups_search_groups(search_term="^IT-GLOBAL-GCP-.*")

# Find data-related APIs
apis_search_api(regexp_pattern=".*data.*")
```
