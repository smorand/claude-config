#!/usr/bin/env python3
"""
GCP Project Auditor - Main orchestration script

This script audits a GCP project for security, compliance, and best practices.
It scans resources, IAM policies, and generates a comprehensive audit report.

Usage:
    python audit_project.py <project_id> [--output-dir <dir>]

Author: Sebastien MORAND
Email: sebastien.morand@loreal.com
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class GCPProjectAuditor:
    """Main auditor class for GCP project security audits."""

    def __init__(self, project_id: str, output_dir: Path, admin_account: str):
        self.project_id = project_id
        self.output_dir = output_dir
        self.admin_account = admin_account
        self.audit_timestamp = datetime.utcnow()

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize result storage
        self.results = {
            "project_id": project_id,
            "audit_timestamp": self.audit_timestamp.isoformat(),
            "auditor": admin_account,
            "project_info": {},
            "resources": [],
            "iam_policies": [],
            "service_accounts": [],
            "firewall_rules": [],
            "findings": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": [],
                "info": [],
            },
        }

    def run_gcloud_command(self, command: list[str], description: str) -> dict[str, Any] | list[Any] | None:
        """Execute a gcloud command and return JSON output."""
        console.print(f"[cyan]→[/cyan] {description}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout.strip():
                return json.loads(result.stdout)
            return None

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Error:[/red] {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            console.print(f"[red]✗ JSON parsing error:[/red] {e}")
            console.print(f"[dim]Output:[/dim] {result.stdout[:200]}")
            return None

    def get_project_info(self) -> dict[str, Any] | None:
        """Get project details and metadata."""
        console.print("\n[bold blue]Phase 1: Project Discovery[/bold blue]")

        command = [
            "gcloud",
            "--account",
            self.admin_account,
            "projects",
            "describe",
            self.project_id,
            "--format=json",
        ]

        project_info = self.run_gcloud_command(command, "Getting project details")

        if project_info:
            self.results["project_info"] = project_info

            # Extract environment tag
            labels = project_info.get("labels", {})
            env = labels.get("env", "unknown")
            console.print(f"[green]✓[/green] Environment: {env}")

            # Get project ancestors
            ancestors_cmd = [
                "gcloud",
                "--account",
                self.admin_account,
                "projects",
                "get-ancestors",
                self.project_id,
                "--format=json",
            ]
            ancestors = self.run_gcloud_command(ancestors_cmd, "Getting project ancestry")
            if ancestors:
                self.results["project_ancestors"] = ancestors

        return project_info

    def scan_resources(self) -> list[dict[str, Any]]:
        """Scan all resources in the project using Cloud Asset Inventory."""
        console.print("\n[bold blue]Phase 2: Resource Inventory[/bold blue]")

        command = [
            "gcloud",
            "--account",
            self.admin_account,
            "asset",
            "search-all-resources",
            f"--scope=projects/{self.project_id}",
            "--format=json",
        ]

        resources = self.run_gcloud_command(command, "Scanning all project resources")

        if resources:
            self.results["resources"] = resources
            console.print(f"[green]✓[/green] Found {len(resources)} resources")

            # Count by resource type
            resource_types = {}
            for resource in resources:
                asset_type = resource.get("assetType", "unknown")
                resource_types[asset_type] = resource_types.get(asset_type, 0) + 1

            console.print(f"[dim]Resource types:[/dim]")
            for asset_type, count in sorted(resource_types.items()):
                console.print(f"  • {asset_type}: {count}")

            # Save to file
            resources_file = self.output_dir / "resources.json"
            with open(resources_file, "w") as f:
                json.dump(resources, f, indent=2)
            console.print(f"[dim]Saved to {resources_file}[/dim]")

        return resources or []

    def scan_iam_policies(self) -> list[dict[str, Any]]:
        """Scan all IAM policies in the project."""
        console.print("\n[bold blue]Phase 3: IAM Security Analysis[/bold blue]")

        command = [
            "gcloud",
            "--account",
            self.admin_account,
            "asset",
            "search-all-iam-policies",
            f"--scope=projects/{self.project_id}",
            "--format=json",
        ]

        iam_policies = self.run_gcloud_command(command, "Scanning all IAM policies")

        if iam_policies:
            self.results["iam_policies"] = iam_policies
            console.print(f"[green]✓[/green] Found {len(iam_policies)} IAM policy bindings")

            # Save to file
            iam_file = self.output_dir / "iam-policies.json"
            with open(iam_file, "w") as f:
                json.dump(iam_policies, f, indent=2)
            console.print(f"[dim]Saved to {iam_file}[/dim]")

        # Also get project-level IAM policy
        project_iam_cmd = [
            "gcloud",
            "--account",
            self.admin_account,
            "projects",
            "get-iam-policy",
            self.project_id,
            "--format=json",
        ]

        project_iam = self.run_gcloud_command(project_iam_cmd, "Getting project-level IAM policy")

        if project_iam:
            self.results["project_iam_policy"] = project_iam
            bindings = project_iam.get("bindings", [])
            console.print(f"[green]✓[/green] Project has {len(bindings)} IAM role bindings")

        return iam_policies or []

    def scan_service_accounts(self) -> list[dict[str, Any]]:
        """Scan all service accounts and their permissions."""
        console.print("\n[bold blue]Phase 4: Service Account Analysis[/bold blue]")

        command = [
            "gcloud",
            "--account",
            self.admin_account,
            "iam",
            "service-accounts",
            "list",
            f"--project={self.project_id}",
            "--format=json",
        ]

        service_accounts = self.run_gcloud_command(command, "Listing service accounts")

        if service_accounts:
            self.results["service_accounts"] = service_accounts
            console.print(f"[green]✓[/green] Found {len(service_accounts)} service accounts")

            # For each service account, check who can impersonate
            for sa in service_accounts:
                sa_email = sa.get("email")
                if sa_email:
                    sa_policy_cmd = [
                        "gcloud",
                        "--account",
                        self.admin_account,
                        "iam",
                        "service-accounts",
                        "get-iam-policy",
                        sa_email,
                        f"--project={self.project_id}",
                        "--format=json",
                    ]
                    sa_policy = self.run_gcloud_command(sa_policy_cmd, f"Checking {sa_email} impersonation")
                    if sa_policy:
                        sa["iam_policy"] = sa_policy

        return service_accounts or []

    def scan_firewall_rules(self) -> list[dict[str, Any]]:
        """Scan firewall rules for security issues."""
        console.print("\n[bold blue]Phase 5: Network Security Review[/bold blue]")

        command = [
            "gcloud",
            "--account",
            self.admin_account,
            "compute",
            "firewall-rules",
            "list",
            f"--project={self.project_id}",
            "--format=json",
        ]

        firewall_rules = self.run_gcloud_command(command, "Listing firewall rules")

        if firewall_rules:
            self.results["firewall_rules"] = firewall_rules
            console.print(f"[green]✓[/green] Found {len(firewall_rules)} firewall rules")
        else:
            console.print("[dim]No firewall rules found (or compute API disabled)[/dim]")

        return firewall_rules or []

    def analyze_findings(self) -> None:
        """Analyze all collected data and identify security issues."""
        console.print("\n[bold blue]Phase 6: Security Analysis[/bold blue]")

        # Load excessive roles list
        excessive_roles = self._load_excessive_roles()

        # Get project environment
        env = self.results["project_info"].get("labels", {}).get("env", "unknown")
        is_production = env in ["pd", "np"]

        console.print(f"[cyan]Environment:[/cyan] {env}")
        console.print(f"[cyan]Production/Non-Prod:[/cyan] {'Yes' if is_production else 'No'}")

        # Analyze IAM policies for excessive roles
        if is_production:
            self._check_excessive_roles(excessive_roles)

        # Check for public access
        self._check_public_access()

        # Check for public Cloud Run and Cloud Functions
        self._check_public_cloud_run_functions()

        # Check for public IP addresses
        self._check_public_ip_addresses()

        # Check firewall rules
        self._check_firewall_rules()

        # Check service account keys
        self._check_service_account_keys()

        # Summary
        total_findings = sum(len(findings) for findings in self.results["findings"].values())
        console.print(f"\n[bold]Total Findings:[/bold] {total_findings}")
        for severity, findings in self.results["findings"].items():
            if findings:
                color = {
                    "critical": "red",
                    "high": "orange1",
                    "medium": "yellow",
                    "low": "blue",
                    "info": "dim",
                }.get(severity, "white")
                console.print(f"  [{color}]{severity.upper()}:[/{color}] {len(findings)}")

    def _load_excessive_roles(self) -> set[str]:
        """Load the list of excessive roles from reference file."""
        # This is a simplified version - in production, load from the markdown file
        # For now, return a subset of critical roles
        return {
            "roles/owner",
            "roles/editor",
            "roles/iam.securityAdmin",
            "roles/resourcemanager.organizationAdmin",
            "roles/compute.admin",
            "roles/bigquery.admin",
            "roles/storage.admin",
            "roles/iam.serviceAccountTokenCreator",
        }

    def _check_excessive_roles(self, excessive_roles: set[str]) -> None:
        """Check for excessive role assignments in production."""
        console.print("[cyan]→[/cyan] Checking for excessive roles in production")

        project_iam = self.results.get("project_iam_policy", {})
        bindings = project_iam.get("bindings", [])

        for binding in bindings:
            role = binding.get("role", "")
            members = binding.get("members", [])

            # Check if role is excessive
            if role in excessive_roles or any(role.endswith(r) for r in ["Admin", "admin", "serviceAgent"]):
                for member in members:
                    # Skip service accounts for service agent roles
                    if member.startswith("serviceAccount:") and "serviceAgent" in role:
                        continue

                    # Flag user accounts with excessive roles
                    if member.startswith("user:") or member.startswith("group:"):
                        self.results["findings"]["critical"].append(
                            {
                                "type": "excessive_role",
                                "severity": "critical",
                                "resource": f"projects/{self.project_id}",
                                "principal": member,
                                "role": role,
                                "message": f"Excessive role {role} granted to {member} in production environment",
                            }
                        )
                        console.print(f"[red]✗ CRITICAL:[/red] {member} has {role}")

    def _check_public_access(self) -> None:
        """Check for public access to resources."""
        console.print("[cyan]→[/cyan] Checking for public access")

        iam_policies = self.results.get("iam_policies", [])

        for policy in iam_policies:
            resource = policy.get("resource", "")
            iam_policy = policy.get("policy", {})
            bindings = iam_policy.get("bindings", [])

            for binding in bindings:
                members = binding.get("members", [])
                role = binding.get("role", "")

                if "allUsers" in members or "allAuthenticatedUsers" in members:
                    self.results["findings"]["critical"].append(
                        {
                            "type": "public_access",
                            "severity": "critical",
                            "resource": resource,
                            "role": role,
                            "members": members,
                            "message": f"Resource {resource} allows public access via {role}",
                        }
                    )
                    console.print(f"[red]✗ CRITICAL:[/red] Public access to {resource}")

    def _check_public_cloud_run_functions(self) -> None:
        """Check for publicly accessible Cloud Run services and Cloud Functions."""
        console.print("[cyan]→[/cyan] Checking for public Cloud Run services and Cloud Functions")

        resources = self.results.get("resources", [])

        for resource in resources:
            asset_type = resource.get("assetType", "")
            name = resource.get("name", "")

            # Check Cloud Run services
            if asset_type == "run.googleapis.com/Service":
                # Get IAM policy for this Cloud Run service
                iam_policy = resource.get("iamPolicy", {})
                bindings = iam_policy.get("bindings", [])

                # Check if allUsers has roles/run.invoker
                for binding in bindings:
                    members = binding.get("members", [])
                    role = binding.get("role", "")

                    if role == "roles/run.invoker" and "allUsers" in members:
                        self.results["findings"]["critical"].append(
                            {
                                "type": "public_cloud_run",
                                "severity": "critical",
                                "resource": name,
                                "role": role,
                                "message": f"Cloud Run service {name} allows unauthenticated public access",
                            }
                        )
                        console.print(f"[red]✗ CRITICAL:[/red] Public Cloud Run service: {name}")

            # Check Cloud Functions (1st gen)
            elif asset_type == "cloudfunctions.googleapis.com/CloudFunction":
                iam_policy = resource.get("iamPolicy", {})
                bindings = iam_policy.get("bindings", [])

                # Check if allUsers has roles/cloudfunctions.invoker
                for binding in bindings:
                    members = binding.get("members", [])
                    role = binding.get("role", "")

                    if role == "roles/cloudfunctions.invoker" and "allUsers" in members:
                        self.results["findings"]["critical"].append(
                            {
                                "type": "public_cloud_function",
                                "severity": "critical",
                                "resource": name,
                                "role": role,
                                "message": f"Cloud Function {name} allows unauthenticated public access",
                            }
                        )
                        console.print(f"[red]✗ CRITICAL:[/red] Public Cloud Function (1st gen): {name}")

            # Check Cloud Functions (2nd gen)
            elif asset_type == "cloudfunctions.googleapis.com/Function":
                iam_policy = resource.get("iamPolicy", {})
                bindings = iam_policy.get("bindings", [])

                # 2nd gen uses roles/run.invoker since it's built on Cloud Run
                for binding in bindings:
                    members = binding.get("members", [])
                    role = binding.get("role", "")

                    if role in ["roles/cloudfunctions.invoker", "roles/run.invoker"] and "allUsers" in members:
                        self.results["findings"]["critical"].append(
                            {
                                "type": "public_cloud_function",
                                "severity": "critical",
                                "resource": name,
                                "role": role,
                                "message": f"Cloud Function (2nd gen) {name} allows unauthenticated public access",
                            }
                        )
                        console.print(f"[red]✗ CRITICAL:[/red] Public Cloud Function (2nd gen): {name}")

    def _check_public_ip_addresses(self) -> None:
        """Check for resources with public IP addresses."""
        console.print("[cyan]→[/cyan] Checking for public IP addresses")

        resources = self.results.get("resources", [])

        for resource in resources:
            asset_type = resource.get("assetType", "")
            name = resource.get("name", "")
            resource_data = resource.get("resource", {}).get("data", {})

            # Check Cloud SQL instances for public IP
            if asset_type == "sqladmin.googleapis.com/Instance":
                ip_addresses = resource_data.get("ipAddresses", [])

                for ip_config in ip_addresses:
                    ip_type = ip_config.get("type", "")
                    ip_address = ip_config.get("ipAddress", "")

                    if ip_type == "PRIMARY":
                        # Cloud SQL has a public IP
                        settings = resource_data.get("settings", {})
                        ip_configuration = settings.get("ipConfiguration", {})

                        # Check if it's actually exposed (not just allocated)
                        if ip_configuration.get("ipv4Enabled", False):
                            self.results["findings"]["critical"].append(
                                {
                                    "type": "public_ip_database",
                                    "severity": "critical",
                                    "resource": name,
                                    "ip_address": ip_address,
                                    "message": f"Cloud SQL instance {name} has public IP enabled: {ip_address}",
                                }
                            )
                            console.print(f"[red]✗ CRITICAL:[/red] Cloud SQL with public IP: {name} ({ip_address})")

            # Check Compute Engine instances for external IP
            elif asset_type == "compute.googleapis.com/Instance":
                network_interfaces = resource_data.get("networkInterfaces", [])

                for interface in network_interfaces:
                    access_configs = interface.get("accessConfigs", [])

                    for access_config in access_configs:
                        nat_ip = access_config.get("natIP")
                        config_type = access_config.get("type", "")

                        if nat_ip and config_type == "ONE_TO_ONE_NAT":
                            self.results["findings"]["critical"].append(
                                {
                                    "type": "public_ip_compute",
                                    "severity": "critical",
                                    "resource": name,
                                    "ip_address": nat_ip,
                                    "message": f"Compute instance {name} has external IP address: {nat_ip}",
                                }
                            )
                            console.print(
                                f"[red]✗ CRITICAL:[/red] Compute instance with external IP: {name} ({nat_ip})"
                            )

            # Check AlloyDB clusters for public IP
            elif asset_type == "alloydb.googleapis.com/Cluster":
                network_config = resource_data.get("networkConfig", {})
                allocated_ip_range = network_config.get("allocatedIpRange")

                # AlloyDB should always be private, flag if there's any public exposure indication
                if resource_data.get("publicIpEnabled", False):
                    self.results["findings"]["critical"].append(
                        {
                            "type": "public_ip_database",
                            "severity": "critical",
                            "resource": name,
                            "message": f"AlloyDB cluster {name} has public IP enabled",
                        }
                    )
                    console.print(f"[red]✗ CRITICAL:[/red] AlloyDB with public IP: {name}")

    def _check_firewall_rules(self) -> None:
        """Check for overly permissive firewall rules."""
        console.print("[cyan]→[/cyan] Checking firewall rules")

        firewall_rules = self.results.get("firewall_rules", [])

        for rule in firewall_rules:
            name = rule.get("name", "")
            source_ranges = rule.get("sourceRanges", [])
            allowed = rule.get("allowed", [])

            # Check for 0.0.0.0/0 with sensitive ports
            if "0.0.0.0/0" in source_ranges:
                sensitive_ports = {"22", "3389", "3306", "5432", "1433", "27017"}

                for allow_rule in allowed:
                    ip_protocol = allow_rule.get("IPProtocol", "")
                    ports = allow_rule.get("ports", [])

                    # Check if any port is sensitive
                    if any(port in sensitive_ports for port in ports):
                        self.results["findings"]["high"].append(
                            {
                                "type": "overly_permissive_firewall",
                                "severity": "high",
                                "resource": name,
                                "source_ranges": source_ranges,
                                "allowed_ports": ports,
                                "message": f"Firewall rule {name} allows {source_ranges} to sensitive ports {ports}",
                            }
                        )
                        console.print(f"[orange1]✗ HIGH:[/orange1] Firewall {name} allows 0.0.0.0/0 to ports {ports}")

    def _check_service_account_keys(self) -> None:
        """Check for user-managed service account keys."""
        console.print("[cyan]→[/cyan] Checking service account keys")

        service_accounts = self.results.get("service_accounts", [])

        for sa in service_accounts:
            sa_email = sa.get("email", "")

            # List keys for this service account
            keys_cmd = [
                "gcloud",
                "--account",
                self.admin_account,
                "iam",
                "service-accounts",
                "keys",
                "list",
                f"--iam-account={sa_email}",
                f"--project={self.project_id}",
                "--format=json",
            ]

            keys = self.run_gcloud_command(keys_cmd, f"Checking keys for {sa_email}")

            if keys:
                # Filter user-managed keys (exclude Google-managed)
                user_keys = [k for k in keys if k.get("keyType") == "USER_MANAGED"]

                if user_keys:
                    self.results["findings"]["high"].append(
                        {
                            "type": "service_account_keys",
                            "severity": "high",
                            "resource": sa_email,
                            "key_count": len(user_keys),
                            "message": f"Service account {sa_email} has {len(user_keys)} user-managed keys",
                        }
                    )
                    console.print(f"[orange1]✗ HIGH:[/orange1] {sa_email} has {len(user_keys)} user-managed keys")

    def generate_report(self) -> Path:
        """Generate the final audit report in markdown format."""
        console.print("\n[bold blue]Phase 7: Report Generation[/bold blue]")

        # Save raw results
        results_file = self.output_dir / "audit-results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        console.print(f"[dim]Saved raw results to {results_file}[/dim]")

        # Generate markdown report
        report_file = self.output_dir / f"audit-report-{self.project_id}.md"

        with open(report_file, "w") as f:
            self._write_report(f)

        console.print(f"[green]✓[/green] Audit report generated: {report_file}")
        return report_file

    def _write_report(self, f) -> None:
        """Write the markdown audit report."""
        # Header
        f.write(f"# GCP Project Audit Report: {self.project_id}\n\n")
        f.write(f"**Audit Date**: {self.audit_timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        f.write(f"**Auditor**: {self.admin_account}\n")

        env = self.results["project_info"].get("labels", {}).get("env", "unknown")
        f.write(f"**Project Environment**: {env}\n")
        f.write(f"**Audit Version**: 1.0\n\n")
        f.write("---\n\n")

        # Executive Summary
        total_findings = sum(len(findings) for findings in self.results["findings"].values())
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Resources**: {len(self.results.get('resources', []))}\n")
        f.write(f"- **Critical Findings**: {len(self.results['findings']['critical'])}\n")
        f.write(f"- **High Findings**: {len(self.results['findings']['high'])}\n")
        f.write(f"- **Medium Findings**: {len(self.results['findings']['medium'])}\n")
        f.write(f"- **Total Findings**: {total_findings}\n\n")

        # Risk assessment
        if self.results["findings"]["critical"]:
            risk_level = "🔴 CRITICAL"
        elif self.results["findings"]["high"]:
            risk_level = "🟠 HIGH"
        elif self.results["findings"]["medium"]:
            risk_level = "🟡 MEDIUM"
        else:
            risk_level = "🟢 LOW"

        f.write(f"**Overall Risk Level**: {risk_level}\n\n")
        f.write("---\n\n")

        # Project Overview
        f.write("## 1. Project Overview\n\n")
        project_info = self.results.get("project_info", {})
        f.write(f"- **Project ID**: {project_info.get('projectId', 'N/A')}\n")
        f.write(f"- **Project Number**: {project_info.get('projectNumber', 'N/A')}\n")
        f.write(f"- **Project Name**: {project_info.get('name', 'N/A')}\n")
        f.write(f"- **Environment**: {env}\n")
        f.write(f"- **State**: {project_info.get('lifecycleState', 'N/A')}\n")
        f.write(f"- **Created**: {project_info.get('createTime', 'N/A')}\n\n")

        # Resource Inventory
        f.write("## 2. Resource Inventory\n\n")
        resources = self.results.get("resources", [])

        # Count by type
        resource_types = {}
        for resource in resources:
            asset_type = resource.get("assetType", "unknown")
            resource_types[asset_type] = resource_types.get(asset_type, 0) + 1

        f.write("### Resources by Type\n\n")
        f.write("| Resource Type | Count |\n")
        f.write("|---------------|-------|\n")
        for asset_type, count in sorted(resource_types.items()):
            f.write(f"| {asset_type} | {count} |\n")
        f.write("\n")

        # IAM Analysis
        f.write("## 3. IAM Security Analysis\n\n")
        project_iam = self.results.get("project_iam_policy", {})
        bindings = project_iam.get("bindings", [])
        f.write(f"**Total Project-Level Bindings**: {len(bindings)}\n\n")

        # Findings
        f.write("## 4. Security Findings\n\n")

        for severity in ["critical", "high", "medium", "low"]:
            findings = self.results["findings"][severity]
            if findings:
                emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🔵",
                }[severity]
                f.write(f"### {emoji} {severity.upper()} Findings\n\n")

                for idx, finding in enumerate(findings, 1):
                    f.write(f"#### {idx}. {finding.get('type', 'Unknown')}\n\n")
                    f.write(f"- **Severity**: {finding.get('severity', 'N/A')}\n")
                    f.write(f"- **Resource**: {finding.get('resource', 'N/A')}\n")
                    f.write(f"- **Message**: {finding.get('message', 'N/A')}\n\n")

                    # Additional details
                    for key, value in finding.items():
                        if key not in ["type", "severity", "resource", "message"]:
                            f.write(f"- **{key.replace('_', ' ').title()}**: {value}\n")
                    f.write("\n")

        # Recommendations
        f.write("## 5. Recommendations\n\n")
        if self.results["findings"]["critical"]:
            f.write("### ⚠️ IMMEDIATE ACTION REQUIRED\n\n")
            f.write("1. Remove excessive roles from production environment immediately\n")
            f.write("2. Disable public access to all resources\n")
            f.write("3. Review and restrict firewall rules\n\n")

        f.write("### General Recommendations\n\n")
        f.write("1. Follow principle of least privilege for all IAM assignments\n")
        f.write("2. Use service accounts instead of user accounts for automation\n")
        f.write("3. Enable uniform bucket-level access on all Cloud Storage buckets\n")
        f.write("4. Rotate or remove user-managed service account keys\n")
        f.write("5. Enable VPC Flow Logs for network monitoring\n")
        f.write("6. Regular audits (monthly for production projects)\n\n")

        # Appendix
        f.write("---\n\n")
        f.write("## Appendix\n\n")
        f.write("### Full Audit Data\n\n")
        f.write(f"Complete audit data saved to: `audit-results.json`\n\n")

    def run(self) -> Path:
        """Run the complete audit process."""
        console.print("[bold green]GCP Project Security Audit[/bold green]")
        console.print(f"[dim]Project:[/dim] {self.project_id}")
        console.print(f"[dim]Output:[/dim] {self.output_dir}")
        console.print(f"[dim]Account:[/dim] {self.admin_account}\n")

        try:
            # Phase 1: Project Discovery
            self.get_project_info()

            # Phase 2: Resource Inventory
            self.scan_resources()

            # Phase 3: IAM Analysis
            self.scan_iam_policies()

            # Phase 4: Service Account Analysis
            self.scan_service_accounts()

            # Phase 5: Network Security
            self.scan_firewall_rules()

            # Phase 6: Analysis
            self.analyze_findings()

            # Phase 7: Report Generation
            report_file = self.generate_report()

            console.print(f"\n[bold green]✓ Audit completed successfully![/bold green]")
            console.print(f"[dim]Report:[/dim] {report_file}")

            return report_file

        except Exception as e:
            console.print(f"\n[bold red]✗ Audit failed:[/bold red] {e}")
            import traceback

            console.print(traceback.format_exc())
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Audit a GCP project for security and compliance")
    parser.add_argument("project_id", help="GCP project ID to audit")
    parser.add_argument(
        "--output-dir",
        default="./audit-output",
        help="Output directory for audit results (default: ./audit-output)",
    )
    parser.add_argument(
        "--admin-account",
        default="sebastien.morand-adm@loreal.com",
        help="Admin account to use for gcloud commands",
    )

    args = parser.parse_args()

    auditor = GCPProjectAuditor(
        project_id=args.project_id,
        output_dir=Path(args.output_dir),
        admin_account=args.admin_account,
    )

    auditor.run()


if __name__ == "__main__":
    main()
