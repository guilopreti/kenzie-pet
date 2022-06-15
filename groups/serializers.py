from unittest.util import _MAX_LENGTH

from rest_framework import serializers

from .models import Group


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=20)
