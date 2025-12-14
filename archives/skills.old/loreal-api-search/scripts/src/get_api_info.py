#!/usr/bin/env python3
"""
Get detailed information about a specific API from the BTDP API Portal.

Usage:
    ./run.sh get_api_info <api_name> [--output FILE]

Arguments:
    api_name        Name of the API to retrieve information for

Options:
    --output FILE   Save results to file instead of stdout
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://api.loreal.net/global/it4it/coe/v1/apiinfos/api",
)


def get_access_token():
    """
    Get access token from saved file or environment.

    Returns:
        str: Access token
    """
    token_file = Path.home() / ".claude" / "credentials" / "api_portal_token"

    if token_file.exists():
        return token_file.read_text().strip()

    token = os.getenv("API_PORTAL_TOKEN")
    if token:
        return token

    print("Error: No access token found. Run './run.sh get_token --save' first.", file=sys.stderr)
    sys.exit(1)


def get_api_information(api_name, token):
    """
    Get information about an API.

    Args:
        api_name: Name of the API
        token: Access token

    Returns:
        dict: API information
    """
    url = f"{API_BASE_URL}/api-datas"
    params = {
        "top": 9000,
        "skip": 0,
        "apiName": api_name,
        "environment": "prd",
    }
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Get API information from BTDP API Portal")
    parser.add_argument("api_name", help="Name of the API")
    parser.add_argument("--output", help="Save results to file")

    args = parser.parse_args()

    try:
        token = get_access_token()
        result = get_api_information(args.api_name, token)

        output = json.dumps(result, indent=2)

        if args.output:
            Path(args.output).write_text(output)
            print(f"API information for '{args.api_name}' saved to {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
