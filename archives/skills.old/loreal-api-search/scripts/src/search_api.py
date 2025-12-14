#!/usr/bin/env python3
"""
Search APIs in the BTDP API Portal using a regular expression pattern.

Usage:
    ./run.sh search_api <pattern> [--output FILE]

Arguments:
    pattern         Regular expression pattern to search API names

Options:
    --output FILE   Save results to file instead of stdout
"""

import argparse
import json
import os
import re
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


def list_apis(token):
    """
    List all APIs from the API portal.

    Args:
        token: Access token

    Returns:
        dict: API response data
    """
    url = f"{API_BASE_URL}/api-datas"
    params = {
        "top": 9000,
        "skip": 0,
        "environment": "prd",
    }
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()


def search_apis(pattern, token):
    """
    Search APIs using a regular expression pattern.

    Args:
        pattern: Regex pattern to match against API names
        token: Access token

    Returns:
        list: Matching API information
    """
    all_apis = list_apis(token)

    try:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
    except re.error as err:
        print(f"Error: Invalid regex pattern: {err}", file=sys.stderr)
        sys.exit(1)

    api_data = all_apis.get("data", [])
    if not isinstance(api_data, list):
        print(f"Error: Unexpected API data format", file=sys.stderr)
        return []

    matching_apis = []
    for api in api_data:
        api_name = api.get("apiName", "")
        if compiled_pattern.search(api_name):
            matching_apis.append(
                {
                    "apiName": api.get("apiName"),
                    "apiTitle": api.get("apiTitle"),
                    "apiDescription": api.get("apiDescription"),
                    "apiVersion": api.get("apiVersion"),
                    "apiCategory": api.get("apiCategory"),
                }
            )

    return matching_apis


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Search APIs in BTDP API Portal")
    parser.add_argument("pattern", help="Regular expression pattern to search")
    parser.add_argument("--output", help="Save results to file")

    args = parser.parse_args()

    try:
        token = get_access_token()
        results = search_apis(args.pattern, token)

        output = json.dumps(results, indent=2)

        if args.output:
            Path(args.output).write_text(output)
            print(f"Found {len(results)} APIs matching pattern '{args.pattern}'", file=sys.stderr)
            print(f"Results saved to {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
