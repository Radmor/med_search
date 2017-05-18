from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import redirect
from django.urls import reverse_lazy

from .serializers import SearchSerializer
from .utils import combine_redirect_url


class SearchView(views.APIView):
    query_data_field_name = 'query'
    queried_fields = ('title',)
    redirect_url = reverse_lazy('search:citations-list')

    def post(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            query_data = serializer.data.get(self.query_data_field_name)
            return redirect(combine_redirect_url(str(self.redirect_url), 
                                                 query_data, 
                                                 self.queried_fields), permanent=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
