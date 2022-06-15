from characteristics.models import Characteristic
from characteristics.serializers import CharacteristicSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers

from .models import Animal


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=15)

    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data):
        validated_data["group"]["name"] = validated_data["group"]["name"].lower()
        validated_data["group"]["scientific_name"] = validated_data["group"][
            "scientific_name"
        ].lower()

        try:
            group = Group.objects.get(name=validated_data["group"]["name"])
            validated_data["group"] = group
        except:
            group = Group.objects.create(**validated_data["group"])
            validated_data["group"] = group

        if "characteristics" in validated_data.keys():
            characteristics = []

            for charact in validated_data["characteristics"]:
                charact["name"] = charact["name"].lower()
                try:
                    characteristics.append(
                        Characteristic.objects.get(name=charact["name"])
                    )
                except:
                    characteristics.append(Characteristic.objects.create(**charact))

        del validated_data["characteristics"]

        animal = Animal.objects.create(**validated_data)

        animal.characteristics.set(characteristics)

        return animal

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.weight = validated_data.get("weight", instance.weight)

        if "characteristics" in validated_data.keys():
            characteristics = []

            for charact in validated_data["characteristics"]:
                charact["name"] = charact["name"].lower()
                try:
                    characteristics.append(
                        Characteristic.objects.get(name=charact["name"])
                    )
                except:
                    characteristics.append(Characteristic.objects.create(**charact))

            instance.characteristics.set(characteristics)

        instance.save()
        return instance
