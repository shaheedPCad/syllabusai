"""
Debug script to extract and display all text from a PDF file.
This helps verify what pypdf is actually extracting from the PDF.
"""

from pypdf import PdfReader
import os

def debug_pdf_extraction(pdf_path):
    """Extract and print all text from a PDF file with detailed information."""

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        return

    print("=" * 80)
    print(f"PDF DEBUG: {pdf_path}")
    print("=" * 80)
    print()

    # Open and read PDF
    reader = PdfReader(pdf_path)

    # Print basic PDF info
    print(f"Number of pages: {len(reader.pages)}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    print()
    print("=" * 80)
    print()

    # Extract text from each page
    full_text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        full_text += page_text

        print(f"PAGE {page_num + 1}")
        print("-" * 80)
        print(page_text)
        print("-" * 80)
        print(f"[Page {page_num + 1} character count: {len(page_text)}]")
        print()

    # Print summary
    print("=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total characters extracted: {len(full_text)}")
    print(f"Total lines: {full_text.count(chr(10)) + 1}")
    print()

    # Print full concatenated text
    print("=" * 80)
    print("FULL CONCATENATED TEXT")
    print("=" * 80)
    print(full_text)
    print("=" * 80)
    print()

    # Search for common contact-related keywords
    print("=" * 80)
    print("KEYWORD SEARCH (Contact Information)")
    print("=" * 80)
    keywords = ["email", "phone", "contact", "@", "tel", "address", "mail"]

    for keyword in keywords:
        count = full_text.lower().count(keyword.lower())
        if count > 0:
            print(f"'{keyword}': Found {count} occurrence(s)")

            # Show context around keyword
            lower_text = full_text.lower()
            index = lower_text.find(keyword.lower())
            if index != -1:
                start = max(0, index - 50)
                end = min(len(full_text), index + 50)
                context = full_text[start:end]
                print(f"  Context: ...{context}...")
        else:
            print(f"'{keyword}': Not found")

    print("=" * 80)

if __name__ == "__main__":
    # Default to syllabus.pdf in current directory
    pdf_file = "syllabus.pdf"

    print("PDF Text Extraction Debug Tool")
    print()

    # Allow user to specify a different file
    user_input = input(f"Enter PDF filename (default: {pdf_file}): ").strip()
    if user_input:
        pdf_file = user_input

    print()
    debug_pdf_extraction(pdf_file)
