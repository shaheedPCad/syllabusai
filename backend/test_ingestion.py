#!/usr/bin/env python3
"""
Test PDF Ingestion Script

This script validates PDF text extraction quality by:
1. Finding test PDFs in the backend/ directory
2. Extracting text using the current PDF parser
3. Printing extracted text to console for analysis
4. Reporting statistics (page count, character count, text density)

Usage:
    python test_ingestion.py
"""

import sys
import os
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from pypdf import PdfReader


def test_pdf_extraction(pdf_path: Path):
    """
    Extract and analyze text from a PDF file.

    Args:
        pdf_path: Path to PDF file
    """
    print(f"\n{'='*80}")
    print(f"Testing PDF: {pdf_path.name}")
    print(f"{'='*80}\n")

    try:
        # Read PDF
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)

            # Print metadata
            print(f"📄 Pages: {len(reader.pages)}")
            print(f"📦 File size: {pdf_path.stat().st_size / 1024:.2f} KB")

            # Extract text from each page
            text_parts = []
            page_stats = []

            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text:
                    text_parts.append(text)
                    char_count = len(text.strip())
                    word_count = len(text.split())
                    page_stats.append({
                        'page': i,
                        'chars': char_count,
                        'words': word_count
                    })

                    print(f"\n--- Page {i} ---")
                    print(f"Characters: {char_count}")
                    print(f"Words: {word_count}")
                    print(f"\nFirst 300 characters:")
                    print(f"{text[:300]}...")
                else:
                    print(f"\n--- Page {i} ---")
                    print("⚠️  NO TEXT EXTRACTED (blank/image-only page)")
                    page_stats.append({
                        'page': i,
                        'chars': 0,
                        'words': 0
                    })

            # Full text analysis
            full_text = "\n\n".join(text_parts)
            total_chars = len(full_text)
            total_words = len(full_text.split())

            print(f"\n{'='*80}")
            print("📊 EXTRACTION SUMMARY")
            print(f"{'='*80}")
            print(f"Total characters: {total_chars:,}")
            print(f"Total words: {total_words:,}")
            print(f"Average chars/page: {total_chars / len(reader.pages):.0f}")
            print(f"Average words/page: {total_words / len(reader.pages):.0f}")

            # Density analysis
            if total_chars < 100:
                print("\n❌ EXTRACTION QUALITY: VERY POOR (almost no text)")
                print("   → Likely image-based PDF or slides with minimal text")
                print("   → Recommend upgrading to pdfplumber or marker")
            elif total_chars < 500:
                print("\n⚠️  EXTRACTION QUALITY: POOR (sparse text)")
                print("   → May be slide deck or scanned document")
                print("   → Consider upgrading PDF parser")
            elif total_chars < 2000:
                print("\n⚠️  EXTRACTION QUALITY: MODERATE (limited text)")
                print("   → Acceptable for short documents")
            else:
                print("\n✅ EXTRACTION QUALITY: GOOD (sufficient text)")

            # Show full text sample
            print(f"\n{'='*80}")
            print("📝 FULL EXTRACTED TEXT (first 1000 chars)")
            print(f"{'='*80}")
            print(full_text[:1000])
            if len(full_text) > 1000:
                print("\n... (truncated)")

            return full_text, {
                'pages': len(reader.pages),
                'total_chars': total_chars,
                'total_words': total_words,
                'page_stats': page_stats
            }

    except Exception as e:
        print(f"❌ ERROR: Failed to extract text from {pdf_path.name}")
        print(f"   Error: {str(e)}")
        return None, None


def main():
    """Find and test all PDFs in backend/ directory."""

    backend_dir = Path(__file__).parent
    pdf_files = list(backend_dir.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDF files found in backend/ directory")
        print(f"   Searched: {backend_dir}")
        return 1

    print(f"\n{'#'*80}")
    print(f"PDF INGESTION TEST")
    print(f"{'#'*80}")
    print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"  • {pdf.name}")

    # Test each PDF
    results = {}
    for pdf_path in pdf_files:
        text, stats = test_pdf_extraction(pdf_path)
        results[pdf_path.name] = {
            'text': text,
            'stats': stats,
            'success': text is not None
        }

    # Final summary
    print(f"\n{'#'*80}")
    print("OVERALL SUMMARY")
    print(f"{'#'*80}")

    for filename, result in results.items():
        if result['success']:
            stats = result['stats']
            quality = "✅" if stats['total_chars'] >= 2000 else "⚠️"
            print(f"{quality} {filename}: {stats['total_chars']:,} chars, {stats['total_words']:,} words")
        else:
            print(f"❌ {filename}: FAILED")

    # Recommendation
    poor_quality = sum(1 for r in results.values()
                       if r['success'] and r['stats']['total_chars'] < 500)

    if poor_quality > 0:
        print(f"\n⚠️  {poor_quality} PDF(s) have poor extraction quality")
        print("   RECOMMENDATION: Upgrade to pdfplumber for better text extraction")
        print("   Install: pip install pdfplumber")
        print("   Update: app/services/rag_service.py line 106-126")
    else:
        print("\n✅ All PDFs extracted successfully with good quality")

    return 0


if __name__ == "__main__":
    sys.exit(main())
