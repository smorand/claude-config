#!/usr/bin/env python3
"""
Office 365 Manager - Email and Calendar Management Tool
Uses OAuth 2.1 PKCE for authentication with Microsoft Graph API
"""

import json
import os
import sys
import webbrowser
import subprocess
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import hashlib
import base64
import secrets
import requests
from datetime import datetime, timedelta, timezone

# Configuration
CLIENT_ID = "76d42bf5-d461-4274-bd4d-a02576b9df36"
TENANT_ID = "e4e1abd9-eac7-4a71-ab52-da5c998aa7ba"
REDIRECT_URI = "http://127.0.0.1:33418"
REDIRECT_PORT = 33418
SCOPES = [
    "https://graph.microsoft.com/Mail.ReadWrite",
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/Calendars.ReadWrite",
    "https://graph.microsoft.com/User.Read",
]

TOKEN_FILE = Path.home() / ".claude" / "credentials" / "o365_tokens.json"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


class OAuth2CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth2 callback"""

    def do_GET(self):
        """Handle GET request from OAuth2 redirect"""
        query_components = parse_qs(urlparse(self.path).query)

        if "code" in query_components:
            self.server.auth_code = query_components["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authentication successful!</h1><p>You can close this window.</p></body></html>"
            )
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication failed!</h1></body></html>")

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def generate_pkce_pair():
    """Generate PKCE code verifier and challenge"""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").rstrip("=")
    )
    return code_verifier, code_challenge


def get_auth_code(code_challenge):
    """Get authorization code via browser"""
    auth_url = (
        f"{AUTHORITY}/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope={' '.join(SCOPES)}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    print(f"Opening browser for authentication...")
    webbrowser.open(auth_url)

    # Start local server to receive callback
    server = HTTPServer(("127.0.0.1", REDIRECT_PORT), OAuth2CallbackHandler)
    server.auth_code = None
    server.handle_request()

    return server.auth_code


def get_tokens(auth_code, code_verifier):
    """Exchange authorization code for tokens"""
    token_url = f"{AUTHORITY}/oauth2/v2.0/token"

    data = {
        "client_id": CLIENT_ID,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    return response.json()


def refresh_access_token(refresh_token):
    """Refresh access token using refresh token"""
    token_url = f"{AUTHORITY}/oauth2/v2.0/token"

    data = {"client_id": CLIENT_ID, "grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    return response.json()


def save_tokens(tokens):
    """Save tokens to file"""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)


def load_tokens():
    """Load tokens from file"""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def get_access_token():
    """Get valid access token (refresh if needed)"""
    tokens = load_tokens()

    if not tokens:
        # New authentication required
        print("No existing tokens found. Starting authentication...")
        code_verifier, code_challenge = generate_pkce_pair()
        auth_code = get_auth_code(code_challenge)

        if not auth_code:
            raise Exception("Failed to get authorization code")

        tokens = get_tokens(auth_code, code_verifier)
        tokens["expires_at"] = datetime.now().timestamp() + tokens["expires_in"]
        save_tokens(tokens)
        print("Authentication successful!")
        return tokens["access_token"]

    # Check if token needs refresh (refresh if expires in less than 5 minutes)
    if "expires_at" in tokens:
        if datetime.now().timestamp() < tokens["expires_at"] - 300:
            return tokens["access_token"]

    # Refresh token
    try:
        print("Refreshing access token...", file=sys.stderr)
        new_tokens = refresh_access_token(tokens["refresh_token"])
        new_tokens["expires_at"] = datetime.now().timestamp() + new_tokens["expires_in"]
        save_tokens(new_tokens)
        print("Token refreshed successfully!", file=sys.stderr)
        return new_tokens["access_token"]
    except Exception as e:
        # Re-authenticate if refresh fails
        print(f"Token refresh failed: {e}. Re-authenticating...", file=sys.stderr)
        code_verifier, code_challenge = generate_pkce_pair()
        auth_code = get_auth_code(code_challenge)

        if not auth_code:
            raise Exception("Failed to get authorization code")

        tokens = get_tokens(auth_code, code_verifier)
        tokens["expires_at"] = datetime.now().timestamp() + tokens["expires_in"]
        save_tokens(tokens)
        return tokens["access_token"]


def make_graph_request(method, endpoint, data=None, params=None):
    """Make authenticated request to Microsoft Graph API"""
    access_token = get_access_token()

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    url = f"{GRAPH_API_ENDPOINT}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()

        if response.content:
            return response.json()
        return {}
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Request Error: {e}", file=sys.stderr)
        raise


# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================


def list_emails(folder="inbox", limit=10, unread_only=False, search=None):
    """List emails from specified folder"""
    params = {"$top": limit}

    # $search cannot be combined with $orderby in Microsoft Graph API
    if not search:
        params["$orderby"] = "receivedDateTime DESC"

    if unread_only:
        params["$filter"] = "isRead eq false"

    if search:
        params["$search"] = f'"{search}"'

    result = make_graph_request("GET", f"/me/mailFolders/{folder}/messages", params=params)

    emails = []
    for msg in result.get("value", []):
        emails.append(
            {
                "id": msg["id"],
                "subject": msg["subject"],
                "from": msg["from"]["emailAddress"]["address"] if msg.get("from") else "Unknown",
                "from_name": msg["from"]["emailAddress"]["name"] if msg.get("from") else "Unknown",
                "received": msg["receivedDateTime"],
                "is_read": msg["isRead"],
                "has_attachments": msg["hasAttachments"],
                "preview": msg["bodyPreview"],
            }
        )

    return emails


def read_email(message_id):
    """Read email content"""
    result = make_graph_request("GET", f"/me/messages/{message_id}")

    email_data = {
        "id": result["id"],
        "subject": result["subject"],
        "from": result["from"]["emailAddress"]["address"] if result.get("from") else "Unknown",
        "from_name": result["from"]["emailAddress"]["name"] if result.get("from") else "Unknown",
        "to": [addr["emailAddress"]["address"] for addr in result.get("toRecipients", [])],
        "cc": [addr["emailAddress"]["address"] for addr in result.get("ccRecipients", [])],
        "received": result["receivedDateTime"],
        "is_read": result["isRead"],
        "body_content_type": result["body"]["contentType"],
        "body": result["body"]["content"],
        "has_attachments": result["hasAttachments"],
    }

    if result["hasAttachments"]:
        attachments = make_graph_request("GET", f"/me/messages/{message_id}/attachments")
        email_data["attachments"] = [
            {"name": att["name"], "content_type": att["contentType"], "size": att["size"]}
            for att in attachments.get("value", [])
        ]

    return email_data


def send_email(to_addresses, subject, body, cc_addresses=None, body_type="HTML", attachments=None):
    """Send email with optional attachments"""
    message = {
        "message": {
            "subject": subject,
            "body": {"contentType": body_type, "content": body},
            "toRecipients": [{"emailAddress": {"address": addr}} for addr in to_addresses],
        }
    }

    if cc_addresses:
        message["message"]["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in cc_addresses]

    # Add attachments if provided
    if attachments:
        message["message"]["attachments"] = []
        for file_path in attachments:
            file_path = os.path.expanduser(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Attachment file not found: {file_path}")

            # Read file and encode to base64
            with open(file_path, "rb") as f:
                file_content = f.read()

            encoded_content = base64.b64encode(file_content).decode("utf-8")
            file_name = os.path.basename(file_path)

            message["message"]["attachments"].append(
                {"@odata.type": "#microsoft.graph.fileAttachment", "name": file_name, "contentBytes": encoded_content}
            )

    make_graph_request("POST", "/me/sendMail", data=message)
    return True


def create_draft(to_addresses, subject, body, cc_addresses=None, body_type="HTML", attachments=None):
    """Create draft email without sending, with optional attachments"""
    message = {
        "subject": subject,
        "body": {"contentType": body_type, "content": body},
        "toRecipients": [{"emailAddress": {"address": addr}} for addr in to_addresses],
    }

    if cc_addresses:
        message["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in cc_addresses]

    # Add attachments if provided
    if attachments:
        message["attachments"] = []
        for file_path in attachments:
            file_path = os.path.expanduser(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Attachment file not found: {file_path}")

            # Read file and encode to base64
            with open(file_path, "rb") as f:
                file_content = f.read()

            encoded_content = base64.b64encode(file_content).decode("utf-8")
            file_name = os.path.basename(file_path)

            message["attachments"].append(
                {"@odata.type": "#microsoft.graph.fileAttachment", "name": file_name, "contentBytes": encoded_content}
            )

    result = make_graph_request("POST", "/me/messages", data=message)
    return result


def reply_to_email(message_id, comment):
    """Reply to email"""
    reply_data = {"comment": comment}

    make_graph_request("POST", f"/me/messages/{message_id}/reply", data=reply_data)
    return True


def mark_email(message_id, is_read=True):
    """Mark email as read/unread"""
    update_data = {"isRead": is_read}

    make_graph_request("PATCH", f"/me/messages/{message_id}", data=update_data)
    return True


def delete_email(message_id):
    """Delete email"""
    make_graph_request("DELETE", f"/me/messages/{message_id}")
    return True


def get_mail_folders():
    """Get list of mail folders"""
    result = make_graph_request("GET", "/me/mailFolders")
    folders = {}
    for folder in result.get("value", []):
        folders[folder["displayName"].lower()] = folder["id"]
    return folders


def move_email(message_id, folder_name):
    """Move email to specified folder"""
    # Get folder ID
    folders = get_mail_folders()
    folder_name_lower = folder_name.lower()

    if folder_name_lower not in folders:
        raise ValueError(f"Folder '{folder_name}' not found. Available folders: {', '.join(folders.keys())}")

    folder_id = folders[folder_name_lower]

    # Move email
    move_data = {"destinationId": folder_id}

    make_graph_request("POST", f"/me/messages/{message_id}/move", data=move_data)
    return True


def archive_email(message_id):
    """Archive email (move to Archive folder)"""
    return move_email(message_id, "archive")


def search_emails(query, limit=20):
    """Search emails"""
    return list_emails(limit=limit, search=query)


def mark_important(message_id):
    """Mark email as important"""
    update_data = {"importance": "high", "categories": ["Important", "VIP"]}
    make_graph_request("PATCH", f"/me/messages/{message_id}", data=update_data)
    return True


def load_email_rules():
    """Load email filtering rules from JSON file"""
    import os

    rules_file = os.path.join(os.path.dirname(__file__), "email_rules.json")
    if os.path.exists(rules_file):
        with open(rules_file, "r") as f:
            return json.load(f)
    return {}


def check_email_rules(email):
    """
    Check email against rules and return action to take
    Returns: dict with 'action', 'reason', 'priority'
    """
    rules = load_email_rules()
    sender = email.get("from", "").lower()
    subject = email.get("subject", "").lower()

    # Rule 1: VIP Senders - Mark as important
    vip_senders = [s.lower() for s in rules.get("vip_senders", [])]
    if sender in vip_senders:
        return {"action": "mark_important", "reason": f'VIP sender: {email.get("from_name", sender)}', "priority": 1}

    # Rule 2: Auto-archive - Recruitment emails from external
    if not sender.endswith("@loreal.com"):
        # Check auto-archive domains
        for domain in rules.get("auto_archive_domains", []):
            if domain in sender:
                return {"action": "archive", "reason": f"Recruitment/spam from {domain}", "priority": 5}

        # Check auto-archive keywords in subject
        for keyword in rules.get("auto_archive_keywords", []):
            if keyword in subject:
                # Verify it's not from a whitelisted partner
                is_whitelisted = any(partner in sender for partner in rules.get("partner_whitelist", []))
                if not is_whitelisted:
                    return {"action": "archive", "reason": f'External recruitment email: "{keyword}"', "priority": 5}

    # Rule 3: Auto-archive declined/cancelled meetings
    for pattern in rules.get("auto_archive_subjects", []):
        if subject.startswith(pattern):
            return {"action": "archive", "reason": f"Cancelled/declined meeting", "priority": 4}

    # Rule 4: System emails requiring action
    if sender in rules.get("system_emails", []):
        if "approu" in subject or "approve" in subject:
            return {"action": "flag", "reason": "Action required: Approval needed", "priority": 2}

    # Rule 5: Partner whitelist - keep but don't prioritize
    for partner in rules.get("partner_whitelist", []):
        if partner in sender:
            return {"action": "keep", "reason": f"Whitelisted partner: {partner}", "priority": 3}

    # Default: keep
    return {"action": "keep", "reason": "No matching rule", "priority": 3}


def process_inbox(limit=100, dry_run=False):
    """
    Process inbox and apply filtering rules
    Returns summary of actions taken
    """
    emails = list_emails(folder="inbox", limit=limit, unread_only=False)

    actions_taken = {"mark_important": [], "archive": [], "flag": [], "keep": []}

    for email in emails:
        # Skip if already read and not important
        if email.get("is_read") and not dry_run:
            continue

        rule_result = check_email_rules(email)
        action = rule_result["action"]

        email_info = {
            "id": email["id"],
            "from": email["from"],
            "from_name": email["from_name"],
            "subject": email["subject"],
            "reason": rule_result["reason"],
            "priority": rule_result["priority"],
        }

        if dry_run:
            actions_taken[action].append(email_info)
        else:
            # Execute action
            if action == "mark_important":
                mark_important(email["id"])
                mark_email(email["id"], True)  # Also mark as read
                actions_taken[action].append(email_info)

            elif action == "archive":
                archive_email(email["id"])
                actions_taken[action].append(email_info)

            elif action == "flag":
                # Just keep track, don't move
                actions_taken[action].append(email_info)

            else:  # keep
                actions_taken[action].append(email_info)

    # Sort by priority
    for action in actions_taken:
        actions_taken[action].sort(key=lambda x: x["priority"])

    return actions_taken


# ============================================================================
# CALENDAR FUNCTIONS
# ============================================================================


def get_local_timezone_offset():
    """
    Get local timezone offset in hours from UTC
    Returns: (offset_hours, timezone_name)
    """
    try:
        # Get timezone offset using date command
        result = subprocess.run(["date", "+%z"], capture_output=True, text=True, check=True)
        offset_str = result.stdout.strip()  # e.g., "+0100" for CET

        # Parse offset: +0100 means +1 hour
        sign = 1 if offset_str[0] == "+" else -1
        hours = int(offset_str[1:3])
        minutes = int(offset_str[3:5])
        offset_hours = sign * (hours + minutes / 60)

        # Get timezone name
        result = subprocess.run(["date", "+%Z"], capture_output=True, text=True, check=True)
        tz_name = result.stdout.strip()

        return offset_hours, tz_name
    except Exception as e:
        # Default to UTC if detection fails
        print(f"Warning: Could not detect timezone, using UTC: {e}", file=sys.stderr)
        return 0, "UTC"


def convert_utc_to_local(utc_time_str):
    """
    Convert UTC time string to local time
    Args:
        utc_time_str: ISO 8601 time string like "2025-11-26T07:30:00.0000000"
    Returns:
        Local time string in same format
    """
    try:
        # Parse UTC time
        utc_dt = datetime.fromisoformat(utc_time_str.replace("Z", "").split(".")[0])

        # Get local offset
        offset_hours, _ = get_local_timezone_offset()

        # Convert to local time
        local_dt = utc_dt + timedelta(hours=offset_hours)

        # Return in same format
        return local_dt.strftime("%Y-%m-%dT%H:%M:%S.0000000")
    except Exception as e:
        print(f"Warning: Could not convert time {utc_time_str}: {e}", file=sys.stderr)
        return utc_time_str


def detect_meeting_collisions(events):
    """
    Detect overlapping meetings in a list of events

    Args:
        events: List of event dictionaries with 'start', 'end', 'id', 'my_response' fields

    Returns:
        List of collision groups, each containing event_ids that overlap
    """
    collisions = []

    # Only check for collisions among accepted/tentative meetings (not declined)
    active_events = [e for e in events if e.get("my_response") not in ["declined", "none"]]

    for i, event1 in enumerate(active_events):
        for event2 in active_events[i + 1 :]:
            # Parse timestamps
            try:
                start1 = datetime.fromisoformat(event1["start"].replace("Z", "").split(".")[0])
                end1 = datetime.fromisoformat(event1["end"].replace("Z", "").split(".")[0])
                start2 = datetime.fromisoformat(event2["start"].replace("Z", "").split(".")[0])
                end2 = datetime.fromisoformat(event2["end"].replace("Z", "").split(".")[0])

                # Check for overlap: events overlap if one starts before the other ends
                if start1 < end2 and start2 < end1:
                    # Found collision - check if already in a collision group
                    found_group = False
                    for collision in collisions:
                        if event1["id"] in collision["event_ids"] or event2["id"] in collision["event_ids"]:
                            collision["event_ids"].add(event1["id"])
                            collision["event_ids"].add(event2["id"])
                            found_group = True
                            break

                    if not found_group:
                        collisions.append({"event_ids": {event1["id"], event2["id"]}})

            except Exception as e:
                print(f"Warning: Could not parse times for collision detection: {e}", file=sys.stderr)
                continue

    # Convert sets to lists for JSON serialization
    for collision in collisions:
        collision["event_ids"] = list(collision["event_ids"])

    return collisions


def list_events(days_ahead=7, days_back=0, limit=50, include_canceled=False, filter_subject=None):
    """
    List calendar events

    Args:
        days_ahead: Number of days in the future to retrieve (default 7)
        days_back: Number of days in the past to retrieve (default 0)
        limit: Maximum number of events to return (default 50)
        include_canceled: Include canceled/declined events (default False)
        filter_subject: Optional regex pattern to filter events by subject (default None)
    """
    if days_back > 0:
        # Query past events only
        start_time = (datetime.utcnow() - timedelta(days=days_back)).isoformat() + "Z"
        end_time = datetime.utcnow().isoformat() + "Z"
    else:
        # Query from start of today (00:00) to end of days_ahead
        # This ensures we see all events for today, including past ones
        now = datetime.utcnow()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0)
        start_time = start_of_today.isoformat() + "Z"
        end_time = (start_of_today + timedelta(days=days_ahead)).isoformat() + "Z"

    # Use calendarView instead of calendar/events to get events across all calendars
    params = {
        "startDateTime": start_time,
        "endDateTime": end_time,
        "$top": limit,
        "$orderby": "start/dateTime DESC" if days_back > 0 else "start/dateTime",
        "$select": "id,subject,start,end,location,organizer,isOnlineMeeting,onlineMeeting,attendees,responseStatus,isCancelled,hasAttachments,attachments",
    }

    result = make_graph_request("GET", "/me/calendarView", params=params)

    events = []
    if result and "value" in result:
        for evt in result.get("value", []):
            # Filter out canceled/declined events unless include_canceled is True
            is_cancelled = evt.get("isCancelled", False)
            my_response = evt.get("responseStatus", {}).get("response", "none")

            if not include_canceled and (is_cancelled or my_response == "declined"):
                continue

            # Get attendees (first 6)
            attendees_list = evt.get("attendees", [])
            attendees_display = []
            for i, att in enumerate(attendees_list[:6]):
                attendees_display.append(
                    {
                        "name": att["emailAddress"].get("name", att["emailAddress"]["address"]),
                        "email": att["emailAddress"]["address"],
                    }
                )

            has_more_attendees = len(attendees_list) > 6
            remaining_count = len(attendees_list) - 6 if has_more_attendees else 0

            # Get attachments (just names)
            attachments_list = evt.get("attachments", [])
            attachment_names = [att.get("name", "Unnamed") for att in attachments_list]

            # Convert UTC times to local timezone
            start_utc = evt["start"]["dateTime"]
            end_utc = evt["end"]["dateTime"]
            start_local = convert_utc_to_local(start_utc)
            end_local = convert_utc_to_local(end_utc)

            # Get local timezone name
            _, local_tz_name = get_local_timezone_offset()

            events.append(
                {
                    "id": evt["id"],
                    "subject": evt["subject"],
                    "start": start_local,
                    "end": end_local,
                    "timezone": local_tz_name,
                    "location": (evt.get("location") or {}).get("displayName", ""),
                    "organizer": evt["organizer"]["emailAddress"]["address"] if evt.get("organizer") else "Unknown",
                    "organizer_name": (
                        evt["organizer"]["emailAddress"].get("name", "") if evt.get("organizer") else "Unknown"
                    ),
                    "is_online_meeting": evt.get("isOnlineMeeting", False),
                    "online_meeting_url": (evt.get("onlineMeeting") or {}).get("joinUrl", ""),
                    "attendees": attendees_display,
                    "more_attendees": remaining_count,
                    "my_response": my_response,
                    "is_cancelled": is_cancelled,
                    "has_attachments": evt.get("hasAttachments", False),
                    "attachments": attachment_names,
                }
            )

    # Apply subject filter if provided
    if filter_subject:
        try:
            pattern = re.compile(filter_subject, re.IGNORECASE)
            events = [e for e in events if pattern.search(e["subject"])]
        except re.error as e:
            print(f"Error: Invalid regex pattern '{filter_subject}': {e}", file=sys.stderr)
            sys.exit(1)

    # Detect meeting collisions
    collisions = detect_meeting_collisions(events)

    # Add collision warnings to events
    for event in events:
        event["has_collision"] = False
        event["collides_with"] = []

        for collision in collisions:
            if event["id"] in collision["event_ids"]:
                event["has_collision"] = True
                # Add info about other colliding events
                for other_id in collision["event_ids"]:
                    if other_id != event["id"]:
                        other_event = next((e for e in events if e["id"] == other_id), None)
                        if other_event:
                            event["collides_with"].append(
                                {
                                    "subject": other_event["subject"],
                                    "start": other_event["start"],
                                    "end": other_event["end"],
                                }
                            )

    return events


def get_event(event_id):
    """Get event details"""
    result = make_graph_request("GET", f"/me/calendar/events/{event_id}")

    return {
        "id": result["id"],
        "subject": result["subject"],
        "start": result["start"]["dateTime"],
        "end": result["end"]["dateTime"],
        "timezone": result["start"]["timeZone"],
        "location": (result.get("location") or {}).get("displayName", ""),
        "body": result["body"]["content"],
        "body_type": result["body"]["contentType"],
        "organizer": result["organizer"]["emailAddress"]["address"] if result.get("organizer") else "Unknown",
        "attendees": [
            {
                "email": att["emailAddress"]["address"],
                "name": att["emailAddress"]["name"],
                "status": att["status"]["response"],
            }
            for att in (result.get("attendees") or [])
        ],
        "is_online_meeting": result.get("isOnlineMeeting", False),
        "online_meeting_url": (result.get("onlineMeeting") or {}).get("joinUrl", ""),
    }


def create_event(subject, start_time, end_time, attendees=None, location=None, body=None, timezone="UTC"):
    """Create calendar event"""
    event_data = {
        "subject": subject,
        "start": {"dateTime": start_time, "timeZone": timezone},
        "end": {"dateTime": end_time, "timeZone": timezone},
    }

    if attendees:
        event_data["attendees"] = [{"emailAddress": {"address": addr}, "type": "required"} for addr in attendees]

    if location:
        event_data["location"] = {"displayName": location}

    if body:
        event_data["body"] = {"contentType": "HTML", "content": body}

    result = make_graph_request("POST", "/me/calendar/events", data=event_data)
    return result["id"]


def update_event(event_id, subject=None, start_time=None, end_time=None, location=None, body=None, timezone="UTC"):
    """Update calendar event"""
    update_data = {}

    if subject:
        update_data["subject"] = subject

    if start_time:
        update_data["start"] = {"dateTime": start_time, "timeZone": timezone}

    if end_time:
        update_data["end"] = {"dateTime": end_time, "timeZone": timezone}

    if location is not None:
        update_data["location"] = {"displayName": location}

    if body:
        update_data["body"] = {"contentType": "HTML", "content": body}

    make_graph_request("PATCH", f"/me/calendar/events/{event_id}", data=update_data)
    return True


def delete_event(event_id):
    """Delete calendar event"""
    make_graph_request("DELETE", f"/me/calendar/events/{event_id}")
    return True


def respond_to_event(event_id, response_type, comment=None, send_response=True):
    """
    Respond to a calendar event invitation

    Args:
        event_id: The event ID
        response_type: "accept", "decline", or "tentative"
        comment: Optional message to include with the response
        send_response: Whether to send response email to organizer (default True)

    Returns:
        True if successful
    """
    response_data = {"sendResponse": send_response}

    if comment:
        response_data["comment"] = comment

    if response_type.lower() == "accept":
        make_graph_request("POST", f"/me/events/{event_id}/accept", data=response_data)
    elif response_type.lower() == "decline":
        make_graph_request("POST", f"/me/events/{event_id}/decline", data=response_data)
    elif response_type.lower() == "tentative":
        make_graph_request("POST", f"/me/events/{event_id}/tentativelyAccept", data=response_data)
    else:
        raise ValueError(f"Invalid response type: {response_type}. Must be 'accept', 'decline', or 'tentative'")

    return True


def download_event_attachment(event_id, attachment_id, output_dir=None):
    """Download an attachment from a calendar event"""
    import os
    from pathlib import Path
    import base64

    # Get attachment details
    result = make_graph_request("GET", f"/me/events/{event_id}/attachments/{attachment_id}")

    if not result:
        raise Exception("Failed to retrieve attachment")

    # Get attachment name and content
    file_name = result.get("name", "attachment")
    content_bytes = result.get("contentBytes")

    if not content_bytes:
        raise Exception("No content found in attachment")

    # Determine output directory
    if not output_dir:
        output_dir = os.path.expanduser("~/Downloads")

    output_path = Path(output_dir) / file_name

    # Decode base64 content and write to file
    file_content = base64.b64decode(content_bytes)

    with open(output_path, "wb") as f:
        f.write(file_content)

    return str(output_path)


# ============================================================================
# CLI INTERFACE
# ============================================================================


def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Office 365 Manager - Email and Calendar Management")
        print("\nUsage: o365_manager.py <command> [options]")
        print("\nEmail Commands:")
        print("  list-emails [--folder inbox] [--limit 10] [--unread] [--search 'query']")
        print("  read-email <message_id>")
        print(
            "  send-email --to addr1,addr2 --subject 'Subject' --body 'Body' [--cc addr3] [--body-type HTML|Text] [--attachments file1,file2]"
        )
        print(
            "  create-draft --to addr1,addr2 --subject 'Subject' --body 'Body' [--cc addr3] [--body-type HTML|Text] [--attachments file1,file2]"
        )
        print("  reply-email <message_id> --comment 'Reply text'")
        print("  mark-read <message_id>")
        print("  mark-unread <message_id>")
        print("  delete-email <message_id>")
        print("  move-email <message_id> --folder 'FolderName'")
        print("  archive-email <message_id>")
        print("  list-folders")
        print("  search-emails --query 'search term' [--limit 20]")
        print("\nCalendar Commands:")
        print(
            "  list-events [--days 7] [--days-back 0] [--limit 50] [--include-canceled | --all | --full] [--filter-subject 'regex']"
        )
        print("  get-event <event_id>")
        print(
            "  create-event --subject 'Meeting' --start '2025-11-12T14:00:00' --end '2025-11-12T15:00:00' [--attendees addr1,addr2] [--location 'Room'] [--body 'Description']"
        )
        print("  update-event <event_id> [--subject 'New subject'] [--start '...'] [--end '...'] [--location '...']")
        print("  delete-event <event_id>")
        print("  respond-event <event_id> --response accept|decline|tentative [--comment 'Message'] [--no-send]")
        print("  download-event-attachment <event_id> <attachment_id> [--output-dir ~/Downloads]")
        print("\nInbox Management Commands:")
        print("  process-inbox [--limit 100] [--dry-run] - Process inbox with filtering rules and return summary")
        print("  mark-important <message_id> - Mark email as important/VIP")
        print("\nOther Commands:")
        print("  auth - Force re-authentication")
        sys.exit(1)

    command = sys.argv[1]

    try:
        # Parse arguments
        args = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i].startswith("--"):
                key = sys.argv[i][2:]
                if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                    args[key] = sys.argv[i + 1]
                    i += 2
                else:
                    args[key] = True
                    i += 1
            else:
                args["_positional"] = args.get("_positional", [])
                args["_positional"].append(sys.argv[i])
                i += 1

        # Execute command
        if command == "auth":
            # Force re-authentication
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
            get_access_token()
            print("Authentication successful!")

        elif command == "list-emails":
            folder = args.get("folder", "inbox")
            limit = int(args.get("limit", 10))
            unread_only = "unread" in args
            search = args.get("search")
            emails = list_emails(folder, limit, unread_only, search)
            print_json(emails)

        elif command == "read-email":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            email = read_email(message_id)
            print_json(email)

        elif command == "send-email":
            to = args.get("to", "").split(",")
            subject = args.get("subject", "")
            body = args.get("body", "")
            cc = args.get("cc", "").split(",") if args.get("cc") else None
            body_type = args.get("body-type", "HTML")
            attachments = args.get("attachments", "").split(",") if args.get("attachments") else None

            if not to or not subject:
                print("Error: --to and --subject required")
                sys.exit(1)

            send_email(to, subject, body, cc, body_type, attachments)
            if attachments:
                print(f"Email sent successfully with {len(attachments)} attachment(s)!")
            else:
                print("Email sent successfully!")

        elif command == "create-draft":
            to = args.get("to", "").split(",")
            subject = args.get("subject", "")
            body = args.get("body", "")
            cc = args.get("cc", "").split(",") if args.get("cc") else None
            body_type = args.get("body-type", "HTML")
            attachments = args.get("attachments", "").split(",") if args.get("attachments") else None

            if not to or not subject:
                print("Error: --to and --subject required")
                sys.exit(1)

            result = create_draft(to, subject, body, cc, body_type, attachments)
            draft_id = result.get("id", "")
            if attachments:
                print(f"Draft created successfully with {len(attachments)} attachment(s)! Draft ID: {draft_id}")
            else:
                print(f"Draft created successfully! Draft ID: {draft_id}")

        elif command == "reply-email":
            message_id = args.get("_positional", [None])[0]
            comment = args.get("comment", "")

            if not message_id or not comment:
                print("Error: message_id and --comment required")
                sys.exit(1)

            reply_to_email(message_id, comment)
            print("Reply sent successfully!")

        elif command == "mark-read":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            mark_email(message_id, True)
            print("Email marked as read!")

        elif command == "mark-unread":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            mark_email(message_id, False)
            print("Email marked as unread!")

        elif command == "delete-email":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            delete_email(message_id)
            print("Email deleted!")

        elif command == "move-email":
            message_id = args.get("_positional", [None])[0]
            folder = args.get("folder", "")

            if not message_id or not folder:
                print("Error: message_id and --folder required")
                sys.exit(1)

            move_email(message_id, folder)
            print(f"Email moved to '{folder}' folder!")

        elif command == "archive-email":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            archive_email(message_id)
            print("Email archived!")

        elif command == "list-folders":
            folders = get_mail_folders()
            print("Available mail folders:")
            for folder_name in sorted(folders.keys()):
                print(f"  - {folder_name}")

        elif command == "mark-important":
            message_id = args.get("_positional", [None])[0]
            if not message_id:
                print("Error: message_id required")
                sys.exit(1)
            mark_important(message_id)
            print("Email marked as important!")

        elif command == "process-inbox":
            limit = int(args.get("limit", 100))
            dry_run = "dry-run" in args

            print(f"Processing inbox (limit: {limit}, dry_run: {dry_run})...")
            results = process_inbox(limit=limit, dry_run=dry_run)

            # Print summary
            print("\n" + "=" * 80)
            print("INBOX PROCESSING SUMMARY")
            print("=" * 80)

            if results["mark_important"]:
                print(f"\n🌟 MARKED AS IMPORTANT ({len(results['mark_important'])} emails):")
                for email in results["mark_important"]:
                    print(f"  ✓ {email['from_name']} - {email['subject']}")
                    print(f"    Reason: {email['reason']}")

            if results["archive"]:
                print(f"\n📦 ARCHIVED ({len(results['archive'])} emails):")
                for email in results["archive"]:
                    print(f"  ✓ {email['from_name']} ({email['from']}) - {email['subject']}")
                    print(f"    Reason: {email['reason']}")

            if results["flag"]:
                print(f"\n🚩 FLAGGED FOR ACTION ({len(results['flag'])} emails):")
                for email in results["flag"]:
                    print(f"  ✓ {email['from_name']} - {email['subject']}")
                    print(f"    Reason: {email['reason']}")

            if results["keep"]:
                print(f"\n📧 KEPT IN INBOX ({len(results['keep'])} emails):")
                for email in results["keep"][:10]:  # Show first 10
                    print(f"  • {email['from_name']} - {email['subject']}")
                if len(results["keep"]) > 10:
                    print(f"  ... and {len(results['keep']) - 10} more")

            # Overall summary
            total = sum(len(results[key]) for key in results)
            print(f"\n" + "=" * 80)
            print(f"Total emails processed: {total}")
            print(f"  - VIP/Important: {len(results['mark_important'])}")
            print(f"  - Archived: {len(results['archive'])}")
            print(f"  - Flagged: {len(results['flag'])}")
            print(f"  - Kept: {len(results['keep'])}")
            print("=" * 80)

            if dry_run:
                print("\n⚠️  DRY RUN MODE - No actual changes were made")
                print("Run without --dry-run to apply these actions")

        elif command == "search-emails":
            query = args.get("query", "")
            limit = int(args.get("limit", 20))

            if not query:
                print("Error: --query required")
                sys.exit(1)

            emails = search_emails(query, limit)
            print_json(emails)

        elif command == "list-events":
            days = int(args.get("days", 7))
            days_back = int(args.get("days-back", 0))
            limit = int(args.get("limit", 50))
            include_canceled = "include-canceled" in args or "all" in args or "full" in args
            filter_subject = args.get("filter-subject")
            events = list_events(days, days_back, limit, include_canceled, filter_subject)
            print_json(events)

        elif command == "get-event":
            event_id = args.get("_positional", [None])[0]
            if not event_id:
                print("Error: event_id required")
                sys.exit(1)
            event = get_event(event_id)
            print_json(event)

        elif command == "create-event":
            subject = args.get("subject", "")
            start = args.get("start", "")
            end = args.get("end", "")
            attendees = args.get("attendees", "").split(",") if args.get("attendees") else None
            location = args.get("location")
            body = args.get("body")
            timezone = args.get("timezone", "Europe/Paris")

            if not subject or not start or not end:
                print("Error: --subject, --start, and --end required")
                sys.exit(1)

            event_id = create_event(subject, start, end, attendees, location, body, timezone)
            print(f"Event created successfully! ID: {event_id}")

        elif command == "update-event":
            event_id = args.get("_positional", [None])[0]
            if not event_id:
                print("Error: event_id required")
                sys.exit(1)

            subject = args.get("subject")
            start = args.get("start")
            end = args.get("end")
            location = args.get("location")
            body = args.get("body")
            timezone = args.get("timezone", "Europe/Paris")

            update_event(event_id, subject, start, end, location, body, timezone)
            print("Event updated successfully!")

        elif command == "delete-event":
            event_id = args.get("_positional", [None])[0]
            if not event_id:
                print("Error: event_id required")
                sys.exit(1)
            delete_event(event_id)
            print("Event deleted!")

        elif command == "respond-event":
            event_id = args.get("_positional", [None])[0]
            response_type = args.get("response", "")

            if not event_id or not response_type:
                print("Error: event_id and --response required")
                sys.exit(1)

            comment = args.get("comment")
            send_response = "no-send" not in args

            respond_to_event(event_id, response_type, comment, send_response)
            action = response_type.capitalize() + "ed" if response_type != "tentative" else "Marked as tentative"
            print(f"{action} event successfully!")

        elif command == "download-event-attachment":
            positional = args.get("_positional", [])
            if len(positional) < 2:
                print("Error: event_id and attachment_id required")
                sys.exit(1)
            event_id = positional[0]
            attachment_id = positional[1]
            output_dir = args.get("output-dir")

            file_path = download_event_attachment(event_id, attachment_id, output_dir)
            print(f"Attachment downloaded to: {file_path}")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        import traceback

        print(f"Error: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
