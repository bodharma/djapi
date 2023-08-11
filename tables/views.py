from django.db import models, connection
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from .models import TableMeta, get_dynamic_model
from .serializers import TableMetaSerializer, DynamicTableRowSerializer
from django.core.exceptions import ObjectDoesNotExist


class TableViewSet(viewsets.ViewSet):
    def _get_dynamic_model(self, table_meta):
        """
        This helper function will create and return a dynamic model based on the given table_meta
        """
        attrs = {
            "__module__": self.__module__,
            "table_meta": models.ForeignKey(TableMeta, on_delete=models.CASCADE),
        }

        for field in table_meta.schema:
            field_title = field["title"]
            if field["type"] == "string":
                attrs[field_title] = models.CharField(max_length=255)
            elif field["type"] == "number":
                attrs[field_title] = models.IntegerField()
            elif field["type"] == "boolean":
                attrs[field_title] = models.BooleanField()

        return type(str(table_meta.name), (models.Model,), attrs)

    def create(self, request):
        # Handle POST /api/table
        table_name = request.data.get("name")
        schema = request.data.get("schema")

        table_meta = TableMeta(name=table_name, schema=schema)
        table_meta.save()

        dynamic_model = self._get_dynamic_model(table_meta)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(dynamic_model)

        return Response(
            {"message": "Table created successfully!"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        # Handle PUT /api/table/:id
        table_meta = TableMeta.objects.get(pk=pk)
        schema = request.data.get("schema")
        table_meta.schema = schema
        table_meta.save()

        dynamic_model = self._get_dynamic_model(table_meta)
        with connection.schema_editor() as schema_editor:
            schema_editor.alter_db_table(
                dynamic_model, table_meta.name, table_meta.name
            )
            # TODO: More refined operations can be added here to handle specific schema changes

        return Response(
            {"message": "Table updated successfully!"}, status=status.HTTP_200_OK
        )

    def create_row(self, request, pk=None):
        # Handle POST /api/table/:id/row
        table_meta = TableMeta.objects.get(pk=pk)
        dynamic_model = self._get_dynamic_model(table_meta)

        data = request.data

        data["table_meta"] = table_meta
        instance = dynamic_model(**data)
        instance.save()

        return Response(
            {"message": "Row added successfully!"}, status=status.HTTP_201_CREATED
        )

    def list_rows(self, request, pk=None):
        # Handle GET /api/table/:id/rows
        table_meta = TableMeta.objects.get(pk=pk)
        dynamic_model = self._get_dynamic_model(table_meta)

        queryset = dynamic_model.objects.all()
        serialized_data = [{"id": obj.id, **obj.__dict__} for obj in queryset]

        return Response(serialized_data, status=status.HTTP_200_OK)


class TableListView(generics.ListAPIView):
    queryset = TableMeta.objects.all()
    serializer_class = TableMetaSerializer


class TableRowViewSet(viewsets.ViewSet):
    def create(self, request, table_id):
        """Create a new row in the dynamic table."""
        try:
            table_meta = TableMeta.objects.get(pk=table_id)
            DynamicTable = get_dynamic_model(table_meta)

            serializer = DynamicTableRowSerializer(
                data=request.data, model=DynamicTable
            )
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request, table_id):
        """Retrieve all rows of a dynamic table."""
        try:
            table_meta = TableMeta.objects.get(pk=table_id)
            DynamicTable = get_dynamic_model(table_meta)

            queryset = DynamicTable.objects.all()
            serializer = DynamicTableRowSerializer(
                queryset, many=True, model=DynamicTable
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND
            )
