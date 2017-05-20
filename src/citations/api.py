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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        found_articles = response.data

        # perform computations here

        response.data = found_articles
        return response

