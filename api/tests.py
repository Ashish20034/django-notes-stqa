
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

    def test_get_routes(self):
        response = self.client.get("/api/")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIsInstance(response.data, list)

    def test_get_notes(self):
        response = self.client.get("/api/notes/")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIsInstance(response.data, list)
        self.assertTrue(
            any(
                note["body"] == "Test note for STQA"
                for note in response.data
            )
        )

    def test_create_note(self):
        response = self.client.post(
            "/api/notes/create/",
            {"body": "New automated test note"},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["body"], "New automated test note"
        )
        self.assertTrue(
            Note.objects.filter(
                body="New automated test note"
            ).exists()
        )

    def test_get_single_note(self):
        response = self.client.get(
            f"/api/notes/{self.note.id}/"
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["body"], "Test note for STQA"
        )

    def test_update_note(self):
        response = self.client.put(
            f"/api/notes/{self.note.id}/update/",
            {"body": "Updated test note"},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["body"], "Updated test note"
        )

        self.note.refresh_from_db()
        self.assertEqual(
            self.note.body, "Updated test note"
        )

    def test_delete_note(self):
        response = self.client.delete(
            f"/api/notes/{self.note.id}/delete/"
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertFalse(
            Note.objects.filter(id=self.note.id).exists()
        )
