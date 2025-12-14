# Looker Deployment Protocol

## Purpose
Deploy Looker code changes through proper git workflow including commit squashing, branch merging, and environment-specific deployment using Looker deployment tools.

## Prerequisites
- Working on feature branch (not develop/main)
- Completed Looker code implementation
- Access to deployment tools for Looker projects
- Understanding of target environment (dev/uat/production)

## Workflow Steps

You must follow this protocol completely. Create a Todo list according to these steps:

1. Ensure you are on a dedicated branch for the feature and that you are not on develop.
2. Squash the commit on the current branch and push force with lease.
3. Merge the current branch on the appropriate branch (develop to make the code available in dev environment, uat to make the code available in uat environment and production to make the code available in production), then push the branch.
4. Delete the feature branch and push the deletion.
5. Run the appropriate tools with the commit sha (check git history), proper environment and the project name (found in the manifest file). If no tools are available to deploy looker, just stop and provide the developer with the information how to deploy.

## Success Criteria
- [ ] Feature branch commits squashed properly
- [ ] Code merged to appropriate target branch (develop/uat/production)
- [ ] Feature branch deleted and deletion pushed
- [ ] Deployment initiated using proper tools and commit SHA
- [ ] Deployment verified in target environment
- [ ] Developer provided with deployment information if tools unavailable

## Environment Detection
This command is specifically for Looker deployment and uses:

**Looker Deployment Environment:**
- **Detection**: Look for `manifest.lkml`, Looker project configuration
- **Branch Mapping**: 
  - `develop` branch → dev environment
  - `uat` branch → uat environment  
  - `production` branch → production environment
- **Deployment Tools**: Uses Looker deployment automation with commit SHA
- **Git Workflow**: Squash commits, merge to target branch, clean up feature branch
- **Validation**: Verify deployment success in target Looker environment

## Task Description
$ARGUMENTS

## Example Usage
```
$ARGUMENTS: Deploy the new sales dashboard features to production environment. Squash commits from the feature branch, merge to production branch, and deploy using the Looker deployment tools with proper commit SHA and project configuration.
```

