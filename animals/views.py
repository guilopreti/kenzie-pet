from django.db import IntegrityError
from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from animals.serializers import AnimalSerializer

from .models import Animal


class AnimalView(APIView):
    def get(self, request):

        animals = get_list_or_404(Animal)

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

    def post(self, request):
        # try:
        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer = serializer.save()

        animal = AnimalSerializer(serializer)
        return Response(animal.data, status=status.HTTP_201_CREATED)

    # except IntegrityError:
    #     return Response(
    #         {"message": "Group scientific name is already registered"},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )


class AnimalParamsView(APIView):
    def get(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)

            serializer = AnimalSerializer(animal)

            return Response(serializer.data)
        except:
            return Response(
                {"message": "Animal not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)

            animal.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"message": "Animal not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, animal_id):

        for key in request.data.keys():
            if key == "sex" or key == "group":
                return Response(
                    {"message": f"You can not update {key} property."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        try:
            animal = Animal.objects.get(id=animal_id)

            serializer = AnimalSerializer(animal, request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer = serializer.save()

            updated_animal = AnimalSerializer(serializer)

            return Response(updated_animal.data)
        except:
            return Response(
                {"message": "Animal not found."}, status=status.HTTP_404_NOT_FOUND
            )
