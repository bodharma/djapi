from django.db import models
from django.db import models
from django.apps import apps


def get_dynamic_model(table_meta):
    """
    Retrieve or create a dynamic model based on the given table meta information.
    :param table_meta: An instance of TableMeta containing the specifications for the model.
    :return: The dynamic Django model class.
    """

    # Check if the model already exists. If it does, return it.
    model_name = table_meta.name
    try:
        return apps.get_model("tables", model_name)
    except LookupError:
        pass

    # Otherwise, create the model.
    attrs = {
        "__module__": "tables.models",
        "Meta": type(
            "Meta",
            (),
            {
                "ordering": ["-id"],  # Just as an example
                "db_table": table_meta.db_table_name,
            },
        ),
    }

    for field in table_meta.fields.all():
        if field.field_type == "string":
            attrs[field.name] = models.CharField(max_length=255)
        elif field.field_type == "number":
            attrs[field.name] = models.IntegerField()
        elif field.field_type == "boolean":
            attrs[field.name] = models.BooleanField(default=False)

    DynamicModel = type(model_name, (models.Model,), attrs)

    # Register the model with the apps registry
    apps.register_model("tables", DynamicModel)

    # Return the dynamic model class
    return DynamicModel


class TableMeta(models.Model):
    name = models.CharField(max_length=255)
    schema = models.JSONField()  # Store the field types and titles in JSON
