from rest_framework import viewsets, permissions
from drf_haystack.viewsets import HaystackViewSet

from .serializers import CitationSerializer, CitationIndexSerializer
from .models import Citation
from .utils import measure_similarity, COMPARISON_METHODS, DESCRIBING_METHODS



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
        terms_weights = {term: self.request.query_params.get(term, 0) for term in query}
        all_titles = Citation.objects.values_list('title', flat=True)
        if filtering_method in DESCRIBING_METHODS.keys() and comparison_method in COMPARISON_METHODS.keys():
                found_articles = \
                    sorted(found_articles,
                           key=lambda result: measure_similarity(documents=all_titles,
                                                                 query=query,
                                                                 result=result,
                                                                 content_describing_method =DESCRIBING_METHODS[filtering_method],
                                                                 comparison_method=COMPARISON_METHODS[comparison_method]))
        response.data = {'results': found_articles, 'terms_weights': terms_weights }
        return response

