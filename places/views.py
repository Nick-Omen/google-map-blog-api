from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from places.models import Place
from places.serializers import PlaceSerializer


class PlaceList(APIView):

    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        places = Place.objects.filter(pk__in=request.data['ids'])
        places.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PlaceDetails(APIView):

        def get(self, request, pk):
            place = get_object_or_404(Place, pk=pk)
            serializer = PlaceSerializer(place)
            return Response(serializer.data)

        def put(self, request, pk):
            place = get_object_or_404(Place, pk=pk)
            serializer = PlaceSerializer(place, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def patch(self, request, pk):
            place = get_object_or_404(Place, pk=pk)
            serializer = PlaceSerializer(place, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            place = get_object_or_404(Place, pk=pk)
            place.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
