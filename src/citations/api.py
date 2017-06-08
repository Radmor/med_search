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

    def ids_to_titles(self, ids):
        return Citation.objects.filter(pmid__in=ids).values_list('title', flat=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        filtering_method = self.request.query_params['filtering_method']
        comparison_method = self.request.query_params['comparison_method']
        query = self.request.query_params.getlist('title')
        ids = self.request.query_params.getlist('ids')
        relevant_titles = self.ids_to_titles(ids)

        found_articles = response.data
        terms_weights = {term: float(self.request.query_params.get(term, 0)) for term in query}
        terms_weights_bis = {term: self.request.query_params.get(term, 0) for term in query}
        all_titles = Citation.objects.values_list('title', flat=True)
        if filtering_method in DESCRIBING_METHODS.keys() and comparison_method in COMPARISON_METHODS.keys():
                found_articles = \
                    sorted(found_articles,
                           key=lambda result: measure_similarity(documents=all_titles,
                                                                 query=query,
                                                                 result=result,
                                                                 content_describing_method =DESCRIBING_METHODS[filtering_method],
                                                                 comparison_method=COMPARISON_METHODS[comparison_method],
                                                                 weights_of_terms=terms_weights),
                                                                 reverse=True
                                                                )
        measures = {}
        for article in found_articles:
            # import pdb; pdb.set_trace()
            measures[article['title']] = measure_similarity(all_titles, query, article,
                                                           DESCRIBING_METHODS[filtering_method],
                                                           COMPARISON_METHODS[comparison_method],
                                                           terms_weights)
        response.data = {'results': found_articles, 'terms_weights': terms_weights_bis, 'measures': measures, 'flags':{} }
        return response

