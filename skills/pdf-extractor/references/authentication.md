# Authentication & Setup

Complete guide to GCP authentication, Vertex AI setup, and troubleshooting.

## Overview

The PDF extractor uses Claude via Google Cloud Vertex AI, which requires:
1. Google Cloud SDK (gcloud) installed
2. Authenticated with your Google Cloud account
3. GCP project with Vertex AI API enabled
4. Proper IAM permissions

## Initial Setup

### Step 1: Install Google Cloud SDK

#### macOS
```bash
# Using Homebrew
brew install google-cloud-sdk

# Or download installer from:
# https://cloud.google.com/sdk/docs/install
```

#### Linux
```bash
# Debian/Ubuntu
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk

# Or use snap
sudo snap install google-cloud-sdk --classic
```

#### Windows
Download and run the installer from:
https://cloud.google.com/sdk/docs/install

#### Verify Installation
```bash
gcloud --version

# Expected output:
# Google Cloud SDK 450.0.0
# bq 2.0.97
# core 2023.10.11
# gcloud-crc32c 1.0.0
# gsutil 5.26
```

### Step 2: Authenticate with Google Cloud

#### Application Default Credentials (Recommended)

```bash
# Login and create application default credentials
gcloud auth application-default login
```

**What this does:**
- Opens browser for Google account login
- Creates credentials file at: `~/.config/gcloud/application_default_credentials.json`
- Used by Anthropic SDK for Vertex AI authentication
- Works for local development

**When to use:**
- Local development (your machine)
- Personal projects
- Testing and prototyping

#### Service Account (Production)

For production or automated environments:

```bash
# Create service account
gcloud iam service-accounts create pdf-extractor-sa \
    --display-name="PDF Extractor Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:pdf-extractor-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create ~/pdf-extractor-key.json \
    --iam-account=pdf-extractor-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/pdf-extractor-key.json"
```

**When to use:**
- Production environments
- Automated workflows
- CI/CD pipelines
- Server deployments

### Step 3: Set Default Project

```bash
# Set your default project
gcloud config set project YOUR_PROJECT_ID

# Verify configuration
gcloud config list

# Expected output:
# [core]
# account = your.email@domain.com
# project = your-project-id
```

### Step 4: Enable Vertex AI API

```bash
# Enable the Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Verify API is enabled
gcloud services list --enabled | grep aiplatform

# Expected output:
# aiplatform.googleapis.com
```

### Step 5: Verify Authentication

```bash
# Test authentication works
gcloud auth application-default print-access-token

# Should output a long access token (starting with ya29.*)
```

If this works, you're ready to use the PDF extractor!

## Configuration Options

### Option 1: Use gcloud Configuration (Recommended)

Set defaults using gcloud:

```bash
# Set project
gcloud config set project your-project-id

# Check configuration
gcloud config list
```

**Pros:**
- Centralized configuration
- Works across all gcloud tools
- Easy to switch between projects

**Cons:**
- Affects all gcloud operations

### Option 2: Environment Variables

Set environment variables:

```bash
# In ~/.bashrc, ~/.zshrc, or ~/.profile
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="europe-west1"

# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc
```

**Pros:**
- Project-specific configuration
- Doesn't affect gcloud defaults
- Easy to override

**Cons:**
- Needs to be set in each shell session
- Must remember to export

### Option 3: Command-Line Arguments

Override per-execution:

```bash
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor document.pdf \
    --project my-project \
    --region us-central1
```

**Pros:**
- Most flexible
- Override for specific runs
- No persistent configuration needed

**Cons:**
- Must specify each time
- Longer commands

### Priority Order

The script uses this priority (highest to lowest):

1. **Command-line arguments** (`--project`, `--region`)
2. **Environment variables** (`GCP_PROJECT_ID`, `GCP_REGION`)
3. **gcloud configuration** (`gcloud config get-value project`)
4. **Default region** (europe-west1)

## Required IAM Permissions

Your account or service account needs:

### Minimum Required Role

```bash
roles/aiplatform.user
```

**Includes permissions:**
- `aiplatform.endpoints.predict`
- `aiplatform.endpoints.get`
- Access to Vertex AI models

### Grant Permission

```bash
# For user account
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="user:your.email@domain.com" \
    --role="roles/aiplatform.user"

# For service account
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
    --role="roles/aiplatform.user"
```

### Check Current Permissions

```bash
# List your project permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:user:your.email@domain.com"
```

## Region Selection

### Available Regions for Claude on Vertex AI

Common regions where Claude is available:

| Region | Location | Best For |
|--------|----------|----------|
| `europe-west1` | Belgium | Europe (default) |
| `us-central1` | Iowa, USA | US Central |
| `us-east1` | South Carolina, USA | US East |
| `us-east4` | Virginia, USA | US East |
| `us-west1` | Oregon, USA | US West |
| `asia-southeast1` | Singapore | Asia Pacific |

### Set Default Region

```bash
# Via environment variable
export GCP_REGION="europe-west1"

# Via command-line argument
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor doc.pdf --region europe-west1
```

### Choose Region Based On

1. **Geographic proximity** - Closer = faster response
2. **Data residency requirements** - Keep data in specific regions
3. **Cost** - Pricing may vary by region
4. **Availability** - Not all regions support all models

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Cause:** No authentication configured

**Solution:**
```bash
# Run authentication
gcloud auth application-default login

# Verify it worked
gcloud auth application-default print-access-token
```

### Error: "Project ID not found"

**Cause:** No project configured

**Solution:**
```bash
# Set default project
gcloud config set project YOUR_PROJECT_ID

# Or use environment variable
export GCP_PROJECT_ID="your-project-id"

# Or use command-line argument
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor doc.pdf --project your-project-id
```

### Error: "Vertex AI API has not been used in project"

**Cause:** Vertex AI API not enabled

**Solution:**
```bash
# Enable the API
gcloud services enable aiplatform.googleapis.com

# Wait a minute for propagation
sleep 60

# Verify it's enabled
gcloud services list --enabled | grep aiplatform
```

### Error: "Permission denied" or "403 Forbidden"

**Cause:** Insufficient IAM permissions

**Solution:**
```bash
# Check current permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:user:$(gcloud config get-value account)"

# Grant required permission
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/aiplatform.user"
```

### Error: "The access token has expired"

**Cause:** Authentication credentials expired

**Solution:**
```bash
# Re-authenticate
gcloud auth application-default login

# Verify new token
gcloud auth application-default print-access-token
```

### Error: "Model not available in region"

**Cause:** Claude model not available in specified region

**Solution:**
```bash
# Use a supported region (europe-west1, us-central1, etc.)
~/.claude/skills/pdf-extractor/scripts/run.sh pdf_extractor doc.pdf --region europe-west1

# Or set default
export GCP_REGION="europe-west1"
```

### Error: "Network connection failed"

**Cause:** Network connectivity issues or firewall

**Solution:**
```bash
# Test connectivity to Google APIs
curl -I https://aiplatform.googleapis.com

# Check if behind corporate proxy
echo $HTTP_PROXY
echo $HTTPS_PROXY

# If using proxy, configure gcloud
gcloud config set proxy/type http
gcloud config set proxy/address PROXY_ADDRESS
gcloud config set proxy/port PROXY_PORT
```

### Error: "Quota exceeded"

**Cause:** API quota limits reached

**Solution:**
1. Check quota usage in GCP Console: https://console.cloud.google.com/iam-admin/quotas
2. Request quota increase if needed
3. Wait for quota to reset (usually hourly or daily)
4. Use different project if available

### Error: "Service account key file not found"

**Cause:** `GOOGLE_APPLICATION_CREDENTIALS` points to non-existent file

**Solution:**
```bash
# Check if file exists
ls -lh $GOOGLE_APPLICATION_CREDENTIALS

# If missing, re-download or use application default credentials
unset GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```

## Verification Checklist

Before using the PDF extractor, verify:

- [ ] gcloud SDK installed (`gcloud --version`)
- [ ] Authenticated (`gcloud auth application-default print-access-token`)
- [ ] Project set (`gcloud config get-value project`)
- [ ] Vertex AI API enabled (`gcloud services list --enabled | grep aiplatform`)
- [ ] Permissions granted (`gcloud projects get-iam-policy PROJECT_ID`)
- [ ] Can access token (`gcloud auth application-default print-access-token`)

Quick verification script:
```bash
#!/bin/bash

echo "Checking gcloud installation..."
gcloud --version || { echo "FAIL: gcloud not installed"; exit 1; }

echo "Checking authentication..."
gcloud auth application-default print-access-token > /dev/null || { echo "FAIL: Not authenticated"; exit 1; }

echo "Checking project..."
PROJECT=$(gcloud config get-value project)
[ -n "$PROJECT" ] || { echo "FAIL: No project set"; exit 1; }
echo "Project: $PROJECT"

echo "Checking Vertex AI API..."
gcloud services list --enabled | grep aiplatform || { echo "FAIL: Vertex AI not enabled"; exit 1; }

echo "✅ All checks passed!"
```

## Advanced Configuration

### Multiple Projects

Switch between projects:

```bash
# List configurations
gcloud config configurations list

# Create new configuration
gcloud config configurations create work
gcloud config configurations create personal

# Activate configuration
gcloud config configurations activate work

# Set project for configuration
gcloud config set project work-project-id

# Switch to different configuration
gcloud config configurations activate personal
```

### Custom Service Account for PDF Extractor

Create dedicated service account:

```bash
# Create service account
gcloud iam service-accounts create pdf-extractor \
    --display-name="PDF Extractor" \
    --description="Service account for PDF extraction with Vertex AI"

# Grant Vertex AI user role
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:pdf-extractor@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create key
gcloud iam service-accounts keys create ~/pdf-extractor-key.json \
    --iam-account=pdf-extractor@PROJECT_ID.iam.gserviceaccount.com

# Use in script
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/pdf-extractor-key.json"
```

### Audit Logging

Enable audit logs for Vertex AI:

```bash
# Create audit config
cat > audit-config.yaml <<EOF
auditConfigs:
- auditLogConfigs:
  - logType: ADMIN_READ
  - logType: DATA_READ
  - logType: DATA_WRITE
  service: aiplatform.googleapis.com
EOF

# Apply configuration
gcloud projects set-iam-policy PROJECT_ID audit-config.yaml
```

View audit logs:
```bash
gcloud logging read "resource.type=aiplatform.googleapis.com" \
    --limit 50 \
    --format json
```

### Cost Monitoring

Set up budget alerts:

```bash
# Create budget (via Console)
# Go to: https://console.cloud.google.com/billing/budgets

# Or monitor costs via CLI
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID
```

Monitor Vertex AI usage:
```bash
# View metrics
gcloud monitoring time-series list \
    --filter='metric.type="aiplatform.googleapis.com/prediction/request_count"' \
    --project=PROJECT_ID
```

## Security Best Practices

1. **Use application default credentials locally**
   ```bash
   gcloud auth application-default login
   ```

2. **Use service accounts in production**
   - Create dedicated service accounts
   - Grant minimum required permissions
   - Rotate keys regularly

3. **Never commit credentials**
   - Add `*.json` to `.gitignore`
   - Use environment variables
   - Use secret managers in production

4. **Limit API access**
   - Use VPC Service Controls if needed
   - Restrict by IP if possible
   - Monitor usage regularly

5. **Enable audit logging**
   - Track API calls
   - Monitor for unusual activity
   - Review logs regularly

## Getting Help

### Google Cloud Documentation
- Vertex AI docs: https://cloud.google.com/vertex-ai/docs
- Authentication guide: https://cloud.google.com/docs/authentication
- IAM roles: https://cloud.google.com/iam/docs/understanding-roles

### Common Resources
- gcloud CLI reference: https://cloud.google.com/sdk/gcloud/reference
- Anthropic Vertex AI docs: https://docs.anthropic.com/en/api/claude-on-vertex-ai
- Troubleshooting guide: https://cloud.google.com/vertex-ai/docs/troubleshooting

### Support Channels
- Google Cloud Support: https://cloud.google.com/support
- Stack Overflow: Tag with `google-cloud-platform` and `vertex-ai`
- Anthropic Discord: https://www.anthropic.com/discord
