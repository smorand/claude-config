# Release Implementation

## Purpose
Create and manage release branches with proper git workflow from develop to master. Handle both complete releases (all user stories) and selective releases (cherry-picked user stories) with comprehensive release documentation.

## Prerequisites
- Clean working directory on develop branch
- Release number (RLSExxxxxxx) provided (MANDATORY)
- Access to git repository with develop and master branches
- Understanding of release workflow and merge strategies

## Protocol

### Input Arguments
```
\$ARGUMENTS: Release number (RLSExxxxxxx) and optional list of user stories for cherry-picking
```

**Expected Input Format:**
- **Mandatory:** Release number in format `RLSExxxxxxx` (7 digits)
- **Optional:** Space-separated list of user story numbers in format `STRYxxxxxxx`

**Examples:**
- `RLSE0001234` (complete release with all stories)
- `RLSE0001235 STRY0001001 STRY0001002 STRY0001003` (selective release)

**Release Number Validation:**
- MUST be provided in format RLSExxxxxxx (where x = digits)
- If not provided or invalid format, STOP execution immediately
- Release number will be used for branch naming and commit messages

**User Stories (Optional):**
- If no list provided: Include ALL user stories from develop branch
- If list provided: Cherry-pick only specified user stories (STRYxxxxxxx format)

You must follow this protocol completely. Create a Todo list according to these steps:

1. **Validate Release Number** - Ensure release number is provided in correct RLSExxxxxxx format (STOP if invalid)
2. **Prepare Release Environment** - Ensure clean working directory and up-to-date branches
3. **Create Release Branch** - Create release branch from develop using release number
4. **Handle User Stories** - Either include all changes or cherry-pick specific user stories
5. **Generate Release Summary** - Create comprehensive summary of included user stories
6. **Create Release Pull Request** - Create PR from develop to master (NO SQUASH)
7. **Document Release Content** - Provide final summary of release contents

## Success Criteria
- [ ] Release number validated in RLSExxxxxxx format
- [ ] Release branch created from develop branch
- [ ] Proper git workflow followed (develop → master, no squash)
- [ ] User stories correctly included (all or cherry-picked)
- [ ] Release summary generated with story descriptions
- [ ] Pull request created with proper merge strategy
- [ ] Release documentation complete

## Release Workflow Steps

### 1. Release Number Validation
**MANDATORY:** Release number must be provided in format `RLSExxxxxxx`

```bash
# Validate release number format
if [[ ! "$RELEASE_NUMBER" =~ ^RLSE[0-9]{7}$ ]]; then
    echo "❌ ERROR: Invalid release number format. Expected: RLSExxxxxxx"
    exit 1
fi
```

### 2. Environment Preparation
```bash
# Ensure clean working directory
git status --porcelain
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Working directory not clean. Commit or stash changes first."
    exit 1
fi

# Update develop and master branches
git checkout develop && git pull origin develop
git checkout master && git pull origin master
git checkout develop  # Return to develop for release branch creation
```

### 3. Release Branch Creation
```bash
# Create release branch from develop
git checkout -b release/$RELEASE_NUMBER

echo "✅ Created release branch: release/$RELEASE_NUMBER"
```

### 4. User Story Management

#### Default: Include All User Stories
```bash
# When no specific stories provided, include all changes from develop
echo "📋 Including ALL user stories from develop branch"
# Branch contains all changes from develop - no additional action needed
```

#### Selective: Cherry-Pick Specific User Stories
```bash
# When specific stories provided, cherry-pick only those commits
if [ ! -z "$USER_STORIES" ]; then
    echo "🔍 Cherry-picking specific user stories: $USER_STORIES"
    
    for story in $USER_STORIES; do
        echo "🍒 Processing story: $story"
        
        # Find commits for this user story
        commits=$(git log develop --grep="$story" --pretty=format:"%H" --reverse)
        
        if [ -z "$commits" ]; then
            echo "⚠️  No commits found for story: $story"
            continue
        fi
        
        # Cherry-pick commits for this story
        for commit in $commits; do
            git cherry-pick $commit
            if [ $? -ne 0 ]; then
                echo "❌ Cherry-pick failed for commit: $commit"
                echo "🔧 Resolve conflicts manually and continue"
                exit 1
            fi
        done
        
        echo "✅ Successfully cherry-picked story: $story"
    done
fi
```

### 5. Release Summary Generation
```bash
# Generate comprehensive release summary
echo "📊 Generating release summary for $RELEASE_NUMBER"

# Create release summary file
cat > release_summary_$RELEASE_NUMBER.md << EOF
# Release Summary: $RELEASE_NUMBER

## Release Information
- **Release Number:** $RELEASE_NUMBER
- **Release Date:** $(date '+%Y-%m-%d %H:%M:%S')
- **Release Type:** $([ -z "$USER_STORIES" ] && echo "Complete Release (All Stories)" || echo "Selective Release (Cherry-picked)")
- **Source Branch:** develop
- **Target Branch:** master

## Included User Stories

EOF

# Add user story details to summary
if [ -z "$USER_STORIES" ]; then
    # All stories from develop
    echo "### All User Stories from Develop Branch" >> release_summary_$RELEASE_NUMBER.md
    git log master..develop --grep="STRY" --pretty=format:"- **%s**" --reverse >> release_summary_$RELEASE_NUMBER.md
else
    # Specific cherry-picked stories
    echo "### Cherry-picked User Stories" >> release_summary_$RELEASE_NUMBER.md
    for story in $USER_STORIES; do
        echo "- **$story:**" >> release_summary_$RELEASE_NUMBER.md
        # Get story description from commit messages
        git log develop --grep="$story" --pretty=format:"  - %s" --reverse >> release_summary_$RELEASE_NUMBER.md
    done
fi

cat >> release_summary_$RELEASE_NUMBER.md << EOF

## Release Notes
$(git log --oneline master..HEAD --reverse)

## Deployment Information
- **Merge Strategy:** Merge commit (NO SQUASH)
- **Approval Required:** Yes
- **Testing Required:** Yes

---
Generated on $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo "✅ Release summary generated: release_summary_$RELEASE_NUMBER.md"
```

### 6. Release Commit and Push
```bash
# Commit release preparation
git add .
git commit -S -m "[$RELEASE_NUMBER](release) Prepare release $RELEASE_NUMBER"

# Push release branch
git push origin release/$RELEASE_NUMBER

echo "✅ Release branch pushed: release/$RELEASE_NUMBER"
```

### 7. Pull Request Creation
```bash
# Create pull request using GitHub CLI
gh pr create \
    --title "Release $RELEASE_NUMBER" \
    --body "$(cat <<EOF
# Release $RELEASE_NUMBER

## ⚠️ IMPORTANT: This is a RELEASE PR - DO NOT SQUASH MERGE

**Merge Strategy:** Use **Merge Commit** to preserve full development history

## Release Summary
$(cat release_summary_$RELEASE_NUMBER.md)

## Pre-merge Checklist
- [ ] All required approvals obtained
- [ ] Testing completed successfully
- [ ] Release notes reviewed
- [ ] Merge strategy confirmed (NO SQUASH)

---
**Target:** master ← develop  
**Type:** Release  
**Merge:** Merge commit (preserve history)
EOF
)" \
    --base master \
    --head release/$RELEASE_NUMBER

echo "✅ Release PR created for $RELEASE_NUMBER"
```

## Environment Detection

This command works with both BTDP Framework and Personal Projects:

**BTDP Framework Projects:**
- Uses enterprise git workflow
- Integrates with BTDP module structure
- Follows enterprise release standards

**Personal Projects:**
- Uses standard git workflow
- Adapts to personal project structure
- Maintains release documentation standards

## Error Handling

### Common Release Issues
| Issue | Cause | Solution | Alternative |
|-------|-------|----------|-------------|
| **Invalid release number** | Wrong format provided | Provide RLSExxxxxxx format | Check existing releases |
| **Dirty working directory** | Uncommitted changes | Commit or stash changes | Use `git status` to check |
| **Cherry-pick conflicts** | Code conflicts during cherry-pick | Resolve conflicts manually | Use `git cherry-pick --continue` |
| **Missing user story** | Story not found in develop | Verify story number format | Check `git log --grep` |
| **Branch already exists** | Release branch exists | Delete old branch or use new number | `git branch -D release/RLSExxxxxxx` |

### Recovery Procedures
| Stage | Recovery Action | Command | Notes |
|-------|----------------|---------|-------|
| **Validation Failed** | Fix release number format | Restart with correct format | Must be RLSExxxxxxx |
| **Cherry-pick Failed** | Resolve conflicts | `git cherry-pick --continue` | Manual resolution required |
| **Push Failed** | Check permissions | Verify git credentials | May need repository access |
| **PR Creation Failed** | Check GitHub CLI | `gh auth status` | Verify authentication |

## Task Description
**\$ARGUMENTS** will be replaced with the actual release information you provide according to the input format above.

## Example Usage

### Complete Release (All Stories)
```
\$ARGUMENTS: RLSE0001234

Creates release branch with ALL user stories from develop to master
```

### Selective Release (Cherry-picked Stories)
```
\$ARGUMENTS: RLSE0001235 STRY0001001 STRY0001002 STRY0001003

Creates release branch with only specified user stories cherry-picked from develop
```

### Release with Specific Features
```
\$ARGUMENTS: RLSE0001236 STRY0002001 STRY0002002

Cherry-picks only the authentication and payment features for this release
```

**How to Use:**
Replace `\$ARGUMENTS` with your specific release number and optional story list when invoking this command. The AI will process your input according to the validation rules and workflow defined above.

## Release Summary Format

The command generates a comprehensive release summary including:

1. **Release Metadata** - Number, date, type, branches
2. **User Story List** - All included stories with descriptions
3. **Release Notes** - Commit history and changes
4. **Deployment Info** - Merge strategy and approval requirements

This ensures complete traceability and documentation for each release.