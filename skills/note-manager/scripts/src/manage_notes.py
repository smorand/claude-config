#!/usr/bin/env python3
"""
Manage Google Keep notes
Create, update, archive, pin, delete, and duplicate notes
"""

import argparse
import json
from auth import get_keep_client
import gkeepapi


def get_note_by_id(keep, note_id):
    """Get a note by its ID."""
    keep.sync()
    note = keep.get(note_id)
    if not note:
        raise ValueError(f"Note with ID {note_id} not found")
    return note


def create_text_note(keep, title, text, pinned=False, color=None):
    """
    Create a text note.

    Args:
        keep: Authenticated Keep client
        title: Note title
        text: Note content
        pinned: Whether to pin the note
        color: Note color (optional)

    Returns:
        Created note
    """
    note = keep.createNote(title, text)

    if pinned:
        note.pinned = True

    if color:
        try:
            note.color = getattr(gkeepapi.node.ColorValue, color.upper())
        except AttributeError:
            print(f"Warning: Unknown color '{color}', using default")

    keep.sync()
    return note


def create_list_note(keep, title, items, pinned=False, color=None):
    """
    Create a list note.

    Args:
        keep: Authenticated Keep client
        title: Note title
        items: List of item texts or dicts with 'text' and optional 'checked'
        pinned: Whether to pin the note
        color: Note color (optional)

    Returns:
        Created note
    """
    note = keep.createList(title)

    # Add items
    for item in items:
        if isinstance(item, dict):
            text = item.get("text", "")
            checked = item.get("checked", False)
        else:
            text = str(item)
            checked = False

        list_item = note.add(text, checked)

    if pinned:
        note.pinned = True

    if color:
        try:
            note.color = getattr(gkeepapi.node.ColorValue, color.upper())
        except AttributeError:
            print(f"Warning: Unknown color '{color}', using default")

    keep.sync()
    return note


def update_note(keep, note_id, title=None, text=None, items=None):
    """
    Update an existing note.

    Args:
        keep: Authenticated Keep client
        note_id: ID of the note to update
        title: New title (optional)
        text: New text content (optional, for text notes)
        items: New list items (optional, for list notes)

    Returns:
        Updated note
    """
    note = get_note_by_id(keep, note_id)

    if title is not None:
        note.title = title

    # Check if it's a list note
    if hasattr(note, "items") and note.items:
        if items is not None:
            # Clear existing items
            for item in list(note.items):
                item.delete()

            # Add new items
            for item_data in items:
                if isinstance(item_data, dict):
                    text = item_data.get("text", "")
                    checked = item_data.get("checked", False)
                else:
                    text = str(item_data)
                    checked = False

                note.add(text, checked)
    else:
        # Text note
        if text is not None:
            note.text = text

    keep.sync()
    return note


def archive_note(keep, note_id, archived=True):
    """Archive or unarchive a note."""
    note = get_note_by_id(keep, note_id)
    note.archived = archived
    keep.sync()
    return note


def pin_note(keep, note_id, pinned=True):
    """Pin or unpin a note."""
    note = get_note_by_id(keep, note_id)
    note.pinned = pinned
    keep.sync()
    return note


def delete_note(keep, note_id):
    """Delete (trash) a note."""
    note = get_note_by_id(keep, note_id)
    note.delete()
    keep.sync()
    return note


def duplicate_note(keep, note_id, new_title=None):
    """
    Duplicate a note with a new title.

    Args:
        keep: Authenticated Keep client
        note_id: ID of the note to duplicate
        new_title: Title for the new note (defaults to "Copy of [original title]")

    Returns:
        New duplicated note
    """
    original = get_note_by_id(keep, note_id)

    # Determine new title
    if new_title is None:
        new_title = f"Copy of {original.title}"

    # Check if it's a list note
    if hasattr(original, "items") and original.items:
        # Duplicate as list
        items = [{"text": item.text, "checked": item.checked} for item in sorted(original.items, key=lambda i: i.sort)]
        new_note = create_list_note(
            keep, new_title, items, pinned=original.pinned, color=original.color.name if original.color else None
        )
    else:
        # Duplicate as text note
        new_note = create_text_note(
            keep,
            new_title,
            original.text,
            pinned=original.pinned,
            color=original.color.name if original.color else None,
        )

    # Copy labels
    for label in original.labels.all():
        new_note.labels.add(label)

    keep.sync()
    return new_note


def main():
    parser = argparse.ArgumentParser(description="Manage Google Keep notes")
    parser.add_argument(
        "--action",
        required=True,
        choices=[
            "create-text",
            "create-list",
            "update",
            "archive",
            "unarchive",
            "pin",
            "unpin",
            "delete",
            "duplicate",
            "get",
        ],
        help="Action to perform",
    )
    parser.add_argument("--note-id", help="Note ID (required for update/archive/pin/delete/duplicate/get)")
    parser.add_argument("--title", help="Note title")
    parser.add_argument("--text", help="Note text (for text notes)")
    parser.add_argument("--items", help="List items as JSON array (for list notes)")
    parser.add_argument("--pinned", action="store_true", help="Pin the note")
    parser.add_argument("--color", help="Note color (e.g., red, blue, green)")
    parser.add_argument("--new-title", help="New title for duplicated note")

    args = parser.parse_args()

    try:
        keep = get_keep_client()

        if args.action == "create-text":
            if not args.title:
                print("Error: --title is required for creating a text note")
                return

            note = create_text_note(keep, args.title, args.text or "", pinned=args.pinned, color=args.color)
            print(f"✓ Text note created: {note.title}")
            print(f"  ID: {note.id}")

        elif args.action == "create-list":
            if not args.title:
                print("Error: --title is required for creating a list note")
                return

            items = []
            if args.items:
                items = json.loads(args.items)

            note = create_list_note(keep, args.title, items, pinned=args.pinned, color=args.color)
            print(f"✓ List note created: {note.title}")
            print(f"  ID: {note.id}")
            print(f"  Items: {len(items)}")

        elif args.action == "update":
            if not args.note_id:
                print("Error: --note-id is required for updating a note")
                return

            items = None
            if args.items:
                items = json.loads(args.items)

            note = update_note(keep, args.note_id, args.title, args.text, items)
            print(f"✓ Note updated: {note.title}")

        elif args.action == "archive":
            if not args.note_id:
                print("Error: --note-id is required for archiving a note")
                return

            note = archive_note(keep, args.note_id, archived=True)
            print(f"✓ Note archived: {note.title}")

        elif args.action == "unarchive":
            if not args.note_id:
                print("Error: --note-id is required for unarchiving a note")
                return

            note = archive_note(keep, args.note_id, archived=False)
            print(f"✓ Note unarchived: {note.title}")

        elif args.action == "pin":
            if not args.note_id:
                print("Error: --note-id is required for pinning a note")
                return

            note = pin_note(keep, args.note_id, pinned=True)
            print(f"✓ Note pinned: {note.title}")

        elif args.action == "unpin":
            if not args.note_id:
                print("Error: --note-id is required for unpinning a note")
                return

            note = pin_note(keep, args.note_id, pinned=False)
            print(f"✓ Note unpinned: {note.title}")

        elif args.action == "delete":
            if not args.note_id:
                print("Error: --note-id is required for deleting a note")
                return

            note = delete_note(keep, args.note_id)
            print(f"✓ Note deleted: {note.title}")

        elif args.action == "duplicate":
            if not args.note_id:
                print("Error: --note-id is required for duplicating a note")
                return

            note = duplicate_note(keep, args.note_id, args.new_title)
            print(f"✓ Note duplicated: {note.title}")
            print(f"  New ID: {note.id}")

        elif args.action == "get":
            if not args.note_id:
                print("Error: --note-id is required for getting a note")
                return

            note = get_note_by_id(keep, args.note_id)

            # Format full note data
            data = {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "pinned": note.pinned,
                "archived": note.archived,
                "trashed": note.trashed,
                "color": note.color.name if note.color else None,
                "labels": [label.name for label in note.labels.all()],
                "created": note.timestamps.created.isoformat(),
                "updated": note.timestamps.updated.isoformat(),
            }

            # Add list items if it's a list note
            if hasattr(note, "items") and note.items:
                data["type"] = "list"
                data["items"] = [
                    {"text": item.text, "checked": item.checked, "sort": item.sort}
                    for item in sorted(note.items, key=lambda i: i.sort)
                ]
            else:
                data["type"] = "text"

            print(json.dumps(data, indent=2))

    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("\nTo set up authentication, run:")
        print("  cd ~/.claude/skills/note-manager/scripts")
        print("  ./run.sh auth")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
