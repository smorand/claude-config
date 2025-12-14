# BTDP Framework End-to-End Tests Implementation

## Purpose
Implement comprehensive end-to-end tests for BTDP Framework projects following proven enterprise patterns. Use this command for testing complete data pipelines with distributed GCP architecture (SRC → DMN → SDDS).

## Prerequisites
- BTDP Framework project with `modules/` directory structure
- Deployed infrastructure in target environment
- Access to enterprise GCP projects (workflows, src, dmn, published)
- Proper service account permissions for multi-project access

## Protocol

### Input Arguments
```
$ARGUMENTS: End-to-end test scenarios for BTDP Framework enterprise data pipelines
```

You must follow this protocol completely. Create a Todo list according to these steps:

1. Analyze BTDP Framework project architecture and identify test scenarios
2. Create enterprise test structure following `btdp-domains-it` patterns
3. **Implement distributed pipeline testing** across enterprise project separation
4. Add GCS bucket management and workflow trigger procedures
5. **Implement workflow monitoring** with proper timing for state machine delays
6. **Test complete SRC → DMN → SDDS flow** with enterprise validation
7. Format test code with `black -l 120`
8. **Document enterprise test procedures** with environment-specific configurations
9. Add test execution instructions for make commands
10. Commit enterprise test implementation and push to remote

## Success Criteria
- [ ] **Enterprise pipeline testing** implemented following proven btdp-domains-it patterns
- [ ] **Distributed project architecture** tested (workflows, src, dmn, published projects)
- [ ] **State machine workflow triggers** properly handled with timing delays
- [ ] **Multi-environment support** configured (dv, qa, np, pd)
- [ ] Test dependencies managed via `requirements-e2etest.txt`
- [ ] All test scenarios documented with enterprise patterns
- [ ] Test code formatted with black -l 120
- [ ] Changes committed and pushed to remote

## BTDP Framework Test Architecture

### Enterprise Project Distribution

**Reference Implementation**: `btdp-domains-it/e2e-tests/test_iam_roles_simple.py`

BTDP Framework uses distributed GCP projects for enterprise separation:

```python
class BTDPPipelineE2ETest:
    """Enterprise data pipeline testing following L'Oréal BTDP patterns."""
    
    def __init__(self):
        """Initialize with enterprise project distribution."""
        self.env = os.environ.get("PROJECT_ENV", "dv")
        
        # BTDP Enterprise project distribution
        self.project_workflows = f"itg-btdpbackit-{self.env}"           # Workflows and modules
        self.project_src = f"itg-btdpback-gbl-ww-{self.env}"           # Raw datasets
        self.project_dmn = f"itg-btdpfront-gbl-ww-{self.env}"          # Domain datasets  
        self.project_published = f"itg-btdppublished-gbl-ww-{self.env}" # SDDS publication

        # Dataset configuration following BTDP naming patterns
        self.bucket_name = f"btdp0-gcs-{self.module_name}-eu-{self.env}"
        self.raw_dataset = f"btdp_ds_c1_{self.dataset_family}_eu_{self.env}"
        self.domain_dataset = f"btdp_ds_c1_{self.dataset_family}_eu_{self.env}"

        # Workflow configuration - enterprise naming conventions
        self.src_workflow = f"btdp0-wkf-SRC_{self.workflow_id}-ew1-{self.env}"
        self.dmn_workflow = f"btdp0-wkf-DMN_{self.workflow_id}-ew1-{self.env}"
        
        # Initialize multi-project clients for distributed architecture
        self.bq_location = "EU"  # EU data residency compliance
        self.bq_client_src = bigquery.Client(project=self.project_src, location=self.bq_location)
        self.bq_client_dmn = bigquery.Client(project=self.project_dmn, location=self.bq_location)
        self.bq_client_published = bigquery.Client(project=self.project_published, location=self.bq_location)
        self.storage_client = storage.Client(project=self.project_workflows)
```

### Test Dependencies Management

**`e2e-tests/requirements-e2etest.txt`** (following proven pattern):
```txt
# E2E test specific requirements - minimal and focused
google-cloud-bigquery==3.13.0
google-cloud-storage==2.13.0
```

**Installation and execution:**
```bash
# Install E2E test dependencies
pip install -r e2e-tests/requirements-e2etest.txt

# Run tests using make command
make -f ../../module.mk ENV=dv e2e-test
```

## Complete Data Pipeline Testing Patterns

### Enterprise Pipeline Flow Testing

Based on the proven `btdp-domains-it` success with IAM roles pipeline (1,961 roles, 111K permissions):

```python
#!/usr/bin/env python3
"""
BTDP Enterprise Data Pipeline End-to-End Test
============================================

Tests complete SRC → DMN → SDDS pipeline flow following L'Oréal enterprise patterns:
1. Clean raw and domain tables across distributed projects
2. Clean GCS trigger bucket (remove activation files)
3. Trigger SRC workflow (data extraction from GCP APIs)
4. Monitor SRC workflow execution with enterprise timeouts
5. Wait for automatic DMN workflow trigger via state machine (5-min delay)
6. Monitor DMN workflow execution (domain transformation)
7. Verify data in domain tables (source of truth)
8. Verify SDDS published views with access control validation

Enterprise Architecture:
- Workflows Project: itg-btdpbackit-{env} (orchestration + modules)
- SRC Data Project: itg-btdpback-gbl-ww-{env} (raw datasets + external tables)
- DMN Data Project: itg-btdpfront-gbl-ww-{env} (domain datasets + business logic)
- SDDS Project: itg-btdppublished-gbl-ww-{env} (published access-controlled views)
"""

import os
import sys
import time
import json
import logging
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime

from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

# Configure enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'/tmp/btdp_pipeline_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
    ],
)
logger = logging.getLogger(__name__)

class BTDPEnterprisePipelineTest:
    """Complete enterprise data pipeline test following BTDP Framework patterns."""

    def __init__(self, module_name: str, dataset_family: str, workflow_id: str):
        """Initialize test with enterprise project distribution."""
        self.env = os.environ.get("PROJECT_ENV", "dv")
        self.module_name = module_name
        self.dataset_family = dataset_family
        self.workflow_id = workflow_id
        
        logger.info(f"Initializing BTDP Enterprise Pipeline Test for environment: {self.env}")
        logger.info(f"Module: {module_name}, Dataset Family: {dataset_family}, Workflow: {workflow_id}")

        # BTDP Enterprise project distribution
        self.project_workflows = f"itg-btdpbackit-{self.env}"           # Workflows and modules
        self.project_src = f"itg-btdpback-gbl-ww-{self.env}"           # Raw datasets
        self.project_dmn = f"itg-btdpfront-gbl-ww-{self.env}"          # Domain datasets  
        self.project_published = f"itg-btdppublished-gbl-ww-{self.env}" # SDDS publication

        # Enterprise resource configuration
        self.bucket_name = f"btdp0-gcs-{module_name}-eu-{self.env}"
        self.raw_dataset = f"btdp_ds_c1_{dataset_family}_eu_{self.env}"
        self.domain_dataset = f"btdp_ds_c1_{dataset_family}_eu_{self.env}"

        # Enterprise workflow naming patterns
        self.src_workflow = f"btdp0-wkf-SRC_{workflow_id}-ew1-{self.env}"
        self.dmn_workflow = f"btdp0-wkf-DMN_{workflow_id}-ew1-{self.env}"
        
        # Test timing for workflow filtering (enterprise requirement)
        self.test_start_time = None

        # Initialize multi-project clients for enterprise distributed architecture
        self.bq_location = "EU"  # EU data residency compliance
        logger.info("Initializing enterprise multi-project clients...")
        try:
            self.bq_client_src = bigquery.Client(project=self.project_src, location=self.bq_location)
            self.bq_client_dmn = bigquery.Client(project=self.project_dmn, location=self.bq_location)
            self.bq_client_published = bigquery.Client(project=self.project_published, location=self.bq_location)
            self.storage_client = storage.Client(project=self.project_workflows)
            logger.info("✅ All enterprise clients initialized successfully")
        except GoogleCloudError as e:
            logger.error(f"❌ Failed to initialize enterprise clients: {e}")
            sys.exit(1)

    def run_bigquery_query(self, client: bigquery.Client, query: str) -> list:
        """Execute BigQuery query with enterprise error handling."""
        try:
            logger.debug(f"Executing enterprise query: {query}")
            job_config = bigquery.QueryJobConfig()
            query_job = client.query(query, job_config=job_config)
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"❌ Enterprise BigQuery query failed: {query}")
            logger.error(f"Error: {e}")
            return []

    def run_gcloud_command(self, cmd: list) -> Dict[str, Any]:
        """Execute gcloud command with enterprise authentication."""
        try:
            logger.debug(f"Executing enterprise command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Enterprise command failed: {' '.join(cmd)}")
            logger.error(f"Error: {e.stderr}")
            raise
        except json.JSONDecodeError:
            logger.error(f"❌ Failed to parse JSON from enterprise command output")
            raise

    def clean_enterprise_pipeline_tables(self, raw_tables: list, domain_tables: list):
        """Clean all pipeline tables across enterprise project distribution."""
        logger.info("🧹 Step 1: Cleaning enterprise pipeline tables...")

        # Clean raw tables in SRC project
        for table in raw_tables:
            query = f"DELETE FROM `{self.project_src}.{self.raw_dataset}.{table}` WHERE TRUE;"
            try:
                self.run_bigquery_query(self.bq_client_src, query)
                logger.info(f"✅ Cleaned SRC table: {self.project_src}.{self.raw_dataset}.{table}")
            except Exception as e:
                if "404" in str(e) and "not found" in str(e).lower():
                    logger.info(f"ℹ️  SRC table {table} will be created during pipeline execution")
                else:
                    logger.warning(f"⚠️  Failed to clean SRC table {table}: {e}")

        # Clean domain tables in DMN project
        for table in domain_tables:
            query = f"DELETE FROM `{self.project_dmn}.{self.domain_dataset}.{table}` WHERE TRUE;"
            try:
                self.run_bigquery_query(self.bq_client_dmn, query)
                logger.info(f"✅ Cleaned DMN table: {self.project_dmn}.{self.domain_dataset}.{table}")
            except Exception as e:
                if "404" in str(e) and "not found" in str(e).lower():
                    logger.info(f"ℹ️  DMN table {table} will be created during pipeline execution")
                else:
                    logger.warning(f"⚠️  Failed to clean DMN table {table}: {e}")

    def clean_enterprise_trigger_bucket(self):
        """Clean GCS bucket to remove enterprise trigger files."""
        logger.info("🗑️  Step 2: Cleaning enterprise GCS trigger bucket...")
        
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blobs = list(bucket.list_blobs())

            if not blobs:
                logger.info(f"✅ Enterprise bucket {self.bucket_name} is already empty")
                return

            logger.info(f"Deleting {len(blobs)} trigger files from enterprise bucket {self.bucket_name}")
            for blob in blobs:
                blob.delete()
                logger.debug(f"Deleted enterprise trigger file: {blob.name}")

            logger.info(f"✅ Cleaned enterprise bucket {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ Failed to clean enterprise bucket {self.bucket_name}: {e}")
            raise

    def trigger_enterprise_src_workflow(self) -> str:
        """Trigger enterprise SRC workflow and return execution ID."""
        logger.info("🚀 Step 3: Triggering enterprise SRC workflow...")

        cmd = [
            "gcloud", "workflows", "run", self.src_workflow,
            "--project", self.project_workflows,
            "--location=europe-west1",
            "--format=json",
        ]

        try:
            result = self.run_gcloud_command(cmd)
            execution_id = result.get("name", "").split("/")[-1]
            logger.info(f"✅ Enterprise SRC workflow triggered - Execution: {execution_id}")
            return execution_id
        except Exception as e:
            logger.error(f"❌ Failed to trigger enterprise SRC workflow: {e}")
            raise

    def check_enterprise_workflow_status(self, workflow_name: str, execution_id: str) -> str:
        """Check enterprise workflow execution status."""
        cmd = [
            "gcloud", "workflows", "executions", "describe", execution_id,
            "--workflow", workflow_name,
            "--project", self.project_workflows,
            "--location=europe-west1",
            "--format=json",
        ]

        try:
            result = self.run_gcloud_command(cmd)
            status = result.get("state", "UNKNOWN")
            return status
        except Exception:
            return "UNKNOWN"

    def monitor_enterprise_workflow(self, workflow_name: str, execution_id: str, max_wait_minutes: int = 10) -> bool:
        """Monitor enterprise workflow execution with proper timeouts."""
        logger.info(f"⏳ Monitoring enterprise workflow: {workflow_name}")

        check_interval = 30  # seconds
        max_checks = (max_wait_minutes * 60) // check_interval

        for i in range(max_checks):
            status = self.check_enterprise_workflow_status(workflow_name, execution_id)
            logger.info(f"Enterprise workflow {workflow_name} status: {status} ({i+1}/{max_checks})")

            if status == "SUCCEEDED":
                logger.info(f"✅ Enterprise workflow {workflow_name} completed successfully")
                return True
            elif status == "FAILED":
                logger.error(f"❌ Enterprise workflow {workflow_name} failed")
                return False
            elif status in ["CANCELLED", "UNKNOWN"]:
                logger.error(f"❌ Enterprise workflow {workflow_name} ended with status: {status}")
                return False

            time.sleep(check_interval)

        logger.error(f"❌ Enterprise workflow {workflow_name} timeout after {max_wait_minutes} minutes")
        return False

    def wait_for_enterprise_dmn_workflow(self) -> Optional[str]:
        """Wait for enterprise DMN workflow automatic trigger via state machine."""
        logger.info("⏳ Step 5: Waiting for enterprise DMN workflow automatic trigger...")
        logger.info(f"Looking for DMN executions started after: {self.test_start_time}")
        logger.info("📝 Note: Enterprise state machine has 5-minute delay for data stabilization")

        max_wait_minutes = 20  # Account for enterprise state machine delay
        check_interval = 60    # Check every minute for enterprise timing

        for i in range(max_wait_minutes):
            cmd = [
                "gcloud", "workflows", "executions", "list", self.dmn_workflow,
                "--project", self.project_workflows,
                "--location=europe-west1",
                f"--filter=start_time>={self.test_start_time}",
                "--limit=5", "--format=json",
            ]

            try:
                result = self.run_gcloud_command(cmd)
                if result and len(result) > 0:
                    execution_id = result[0].get("name", "").split("/")[-1]
                    start_time = result[0].get("startTime", "")
                    logger.info(f"✅ Enterprise DMN workflow triggered - Execution: {execution_id} (started: {start_time})")
                    return execution_id

                elapsed_minutes = (i + 1) * (check_interval / 60)
                logger.info(f"Waiting for enterprise DMN trigger... ({elapsed_minutes:.0f}/{max_wait_minutes} min)")
                if elapsed_minutes < 5:
                    logger.info(f"⏰ Enterprise state machine delay in progress... {5 - elapsed_minutes:.0f} minutes remaining")
                time.sleep(check_interval)

            except Exception as e:
                logger.warning(f"Error checking enterprise DMN workflow: {e}")
                time.sleep(check_interval)

        logger.error(f"❌ Enterprise DMN workflow was not triggered within {max_wait_minutes} minutes")
        return None

    def verify_enterprise_domain_data(self, domain_tables: list) -> bool:
        """Verify data exists in enterprise domain tables (source of truth)."""
        logger.info("✅ Step 7: Verifying enterprise domain data...")

        for table, description in domain_tables:
            query = f"SELECT COUNT(*) as count FROM `{self.project_dmn}.{self.domain_dataset}.{table}`;"
            
            try:
                result = self.run_bigquery_query(self.bq_client_dmn, query)
                if result and len(result) > 0:
                    count = result[0].get("count", 0)
                    if count > 0:
                        logger.info(f"✅ Found {count} records in enterprise {description} table")
                    else:
                        logger.error(f"❌ No data found in enterprise {description} table")
                        return False
                else:
                    logger.error(f"❌ Failed to query enterprise {description} table")
                    return False
            except Exception as e:
                if "404" in str(e) and "not found" in str(e).lower():
                    logger.error(f"❌ Enterprise {description} table does not exist: {self.project_dmn}.{self.domain_dataset}.{table}")
                    logger.error("   This indicates the enterprise DMN workflow failed to create domain tables")
                else:
                    logger.error(f"❌ Error verifying enterprise {description} table: {e}")
                return False

        return True

    def verify_enterprise_published_views(self, domain_tables: list) -> bool:
        """Verify enterprise SDDS published views with access control."""
        logger.info("✅ Step 8: Verifying enterprise SDDS published views...")

        for table, description in domain_tables:
            query = f"SELECT COUNT(*) as count FROM `{self.project_published}.{self.domain_dataset}.{table}` LIMIT 1;"
            
            try:
                result = self.run_bigquery_query(self.bq_client_published, query)
                if result and len(result) > 0:
                    count = result[0].get("count", 0)
                    logger.info(f"✅ Enterprise SDDS {description} view accessible (shows {count} records)")
                else:
                    logger.error(f"❌ Failed to query enterprise SDDS {description} view")
                    return False
            except Exception as e:
                if "404" in str(e) and "not found" in str(e).lower():
                    logger.error(f"❌ Enterprise SDDS {description} view does not exist")
                    return False
                elif "access denied" in str(e).lower() or "permission" in str(e).lower():
                    logger.info(f"✅ Enterprise SDDS {description} view exists (access control working)")
                else:
                    logger.error(f"❌ Error verifying enterprise SDDS {description} view: {e}")
                    return False

        return True

    def run_complete_enterprise_test(self, raw_tables: list, domain_tables: list) -> bool:
        """Run complete enterprise pipeline test following BTDP patterns."""
        logger.info("🚀 Starting BTDP Enterprise Data Pipeline End-to-End Test")
        logger.info(f"Environment: {self.env}")
        logger.info(f"Enterprise Workflows Project: {self.project_workflows}")
        logger.info(f"Enterprise SRC Data Project: {self.project_src}")
        logger.info(f"Enterprise DMN Data Project: {self.project_dmn}")
        logger.info(f"Enterprise SDDS Project: {self.project_published}")
        logger.info(f"SRC Workflow: {self.src_workflow}")
        logger.info(f"DMN Workflow: {self.dmn_workflow}")
        logger.info("=" * 80)

        start_time = time.time()
        # Store test start time in ISO format for enterprise workflow filtering
        self.test_start_time = datetime.utcnow().isoformat() + "Z"

        try:
            # Step 1: Clean enterprise pipeline tables
            self.clean_enterprise_pipeline_tables(raw_tables, domain_tables)

            # Step 2: Clean enterprise trigger bucket
            self.clean_enterprise_trigger_bucket()

            # Step 3: Trigger enterprise SRC workflow
            src_execution_id = self.trigger_enterprise_src_workflow()

            # Step 4: Monitor enterprise SRC workflow
            if not self.monitor_enterprise_workflow(self.src_workflow, src_execution_id, max_wait_minutes=10):
                logger.error("❌ Enterprise test failed: SRC workflow did not complete successfully")
                return False

            # Step 5: Wait for enterprise DMN workflow trigger
            dmn_execution_id = self.wait_for_enterprise_dmn_workflow()
            if not dmn_execution_id:
                logger.error("❌ Enterprise test failed: DMN workflow was not triggered")
                return False

            # Step 6: Monitor enterprise DMN workflow
            if not self.monitor_enterprise_workflow(self.dmn_workflow, dmn_execution_id, max_wait_minutes=10):
                logger.error("❌ Enterprise test failed: DMN workflow did not complete successfully")
                return False

            # Step 7: Verify enterprise domain data (source of truth)
            if not self.verify_enterprise_domain_data(domain_tables):
                logger.error("❌ Enterprise test failed: No data found in domain tables")
                return False

            # Step 8: Verify enterprise SDDS published views
            if not self.verify_enterprise_published_views(domain_tables):
                logger.error("❌ Enterprise test failed: SDDS published views not accessible")
                return False

            elapsed_time = (time.time() - start_time) / 60
            logger.info("=" * 80)
            logger.info(f"🎉 BTDP ENTERPRISE PIPELINE TEST PASSED! (Duration: {elapsed_time:.1f} minutes)")
            logger.info("✅ All enterprise steps completed successfully:")
            logger.info("   1. ✅ Enterprise pipeline tables cleaned")
            logger.info("   2. ✅ Enterprise trigger bucket cleaned")
            logger.info("   3. ✅ Enterprise SRC workflow triggered")
            logger.info("   4. ✅ Enterprise SRC workflow completed")
            logger.info("   5. ✅ Enterprise DMN workflow triggered automatically")
            logger.info("   6. ✅ Enterprise DMN workflow completed")
            logger.info("   7. ✅ Enterprise domain data verified")
            logger.info("   8. ✅ Enterprise SDDS views verified")
            return True

        except Exception as e:
            elapsed_time = (time.time() - start_time) / 60
            logger.error("=" * 80)
            logger.error(f"❌ BTDP ENTERPRISE PIPELINE TEST FAILED! (Duration: {elapsed_time:.1f} minutes)")
            logger.error(f"Error: {e}")
            return False

# Example usage for specific module
def test_iam_roles_pipeline():
    """Test IAM roles pipeline following btdp-domains-it proven pattern."""
    test = BTDPEnterprisePipelineTest(
        module_name="0a1-iamroles-dumper",
        dataset_family="0a1_gcpassets",
        workflow_id="0a1_iamroles"
    )
    
    raw_tables = ["raw_roles_v1"]
    domain_tables = [
        ("roles_v1", "IAM roles"),
        ("role_permissions_v1", "IAM role permissions")
    ]
    
    return test.run_complete_enterprise_test(raw_tables, domain_tables)

def main():
    """Main entry point for enterprise pipeline testing."""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        return

    # Example: Test IAM roles pipeline (proven success case)
    success = test_iam_roles_pipeline()

    if success:
        logger.info("Enterprise pipeline test completed successfully")
        sys.exit(0)
    else:
        logger.error("Enterprise pipeline test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Enterprise Error Recovery Procedures

### Common Enterprise Issues

| Enterprise Issue | Common Causes | Solutions | Escalation |
|------------------|---------------|-----------|------------|
| **Multi-project access denied** | Missing IAM permissions | Use `-adm` account for setup | Enterprise security team |
| **Workflow not triggered** | State machine configuration | Check SDDS project regex | BTDP Framework team |
| **DMN workflow delay** | State machine 5-min delay | Normal behavior - wait 20 min | None required |
| **Published views access denied** | SDDS access control | Expected for access-controlled views | Verify view exists |
| **BigQuery quota exceeded** | High data volume | Use test-specific projects | Quota management team |

### Enterprise Testing Execution

**Command Execution:**
```bash
# Navigate to module directory
cd modules/your-module-name

# Install enterprise test dependencies
pip install -r e2e-tests/requirements-e2etest.txt

# Run enterprise end-to-end tests
make -f ../../module.mk ENV=dv e2e-test

# Check test logs
tail -f /tmp/btdp_pipeline_test_*.log
```

**Environment Configuration:**
```bash
# Set enterprise environment
export PROJECT_ENV=dv  # or qa, np, pd

# Verify enterprise access
gcloud auth list
gcloud config get-value project

# Test enterprise connectivity
gcloud projects list --filter="name:itg-btdp*"
```

## Example Usage

**BTDP Framework Example (Based on proven btdp-domains-it success):**
```
$ARGUMENTS: Implement enterprise end-to-end tests for GCP Assets data pipeline following the proven btdp-domains-it pattern. Test complete SRC → DMN → SDDS flow with:

Module Configuration:
- Module: 0a1-gcpassets-dumper
- Dataset Family: 0a1_gcpassets  
- Workflow ID: 0a1_gcpassets

Test Scope:
- Clean raw tables in itg-btdpback-gbl-ww-dv (assets_dump_v1, projects_v3, etc.)
- Clean domain tables in itg-btdpfront-gbl-ww-dv (processed assets)
- Clean GCS trigger bucket btdp0-gcs-0a1-gcpassets-dumper-eu-dv
- Trigger SRC workflow: btdp0-wkf-SRC_0a1_gcpassets-ew1-dv
- Monitor 10-minute SRC execution timeout
- Wait for DMN workflow trigger: btdp0-wkf-DMN_0a1_gcpassets-ew1-dv (20 min with 5-min state machine delay)
- Monitor 10-minute DMN execution timeout  
- Verify domain data in assets tables
- Verify SDDS published views with access control validation

Enterprise Environment: dv
Expected Duration: 25-30 minutes total
Reference: btdp-domains-it IAM roles success (1,961 roles, 111K permissions processed)
```