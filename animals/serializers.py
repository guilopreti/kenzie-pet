from characteristics.models import Characteristic
from groups.models import Group
from rest_framework import serializers

from .models import Animal


class AnimalGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    scientific_name = serializers.CharField(max_length=20)


class AnimalCharacteristicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=15)

    group = AnimalGroupSerializer()
    characteristics = AnimalCharacteristicSerializer(many=True)

    def create(self, validated_data):

        try:
            group = Group.objects.get(name=validated_data["group"]["name"])
            validated_data["group"] = group
        except:
            group = Group.objects.create(**validated_data["group"])
            validated_data["group"] = group

        if "characteristics" in validated_data.keys():
            characteristics = []

            for charact in validated_data["characteristics"]:
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
        instance.weigth = validated_data.get("weigth", instance.weigth)
        instance.sex = validated_data.get("sex", instance.sex)
        instance.group = validated_data.get("group", instance.group)

        instance.save()
        return instance
