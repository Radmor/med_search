from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    filtering_method = serializers.CharField()
    comparison_method = serializers.CharField()
