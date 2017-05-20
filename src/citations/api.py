from rest_framework import viewsets, permissions
from drf_haystack.viewsets import HaystackViewSet

from .serializers import CitationSerializer, CitationIndexSerializer
from .models import Citation
from .utils import term_frequency


class CitationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CitationSerializer

    def get_queryset(self):
        return Citation.objects.all()[:100]


class CitationIndexViewSet(HaystackViewSet):
    index_models = (Citation,)
    serializer_class = CitationIndexSerializer

    def get_queryset(self, **kwargs):
        obj = super(HaystackViewSet, self).get_queryset()
        # obj = sorted(obj, key=lambda result: term_frequency(self.request.query_params, result))
        # import pdb
        # pdb.set_trace()
        return obj
