#!/usr/bin/env python3
"""
Extract text and key information from CV files (PDF, DOCX, etc.)
"""

import sys
import os
from pathlib import Path
from PyPDF2 import PdfReader
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF text: {e}", file=sys.stderr)
        return ""


def extract_docx_text(file_id: str, creds: Credentials) -> str:
    """Extract text from a Google Docs file."""
    try:
        docs_service = build("docs", "v1", credentials=creds)
        document = docs_service.documents().get(documentId=file_id).execute()

        text = ""
        for element in document.get("body", {}).get("content", []):
            if "paragraph" in element:
                for text_run in element["paragraph"].get("elements", []):
                    if "textRun" in text_run:
                        text += text_run["textRun"].get("content", "")

        return text.strip()
    except Exception as e:
        print(f"Error extracting Google Docs text: {e}", file=sys.stderr)
        return ""


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_cv.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Determine file type and extract text
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".pdf":
        text = extract_pdf_text(file_path)
    else:
        print(f"Unsupported file format: {file_ext}", file=sys.stderr)
        print("Supported formats: .pdf", file=sys.stderr)
        sys.exit(1)

    if text:
        print(text)
    else:
        print("No text extracted from file", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
