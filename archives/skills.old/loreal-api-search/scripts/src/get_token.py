#!/usr/bin/env python3
"""
Get Azure OAuth access token for BTDP API Portal access.

This script retrieves Azure OAuth credentials from Google Secret Manager
and generates an access token using the client credentials flow.

Usage:
    ./run.sh get_token [--save]

Options:
    --save    Save the token to ~/.gcp/api_portal_token for reuse
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from google.cloud import secretmanager


# Configuration
SECRET_PROJECT_ID = os.getenv("SECRET_PROJECT_ID", "itg-btdpsecurity-gbl-ww-pd")
SECRET_NAME = os.getenv("SECRET_NAME", "btdp-srt-azure_app-pd")
OAUTH_URL = os.getenv("OAUTH_URL", "https://api.loreal.net/v1/oauth20/token")
OAUTH_SCOPE = "api://32a1cb44-61cd-4c6b-bd8e-1ecff52de813/.default"


def get_azure_credentials():
    """
    Retrieve Azure OAuth credentials from Google Secret Manager.

    Returns:
        dict: Dictionary containing tenant_id, client_id, and client_secret
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{SECRET_PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"

    response = client.access_secret_version(request={"name": secret_path})
    secret_data = response.payload.data.decode("UTF-8")

    return json.loads(secret_data)


def generate_access_token():
    """
    Generate Azure OAuth access token using client credentials flow.

    Returns:
        str: Access token for API authentication
    """
    credentials = get_azure_credentials()

    data = {
        "grant_type": "client_credentials",
        "client_id": credentials["client_id"],
        "scope": OAUTH_SCOPE,
        "client_secret": credentials["client_secret"],
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(OAUTH_URL, data=data, headers=headers, timeout=30)
    response.raise_for_status()

    token_data = response.json()
    return token_data["access_token"]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Get Azure OAuth access token for BTDP API Portal")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the token to ~/.claude/credentials/api_portal_token",
    )

    args = parser.parse_args()

    try:
        token = generate_access_token()

        if args.save:
            token_dir = Path.home() / ".claude" / "credentials"
            token_dir.mkdir(parents=True, exist_ok=True)
            token_file = token_dir / "api_portal_token"
            token_file.write_text(token)
            print(f"Token saved to {token_file}", file=sys.stderr)
        else:
            print(token)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
