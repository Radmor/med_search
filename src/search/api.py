from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import SearchSerializer



class SearchView(views.APIView):
    def post(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
