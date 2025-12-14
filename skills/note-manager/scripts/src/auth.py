#!/usr/bin/env python3
"""
Google Keep Authentication
Handles login and token management for Google Keep API
"""

import gkeepapi
import os
import json
from pathlib import Path


def get_credentials_path():
    """Get path to credentials file."""
    return os.path.expanduser("~/.claude/credentials/gkeep_credentials.json")


def get_keep_client():
    """
    Get authenticated Google Keep client.

    Returns:
        gkeepapi.Keep: Authenticated Keep client
    """
    keep = gkeepapi.Keep()

    credentials_path = get_credentials_path()

    # Check if credentials exist
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Credentials not found at {credentials_path}\n"
            "Please run: cd ~/.claude/skills/note-manager/scripts && ./run.sh auth"
        )

    # Load credentials
    with open(credentials_path, "r") as f:
        creds = json.load(f)

    username = creds.get("username")
    token = creds.get("token")

    if not username or not token:
        raise ValueError("Invalid credentials file. Missing username or token.")

    # Resume session with master token (authenticate is the new method name but resume still works)
    keep.resume(username, token)

    return keep


def setup_credentials():
    """
    Interactive setup for Google Keep credentials.
    This should be run once to obtain and save the authentication token.
    """
    import getpass

    keep = gkeepapi.Keep()

    print("Google Keep Authentication Setup")
    print("=" * 40)
    username = input("Enter your Google email: ")
    password = getpass.getpass("Enter your password (or app password if 2FA enabled): ")

    try:
        print("Authenticating...")
        # Use authenticate instead of deprecated login
        success = keep.authenticate(username, password)

        if not success:
            raise Exception("Authentication failed - invalid credentials")

        # Get the master token
        token = keep.getMasterToken()

        # Save credentials
        credentials_path = get_credentials_path()
        Path(credentials_path).parent.mkdir(parents=True, exist_ok=True)

        with open(credentials_path, "w") as f:
            json.dump({"username": username, "token": token}, f)

        # Set proper permissions
        os.chmod(credentials_path, 0o600)

        print(f"\n✓ Authentication successful!")
        print(f"✓ Credentials saved to: {credentials_path}")
        print("\nYou can now use the Google Keep scripts.")

    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're using the correct Google account credentials")
        print("2. If you have 2FA enabled, you MUST use an App Password")
        print("   Generate one at: https://myaccount.google.com/apppasswords")
        print("3. Make sure 'Less secure app access' is enabled (if not using App Password)")
        print("4. Try using your Gmail address (not @loreal.com)")


if __name__ == "__main__":
    setup_credentials()
