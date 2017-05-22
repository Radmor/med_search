from rest_framework import viewsets, permissions
from drf_haystack.viewsets import HaystackViewSet

from .serializers import CitationSerializer, CitationIndexSerializer
from .models import Citation
from .utils import term_frequency, COMPARISON_METHODS


class CitationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CitationSerializer

    def get_queryset(self):
        return Citation.objects.all()[:100]


class CitationIndexViewSet(HaystackViewSet):
    index_models = (Citation,)
    serializer_class = CitationIndexSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        filtering_method = self.request.query_params['filtering_method']
        comparison_method = self.request.query_params['comparison_method']
        query = self.request.query_params.getlist('title')
        found_articles = response.data
        # perform computations here
        if filtering_method == 'tf':
            if comparison_method in COMPARISON_METHODS:
                found_articles = \
                    sorted(found_articles,
                           key=lambda result: term_frequency(documents=Citation.objects.all(),
                                                             query=query,
                                                             result=result,
                                                             filtering_method=filtering_method,
                                                             comparison_method=COMPARISON_METHODS[comparison_method]))
        response.data = found_articles
        return response

