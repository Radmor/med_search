from rest_framework import views, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import redirect
from django.urls import reverse_lazy

from .serializers import SearchSerializer, SearchConfigSerializer
from .utils import combine_redirect_url, DESCRIBING_METHODS, COMPARISON_METHODS
from citations.models import Citation

class SearchView(views.APIView):
    query_data_field_name = 'query'
    filtering_type_field_name = 'filtering_method'
    comparison_type_field_name = 'comparison_method'
    terms_weights_field_name = 'terms_weights'
    flags_field_name = 'flags'
    queried_fields = ('title',)
    redirect_url = reverse_lazy('search:citations-list')

    def get_ids(self, titles):
        return Citation.objects.filter(title__in=titles.keys()).values_list(
            'pmid', flat=True
        )

    def post(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            query_data = serializer.data.get(self.query_data_field_name)
            filtering_method = serializer.data.get(self.filtering_type_field_name)
            comparison_method = serializer.data.get(self.comparison_type_field_name)
            terms_weights = serializer.data.get(self.terms_weights_field_name)
            flags = serializer.data.get(self.flags_field_name)
            ids = self.get_ids(flags)
            return redirect(combine_redirect_url(str(self.redirect_url), 
                                                 query_data, filtering_method,
                                                 comparison_method,
                                                 terms_weights,
                                                 self.queried_fields, ids), permanent=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchConfigViewSet(viewsets.ViewSet):
    def list(self, request):
        
        serializer = SearchConfigSerializer({
            'filtering_methods': DESCRIBING_METHODS.values(),
            'comparison_methods': COMPARISON_METHODS.values(),
        })

        return Response(serializer.data)