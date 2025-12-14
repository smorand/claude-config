#!/usr/bin/env python3
"""
Search and list Google Keep notes
Provides search functionality with pinned notes first
"""

import argparse
import json
from auth import get_keep_client


def search_notes(keep, query="", include_archived=False, include_trashed=False):
    """
    Search notes in Google Keep.

    Args:
        keep: Authenticated Keep client
        query: Search query string
        include_archived: Include archived notes
        include_trashed: Include trashed notes

    Returns:
        List of notes sorted by pinned status (pinned first)
    """
    # Sync with server
    keep.sync()

    # Get all notes
    all_notes = keep.all()

    # Filter notes
    filtered_notes = []
    for note in all_notes:
        # Skip trashed notes unless requested
        if note.trashed and not include_trashed:
            continue

        # Skip archived notes unless requested
        if note.archived and not include_archived:
            continue

        # Apply query filter if provided
        if query:
            query_lower = query.lower()
            title_match = query_lower in note.title.lower()
            text_match = query_lower in note.text.lower()

            if not (title_match or text_match):
                continue

        filtered_notes.append(note)

    # Sort by pinned status (pinned first), then by modification time
    sorted_notes = sorted(filtered_notes, key=lambda n: (not n.pinned, n.timestamps.updated), reverse=True)

    return sorted_notes


def format_note_summary(note):
    """Format note as summary dict."""
    return {
        "id": note.id,
        "title": note.title,
        "text": note.text[:200] + "..." if len(note.text) > 200 else note.text,
        "pinned": note.pinned,
        "archived": note.archived,
        "trashed": note.trashed,
        "color": note.color.name if note.color else None,
        "labels": [label.name for label in note.labels.all()],
        "created": note.timestamps.created.isoformat(),
        "updated": note.timestamps.updated.isoformat(),
        "type": "list" if hasattr(note, "items") and note.items else "note",
    }


def format_note_full(note):
    """Format note with full details."""
    data = format_note_summary(note)

    # Add list items if it's a list note
    if hasattr(note, "items") and note.items:
        data["items"] = [
            {"text": item.text, "checked": item.checked, "sort": item.sort}
            for item in sorted(note.items, key=lambda i: i.sort)
        ]

    return data


def main():
    parser = argparse.ArgumentParser(description="Search Google Keep notes")
    parser.add_argument("--query", default="", help="Search query (searches in title and text)")
    parser.add_argument("--include-archived", action="store_true", help="Include archived notes")
    parser.add_argument("--include-trashed", action="store_true", help="Include trashed notes")
    parser.add_argument("--full", action="store_true", help="Show full note details including list items")
    parser.add_argument("--max-results", type=int, default=50, help="Maximum number of results")

    args = parser.parse_args()

    try:
        keep = get_keep_client()

        notes = search_notes(
            keep, query=args.query, include_archived=args.include_archived, include_trashed=args.include_trashed
        )

        # Limit results
        notes = notes[: args.max_results]

        if not notes:
            print("No notes found")
            return

        print(f"Found {len(notes)} note(s)\n")

        # Format output
        if args.full:
            results = [format_note_full(note) for note in notes]
            print(json.dumps(results, indent=2))
        else:
            for i, note in enumerate(notes, 1):
                pin_indicator = "📌 " if note.pinned else "   "
                archived_indicator = "[ARCHIVED] " if note.archived else ""
                title = note.title or "(No title)"

                print(f"{i}. {pin_indicator}{archived_indicator}{title}")
                print(f"   ID: {note.id}")
                if note.text:
                    preview = note.text[:100] + "..." if len(note.text) > 100 else note.text
                    print(f"   {preview}")
                print()

    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("\nTo set up authentication, run:")
        print("  cd ~/.claude/skills/note-manager/scripts")
        print("  ./run.sh auth")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
