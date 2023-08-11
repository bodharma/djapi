from rest_framework import serializers
from .models import TableMeta

class TableMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableMeta
        fields = '__all__'


class DynamicTableRowSerializer(serializers.BaseSerializer):
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

    def to_internal_value(self, data):
        # Convert incoming data into a format suitable for your model
        return data

    def to_representation(self, instance):
        # Convert your model instance into a format suitable for rendering into JSON
        return {field.name: getattr(instance, field.name) for field in instance._meta.fields}

    def create(self, validated_data):
        return self.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
