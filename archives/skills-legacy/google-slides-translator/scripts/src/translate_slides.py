#!/usr/bin/env python3
"""
Google Slides Translator
Translates Google Slides presentations while preserving formatting
Based on the godri slides_service.py implementation
"""

import os
import sys
from pathlib import Path
from typing import Optional, List

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.cloud import translate_v2 as translate
except ImportError:
    print("❌ Error: Required packages are not installed.", file=sys.stderr)
    print("Please ensure the virtual environment is properly set up.", file=sys.stderr)
    sys.exit(1)


SCOPES = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/cloud-translation"]


class SlidesTranslator:
    """Translate Google Slides while preserving formatting."""

    def __init__(self):
        self.creds = None
        self.slides_service = None
        self.translate_client = None

    def authenticate(self):
        """Authenticate with Google APIs."""
        # Store credentials in ~/.claude/credentials/
        token_path = Path.home() / ".claude" / "credentials" / "google_token.json"
        credentials_path = Path.home() / ".claude" / "credentials" / "google_credentials.json"

        # Load existing credentials
        if token_path.exists():
            self.creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not credentials_path.exists():
                    print("\n⚠️  Google OAuth credentials not found", file=sys.stderr)
                    print(f"\nTo set up authentication:", file=sys.stderr)
                    print(f"1. Go to Google Cloud Console: https://console.cloud.google.com/", file=sys.stderr)
                    print(f"2. Enable Google Slides API and Cloud Translation API", file=sys.stderr)
                    print(f"3. Create OAuth 2.0 Client ID (Desktop application)", file=sys.stderr)
                    print(f"4. Download credentials.json", file=sys.stderr)
                    print(f"5. Save to: {credentials_path}", file=sys.stderr)
                    print(f"\nRun this command to create the directory:", file=sys.stderr)
                    print(f"  mkdir -p {credentials_path.parent}", file=sys.stderr)
                    sys.exit(1)

                print("\n🔐 Starting OAuth authentication flow...")
                print("📝 A browser window will open for authentication")
                print("✓ Grant access to Google Slides and Cloud Translation")
                flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
                self.creds = flow.run_local_server(port=0)
                print("✅ Authentication successful!")

            # Save credentials
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_text(self.creds.to_json())

        # Initialize services
        self.slides_service = build("slides", "v1", credentials=self.creds)
        self.translate_client = translate.Client(credentials=self.creds)

        print("✅ Authenticated successfully")

    def get_presentation(self, presentation_id: str):
        """Get presentation content."""
        return self.slides_service.presentations().get(presentationId=presentation_id).execute()

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language with auto-detect source."""
        if not text or not text.strip():
            return text

        result = self.translate_client.translate(text, target_language=target_language, format_="text")
        return result["translatedText"]

    def extract_element_text(self, presentation, element_id: str) -> str:
        """Extract text content from a presentation element."""
        for slide in presentation.get("slides", []):
            for element in slide.get("pageElements", []):
                if element["objectId"] == element_id and "shape" in element:
                    shape = element["shape"]
                    if "text" in shape:
                        text_content = ""
                        for text_element in shape["text"].get("textElements", []):
                            if "textRun" in text_element:
                                text_content += text_element["textRun"].get("content", "")
                        return text_content
        return ""

    def update_text_preserving_format(
        self, presentation_id: str, slide_id: str, element_id: str, current_text: str, new_text: str
    ):
        """Update text content while preserving formatting using replaceAllText."""
        requests = [
            {
                "replaceAllText": {
                    "containsText": {"text": current_text, "matchCase": True},
                    "replaceText": new_text,
                    "pageObjectIds": [slide_id],
                }
            }
        ]

        return (
            self.slides_service.presentations()
            .batchUpdate(presentationId=presentation_id, body={"requests": requests})
            .execute()
        )

    def parse_slide_range(self, slides_str: str, total_slides: int) -> List[int]:
        """
        Parse slide range string into list of 0-based slide indices.

        Examples:
        - "1-3" -> [0, 1, 2]
        - "1,3,5" -> [0, 2, 4]
        - "2-4,6" -> [1, 2, 3, 5]
        - "all" -> [0, 1, 2, ..., total_slides-1]
        """
        if slides_str.lower() == "all":
            return list(range(total_slides))

        indices = set()
        for part in slides_str.split(","):
            part = part.strip()
            if "-" in part:
                # Range like "2-4"
                start, end = map(int, part.split("-"))
                # Convert to 0-based and validate
                start_idx = max(0, start - 1)
                end_idx = min(total_slides - 1, end - 1)
                indices.update(range(start_idx, end_idx + 1))
            else:
                # Single slide like "3"
                slide_num = int(part)
                slide_idx = slide_num - 1  # Convert to 0-based
                if 0 <= slide_idx < total_slides:
                    indices.add(slide_idx)

        return sorted(list(indices))

    def translate_slides(self, presentation_id: str, slides: str, target_language: str):
        """
        Translate text content in slides.

        Args:
            presentation_id: Presentation ID
            slides: Slide range to translate (e.g., '1-3', '2', '1,3,5', 'all')
            target_language: Target language code (auto-detects source language)
        """
        print(f"📊 Translating slides in presentation: {presentation_id}")
        print(f"🌍 Target language: {target_language}")
        print(f"📄 Slide range: {slides}")

        # Get presentation
        presentation = self.get_presentation(presentation_id)
        presentation_title = presentation.get("title", "Untitled")
        total_slides = len(presentation.get("slides", []))

        print(f"📝 Presentation: {presentation_title}")
        print(f"📊 Total slides: {total_slides}")

        # Parse slide range
        slide_indices = self.parse_slide_range(slides, total_slides)

        if not slide_indices:
            print(f"⚠️  No valid slides found for range: {slides}")
            return

        print(f"🎯 Translating {len(slide_indices)} slide(s): {[i+1 for i in slide_indices]}")

        translated_count = 0
        total_translated_elements = 0

        for slide_index in slide_indices:
            slide = presentation["slides"][slide_index]
            slide_id = slide["objectId"]
            slide_number = slide_index + 1
            slide_translated_elements = 0

            print(f"\n🔄 Processing slide {slide_number}...")

            # Process all text elements in the slide
            for element in slide.get("pageElements", []):
                if "shape" in element and "text" in element["shape"]:
                    element_id = element["objectId"]

                    # Extract current text
                    current_text = self.extract_element_text(presentation, element_id)

                    if current_text and current_text.strip():
                        try:
                            # Translate the text
                            translated_text = self.translate_text(current_text, target_language)

                            # Update element with translated text while preserving formatting
                            self.update_text_preserving_format(
                                presentation_id, slide_id, element_id, current_text, translated_text
                            )
                            slide_translated_elements += 1
                            print(f"  ✅ Translated element {element_id[:8]}...")

                        except Exception as e:
                            print(f"  ⚠️  Failed to translate element {element_id}: {e}", file=sys.stderr)

            if slide_translated_elements > 0:
                translated_count += 1
                total_translated_elements += slide_translated_elements
                print(f"  📊 Slide {slide_number}: {slide_translated_elements} elements translated")

        print(f"\n✅ Translation complete!")
        print(f"📊 Slides translated: {translated_count}/{len(slide_indices)}")
        print(f"📝 Total text elements translated: {total_translated_elements}")


def print_usage():
    """Print usage information."""
    print("Usage: python translate_slides.py <presentation_id> <slides> <target_language>")
    print()
    print("Arguments:")
    print("  presentation_id   Google Slides presentation ID")
    print("  slides            Slide range: 'all', '1-5', '2', '1,3,5', '2-4,6-8'")
    print("  target_language   Target language code (e.g., 'fr', 'es', 'de')")
    print()
    print("Examples:")
    print("  # Translate all slides to French")
    print("  python translate_slides.py 1abc123... all fr")
    print()
    print("  # Translate slides 10 to 15 to French")
    print("  python translate_slides.py 1abc123... 10-15 fr")
    print()
    print("  # Translate specific slides to Spanish")
    print("  python translate_slides.py 1abc123... 1,5,10 es")
    print()
    print("Supported language codes:")
    print("  fr (French), es (Spanish), de (German), it (Italian),")
    print("  pt (Portuguese), ja (Japanese), zh (Chinese), ko (Korean), etc.")
    print()
    print("Note: Source language is auto-detected")


def main():
    """Main entry point."""
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    presentation_id = sys.argv[1]
    slides = sys.argv[2]
    target_language = sys.argv[3]

    try:
        # Initialize translator
        translator = SlidesTranslator()
        translator.authenticate()

        # Translate slides
        translator.translate_slides(presentation_id=presentation_id, slides=slides, target_language=target_language)

    except KeyboardInterrupt:
        print("\n⚠️  Translation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
