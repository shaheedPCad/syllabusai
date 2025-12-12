"""
Integration test for complete course workflow:
1. Teacher creates course
2. Student joins course
3. Teacher uploads document
4. Verify document appears in listing
"""
import httpx
import io

# Configuration
BASE_URL = "http://localhost:8000"
TEACHER_EMAIL = "teacher@clarity.com"
STUDENT_EMAIL = "student@clarity.com"

# Test data
COURSE_DATA = {
    "title": "Physics 101",
    "description": "Introduction to Physics",
    "course_code": "PHYS101"
}


def test_complete_flow():
    """Test the complete course workflow end-to-end."""

    # Step 1: Teacher creates course
    print("\n=== Step 1: Teacher creates course 'Physics 101' ===")
    response = httpx.post(
        f"{BASE_URL}/api/v1/courses",
        json=COURSE_DATA,
        headers={"x-user-email": TEACHER_EMAIL},
        follow_redirects=True
    )

    assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
    course = response.json()

    assert "id" in course, "Course ID not returned"
    assert "join_code" in course, "Join code not returned"
    assert course["title"] == COURSE_DATA["title"]

    course_id = course["id"]
    join_code = course["join_code"]

    print(f"✓ Course created successfully")
    print(f"  - Course ID: {course_id}")
    print(f"  - Join Code: {join_code}")
    print(f"  - Title: {course['title']}")

    # Step 2: Student joins course
    print(f"\n=== Step 2: Student joins course using join code '{join_code}' ===")
    response = httpx.post(
        f"{BASE_URL}/api/v1/courses/{course_id}/join",
        json={"join_code": join_code},
        headers={"x-user-email": STUDENT_EMAIL},
        follow_redirects=True
    )

    assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
    enrollment_result = response.json()

    assert "message" in enrollment_result or "id" in enrollment_result, "Enrollment confirmation not returned"

    print(f"✓ Student enrolled successfully")
    print(f"  - Response: {enrollment_result}")

    # Verify student can now see the course
    response = httpx.get(
        f"{BASE_URL}/api/v1/courses",
        headers={"x-user-email": STUDENT_EMAIL},
        follow_redirects=True
    )
    assert response.status_code == 200
    student_courses = response.json()
    course_ids = [c["id"] for c in student_courses]
    assert course_id in course_ids, "Course not in student's course list"
    print(f"✓ Verified: Course appears in student's course list")

    # Step 3: Teacher uploads document
    print("\n=== Step 3: Teacher uploads document to course ===")

    # Create a dummy text file
    file_content = b"This is a test document for Physics 101.\nChapter 1: Introduction to Mechanics"
    file_data = io.BytesIO(file_content)

    response = httpx.post(
        f"{BASE_URL}/api/v1/courses/{course_id}/documents",
        files={"file": ("physics_notes.txt", file_data, "text/plain")},
        headers={"x-user-email": TEACHER_EMAIL},
        follow_redirects=True
    )

    assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
    document = response.json()

    assert "id" in document, "Document ID not returned"
    assert "s3_key" in document, "S3 key not returned"
    assert "filename" in document, "Filename not returned"

    document_id = document["id"]
    s3_key = document["s3_key"]

    print(f"✓ Document uploaded successfully")
    print(f"  - Document ID: {document_id}")
    print(f"  - S3 Key: {s3_key}")
    print(f"  - Filename: {document['filename']}")

    # Step 4: Verify document appears in listing
    print("\n=== Step 4: Verify document appears in course documents ===")

    # Teacher lists documents
    response = httpx.get(
        f"{BASE_URL}/api/v1/courses/{course_id}/documents",
        headers={"x-user-email": TEACHER_EMAIL},
        follow_redirects=True
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    documents = response.json()

    assert isinstance(documents, list), "Documents should be a list"
    assert len(documents) >= 1, "No documents found"

    document_ids = [doc["id"] for doc in documents]
    assert document_id in document_ids, "Uploaded document not in list"

    print(f"✓ Document verified in course documents list")
    print(f"  - Total documents: {len(documents)}")

    # Student lists documents (should also see it if enrolled)
    response = httpx.get(
        f"{BASE_URL}/api/v1/courses/{course_id}/documents",
        headers={"x-user-email": STUDENT_EMAIL},
        follow_redirects=True
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    student_documents = response.json()

    assert document_id in [doc["id"] for doc in student_documents], "Student cannot see uploaded document"
    print(f"✓ Verified: Student can also see the document")

    print("\n" + "="*50)
    print("✓ ALL TESTS PASSED - Complete workflow verified!")
    print("="*50)


if __name__ == "__main__":
    try:
        test_complete_flow()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
