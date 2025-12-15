#!/usr/bin/env python3
"""
End-to-End Test for Study Suite: Upload -> Process -> Flashcards/Quiz

This script tests the complete Study Suite pipeline:
1. Teacher creates a course
2. Teacher uploads a PDF document
3. Wait for Celery worker to process and generate embeddings
4. Student joins the course
5. Student requests flashcards via POST /documents/{id}/flashcards
6. Student requests quiz via POST /documents/{id}/quiz
7. Verify responses contain valid JSON with expected fields
"""

import asyncio
import httpx
import sys
import time
from pathlib import Path

# Configuration
BASE_URL = "http://backend:8000/api/v1"  # Docker internal
TEACHER_EMAIL = "teacher@clarity.com"
STUDENT_EMAIL = "student@clarity.com"

# Test data
COURSE_TITLE = "Biology 101"
COURSE_DESCRIPTION = "Introduction to Biology"
COURSE_CODE = "BIO101"
TEST_PDF_PATH = "/app/syllabus.pdf"  # Existing PDF with content


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header():
    """Print test header."""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.HEADER}Study Suite End-to-End Test{Colors.ENDC}")
    print(f"{Colors.BOLD}Testing: Upload → Process → Flashcards/Quiz{Colors.ENDC}")
    print("="*70)


def print_step(step_num: int, message: str):
    """Print step header."""
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}Step {step_num}: {message}{Colors.ENDC}")


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


async def run_test() -> bool:
    """
    Run the complete Study Suite test flow.

    Returns:
        True if all tests passed, False otherwise
    """
    print_header()

    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:

            # Step 1: Teacher Creates Course
            print_step(1, "Teacher Creates Course")
            create_response = await client.post(
                f"{BASE_URL}/courses",
                json={
                    "title": COURSE_TITLE,
                    "description": COURSE_DESCRIPTION,
                    "course_code": COURSE_CODE
                },
                headers={"x-user-email": TEACHER_EMAIL}
            )

            if create_response.status_code not in [200, 201]:
                print_error(f"Failed to create course: {create_response.status_code}")
                print_error(f"Response: {create_response.text}")
                return False

            course_data = create_response.json()
            course_id = course_data["id"]
            join_code = course_data["join_code"]

            print_success(f"Course created: {COURSE_TITLE}")
            print_info(f"Course ID: {course_id}")
            print_info(f"Join Code: {join_code}")

            # Step 2: Teacher Uploads Document
            print_step(2, "Teacher Uploads Document")

            # Verify PDF exists
            pdf_path = Path(TEST_PDF_PATH)
            if not pdf_path.exists():
                print_error(f"PDF file not found: {TEST_PDF_PATH}")
                return False

            with open(TEST_PDF_PATH, "rb") as f:
                upload_response = await client.post(
                    f"{BASE_URL}/courses/{course_id}/documents",
                    files={"file": ("syllabus.pdf", f, "application/pdf")},
                    headers={"x-user-email": TEACHER_EMAIL}
                )

            if upload_response.status_code not in [200, 201]:
                print_error(f"Failed to upload document: {upload_response.status_code}")
                print_error(f"Response: {upload_response.text}")
                return False

            document_data = upload_response.json()
            document_id = document_data["id"]

            print_success(f"Document uploaded: {document_data['filename']}")
            print_info(f"Document ID: {document_id}")

            # Step 3: Wait for Document Processing
            print_step(3, "Wait for Document Processing")
            print_info("⏳ Waiting 15 seconds for Celery to process PDF...")
            await asyncio.sleep(15)
            print_success("Processing wait complete")

            # Step 4: Student Joins Course
            print_step(4, "Student Joins Course")
            join_response = await client.post(
                f"{BASE_URL}/courses/{course_id}/join",
                json={"join_code": join_code},
                headers={"x-user-email": STUDENT_EMAIL}
            )

            if join_response.status_code not in [200, 201]:
                print_error(f"Failed to join course: {join_response.status_code}")
                print_error(f"Response: {join_response.text}")
                return False

            print_success("Student enrolled in course")

            # Step 5: Test Flashcards Endpoint
            print_step(5, "Test Flashcards Endpoint")
            flashcards_response = await client.post(
                f"{BASE_URL}/documents/{document_id}/flashcards",
                headers={"x-user-email": STUDENT_EMAIL}
            )

            if flashcards_response.status_code != 200:
                print_error(f"Flashcards endpoint failed: {flashcards_response.status_code}")
                print_error(f"Response: {flashcards_response.text}")
                return False

            print_success("Flashcards endpoint returned 200")

            # Validate flashcards JSON structure
            flashcards_data = flashcards_response.json()

            # Check required fields
            required_fields = ["flashcards", "document_id", "document_name", "total_cards"]
            for field in required_fields:
                if field not in flashcards_data:
                    print_error(f"Missing required field: {field}")
                    return False

            print_success("JSON structure is valid")

            # Validate flashcards list
            flashcards = flashcards_data["flashcards"]
            if not isinstance(flashcards, list):
                print_error("'flashcards' is not a list")
                return False

            if len(flashcards) < 5:
                print_error(f"Too few flashcards: {len(flashcards)} (minimum 5)")
                return False

            print_success(f"Generated {len(flashcards)} flashcards")

            # Validate each flashcard
            for i, card in enumerate(flashcards):
                if "front" not in card or "back" not in card:
                    print_error(f"Card {i} missing 'front' or 'back' field")
                    return False

                if not isinstance(card["front"], str) or not isinstance(card["back"], str):
                    print_error(f"Card {i} has invalid field types")
                    return False

                if len(card["front"]) == 0 or len(card["back"]) == 0:
                    print_error(f"Card {i} has empty fields")
                    return False

            print_success("All flashcards have valid structure")
            print_info(f"First card: \"{flashcards[0]['front'][:50]}...\"")

            # Step 6: Test Quiz Endpoint
            print_step(6, "Test Quiz Endpoint")
            quiz_response = await client.post(
                f"{BASE_URL}/documents/{document_id}/quiz",
                headers={"x-user-email": STUDENT_EMAIL}
            )

            if quiz_response.status_code != 200:
                print_error(f"Quiz endpoint failed: {quiz_response.status_code}")
                print_error(f"Response: {quiz_response.text}")
                return False

            print_success("Quiz endpoint returned 200")

            # Validate quiz JSON structure
            quiz_data = quiz_response.json()

            # Check required fields
            required_fields = ["questions", "document_id", "document_name", "total_questions"]
            for field in required_fields:
                if field not in quiz_data:
                    print_error(f"Missing required field: {field}")
                    return False

            print_success("JSON structure is valid")

            # Validate questions list
            questions = quiz_data["questions"]
            if not isinstance(questions, list):
                print_error("'questions' is not a list")
                return False

            if len(questions) < 3:
                print_error(f"Too few questions: {len(questions)} (minimum 3)")
                return False

            print_success(f"Generated {len(questions)} questions")

            # Validate each question
            for i, question in enumerate(questions):
                # Check required fields
                required = ["question", "options", "correct_answer_index", "explanation"]
                for field in required:
                    if field not in question:
                        print_error(f"Question {i} missing '{field}' field")
                        return False

                # Validate types
                if not isinstance(question["question"], str):
                    print_error(f"Question {i}: 'question' is not a string")
                    return False

                if not isinstance(question["options"], list):
                    print_error(f"Question {i}: 'options' is not a list")
                    return False

                if not isinstance(question["correct_answer_index"], int):
                    print_error(f"Question {i}: 'correct_answer_index' is not an int")
                    return False

                if not isinstance(question["explanation"], str):
                    print_error(f"Question {i}: 'explanation' is not a string")
                    return False

                # Validate constraints
                if len(question["options"]) < 2:
                    print_error(f"Question {i}: too few options ({len(question['options'])})")
                    return False

                if question["correct_answer_index"] < 0 or question["correct_answer_index"] >= len(question["options"]):
                    print_error(f"Question {i}: correct_answer_index out of bounds")
                    return False

                if len(question["question"]) == 0 or len(question["explanation"]) == 0:
                    print_error(f"Question {i}: empty question or explanation")
                    return False

            print_success("All quiz questions have valid structure")
            print_info(f"First question: \"{questions[0]['question'][:50]}...\"")

            # Final Success
            print("\n" + "="*70)
            print(f"{Colors.OKGREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.ENDC}")
            print(f"\n{Colors.BOLD}The Study Suite endpoints are working correctly:{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  1. Flashcards generation ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  2. Quiz generation ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  3. JSON structure validation ✓{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  4. Access control ✓{Colors.ENDC}")
            print("="*70 + "\n")

            return True

    except Exception as e:
        print_error(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_test())
    sys.exit(0 if success else 1)
