
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Note


class NoteAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.note = Note.objects.create(
            body="Test note for STQA"
        )

    # Test 1: Get API routes
    def test_get_routes(self):
        response = self.client.get("/api/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIsInstance(response.data, list)

    # Test 2: Get all notes
    def test_get_notes(self):
        response = self.client.get("/api/notes/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIsInstance(response.data, list)

        self.assertTrue(
            any(
                note["body"] == "Test note for STQA"
                for note in response.data
            )
        )

    # Test 3: Create a new note
    def test_create_note(self):
        response = self.client.post(
            "/api/notes/create/",
            {"body": "New automated test note"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["body"],
            "New automated test note"
        )

        self.assertTrue(
            Note.objects.filter(
                body="New automated test note"
            ).exists()
        )

    # Test 4: Get a single note
    def test_get_single_note(self):
        response = self.client.get(
            f"/api/notes/{self.note.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["body"],
            "Test note for STQA"
        )

    # Test 5: Update an existing note
    def test_update_note(self):
        response = self.client.put(
            f"/api/notes/{self.note.id}/update/",
            {"body": "Updated test note"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["body"],
            "Updated test note"
        )

        self.note.refresh_from_db()

        self.assertEqual(
            self.note.body,
            "Updated test note"
        )

    # Test 6: Delete a note
    def test_delete_note(self):
        response = self.client.delete(
            f"/api/notes/{self.note.id}/delete/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            Note.objects.filter(
                id=self.note.id
            ).exists()
        )

    # Test 7: GET method not allowed on create endpoint
    def test_create_note_rejects_get(self):
        response = self.client.get(
            "/api/notes/create/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Test 8: POST method not allowed on list endpoint
    def test_list_notes_rejects_post(self):
        response = self.client.post(
            "/api/notes/",
            {"body": "Should not be created"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # Test 9: PUT method not allowed on detail endpoint
    def test_get_note_rejects_put(self):
        response = self.client.put(
            f"/api/notes/{self.note.id}/",
            {"body": "Should not be updated"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

