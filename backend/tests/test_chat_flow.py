#!/usr/bin/env python3
"""
End-to-End Test for RAG Flow: Upload -> Process -> Chat

This script tests the complete RAG pipeline:
1. Teacher creates a course
2. Teacher uploads a document with known content
3. Wait for Celery worker to process and generate embeddings
4. Student joins the course
5. Student asks a question via chat API
6. Verify the answer contains expected information
"""

import asyncio
import httpx
import sys
import time
from pathlib import Path
from uuid import UUID

# Configuration
# Use backend service name when running in Docker, localhost when running locally
import os
BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000/api/v1")
TEACHER_EMAIL = "teacher@clarity.com"
STUDENT_EMAIL = "student@clarity.com"

# Test content
COURSE_TITLE = "Computer Science 100"
COURSE_DESCRIPTION = "Introduction to Computing through Applications"
# Use existing syllabus.pdf for testing (known to work with RAG pipeline)
TEST_PDF_PATH = "/app/syllabus.pdf"

QUESTION = "What is CS100 about?"
EXPECTED_ANSWER_CONTAINS = "computing"


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_step(step_num: int, message: str):
    """Print a formatted step message"""
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}Step {step_num}: {message}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{'='*70}{Colors.ENDC}\n")


def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print an info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_waiting(message: str):
    """Print a waiting message"""
    print(f"{Colors.WARNING}⏳ {message}{Colors.ENDC}")


async def run_test():
    """Run the complete RAG flow test"""

    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("=" * 70)
    print("RAG Flow End-to-End Test")
    print("Testing: Upload → Process → Chat")
    print("=" * 70)
    print(f"{Colors.ENDC}\n")

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:

        # Step 1: Teacher creates course
        print_step(1, "Teacher Creates Course")

        create_response = await client.post(
            f"{BASE_URL}/courses",
            json={
                "title": COURSE_TITLE,
                "description": COURSE_DESCRIPTION,
                "course_code": "HIST101"
            },
            headers={"x-user-email": TEACHER_EMAIL}
        )

        if create_response.status_code not in [200, 201]:
            print_error(f"Failed to create course (status {create_response.status_code}): {create_response.text}")
            print_info(f"Request URL: {BASE_URL}/courses")
            print_info(f"Headers: x-user-email: {TEACHER_EMAIL}")
            return False

        course_data = create_response.json()
        course_id = course_data["id"]
        join_code = course_data["join_code"]

        print_success(f"Course created: {COURSE_TITLE}")
        print_info(f"Course ID: {course_id}")
        print_info(f"Join Code: {join_code}")

        # Step 2: Teacher uploads document
        print_step(2, "Teacher Uploads Document")

        print_info(f"Using test PDF: {TEST_PDF_PATH}")

        with open(TEST_PDF_PATH, "rb") as f:
            upload_response = await client.post(
                f"{BASE_URL}/courses/{course_id}/documents",
                files={"file": ("cs100_syllabus.pdf", f, "application/pdf")},
                headers={"x-user-email": TEACHER_EMAIL}
            )

        if upload_response.status_code not in [200, 201]:
            print_error(f"Failed to upload document (status {upload_response.status_code}): {upload_response.text}")
            return False

        upload_data = upload_response.json()
        document_id = upload_data["id"]

        print_success(f"Document uploaded: {upload_data['filename']}")
        print_info(f"Document ID: {document_id}")
        print_info(f"File uploaded to S3: {upload_data.get('s3_key', 'N/A')}")

        # Step 3: Wait for Celery worker to process
        print_step(3, "Wait for Document Processing")

        print_waiting("Waiting for Celery worker to process document and generate embeddings...")
        print_info("This may take 10-15 seconds depending on document size and OpenAI API response time")

        # Wait for processing (Celery task processes asynchronously)
        wait_time = 15  # Wait 15 seconds for processing
        for i in range(wait_time):
            await asyncio.sleep(1)
            if (i + 1) % 5 == 0:
                print_info(f"[{i + 1}s] Still waiting...")

        print_success(f"Waited {wait_time} seconds for processing to complete")

        # Step 4: Student joins course
        print_step(4, "Student Joins Course")

        join_response = await client.post(
            f"{BASE_URL}/courses/{course_id}/join",
            json={"join_code": join_code},
            headers={"x-user-email": STUDENT_EMAIL}
        )

        if join_response.status_code not in [200, 201]:
            print_error(f"Failed to join course (status {join_response.status_code}): {join_response.text}")
            return False

        print_success(f"Student enrolled in course")
        print_info(f"Student: {STUDENT_EMAIL}")

        # Step 5: Student asks question via chat
        print_step(5, "Student Asks Question via Chat API")

        print_info(f"Question: \"{QUESTION}\"")

        chat_response = await client.post(
            f"{BASE_URL}/courses/{course_id}/chat",
            json={"question": QUESTION},
            headers={"x-user-email": STUDENT_EMAIL}
        )

        if chat_response.status_code != 200:
            print_error(f"Chat request failed: {chat_response.text}")
            return False

        chat_data = chat_response.json()
        answer = chat_data["answer"]
        sources = chat_data["sources"]
        confidence = chat_data["confidence"]

        print_success("Received chat response!")
        print_info(f"Answer: {answer}")
        print_info(f"Sources: {len(sources)} document chunks")
        print_info(f"Confidence: {confidence}")

        if sources:
            print_info(f"Top similarity score: {sources[0]['similarity_score']:.3f}")

        # Step 6: Verify results
        print_step(6, "Verify Results")

        success = True

        # Check if answer contains expected content (case-insensitive)
        if EXPECTED_ANSWER_CONTAINS.lower() in answer.lower():
            print_success(f"Answer contains expected text: \"{EXPECTED_ANSWER_CONTAINS}\"")
        else:
            print_error(f"Answer does NOT contain expected text: \"{EXPECTED_ANSWER_CONTAINS}\"")
            success = False

        # Check confidence level
        if confidence in ["high", "medium"]:
            print_success(f"Confidence level is acceptable: {confidence}")
        else:
            print_error(f"Confidence level is low: {confidence}")
            success = False

        # Check sources
        if len(sources) > 0:
            print_success(f"Retrieved {len(sources)} relevant sources")
        else:
            print_error("No sources retrieved")
            success = False

        return success


async def main():
    """Main entry point"""
    try:
        success = await run_test()

        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("=" * 70)
        if success:
            print(f"{Colors.OKGREEN}✓ ALL TESTS PASSED!{Colors.ENDC}")
            print(f"\n{Colors.OKGREEN}The complete RAG flow is working correctly:{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  1. Document upload ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  2. Celery processing ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  3. Embedding generation ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  4. pgvector search ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  5. GPT-4 answer generation ✓{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ TESTS FAILED{Colors.ENDC}")
            print(f"\n{Colors.FAIL}Some checks did not pass. Review the output above.{Colors.ENDC}")
        print("=" * 70)
        print(f"{Colors.ENDC}\n")

        sys.exit(0 if success else 1)

    except Exception as e:
        print_error(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
