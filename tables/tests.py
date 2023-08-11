from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import TableMeta
from django.test.utils import override_settings


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": [],
        "DEFAULT_PERMISSION_CLASSES": [],
    },
)
class TableTests(APITestCase):
    # Test for POST /api/table
    def test_create_table(self):
        url = reverse("create-table")
        data = {
            "name": "sample_table",
            "schema": [
                {"title": "name", "type": "string"},
                {"title": "age", "type": "number"},
                {"title": "is_student", "type": "boolean"},
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TableMeta.objects.count(), 1)
        self.assertEqual(TableMeta.objects.get().name, "sample_table")

    # Test for PUT /api/table/:id
    def test_update_table(self):
        table = TableMeta.objects.create(
            name="sample_table",
            schema=[
                {"title": "name", "type": "string"},
                {"title": "age", "type": "number"},
                {"title": "is_student", "type": "boolean"},
            ],
        )
        url = reverse("update-table", args=[table.id])
        data = {
            "schema": [
                {"title": "name", "type": "string"},
                {"title": "age", "type": "number"},
                {"title": "is_student", "type": "boolean"},
                {"title": "address", "type": "string"},
            ]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        table.refresh_from_db()
        self.assertIn({"title": "address", "type": "string"}, table.schema)
