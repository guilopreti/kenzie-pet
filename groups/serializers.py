from unittest.util import _MAX_LENGTH

from rest_framework import serializers

from .models import Group


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Group.objects.create(**validated_data)

    def update(self, instace, validated_data, partial=True):
        instace.name = validated_data.get("name", instace.name)
        instace.scientific_name = validated_data.get(
            "scientific_name", instace.scientific_name
        )

        instace.save()
        return instace
