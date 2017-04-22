from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from .search_indexes import CitationIndex
from .models import Citation

class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citation
        fields = ('sections','title')


class CitationIndexSerializer(HaystackSerializer):
    class Meta:
        index_classes = (CitationIndex,)
        fields = ('title',)