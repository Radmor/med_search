from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    filtering_method = serializers.CharField()
    comparison_method = serializers.CharField()
    terms_weights = serializers.DictField(
        child=serializers.FloatField(),
        default={},
    )
    flags = serializers.DictField(default={})


class SearchConfigSerializer(serializers.Serializer):
    filtering_methods = serializers.ListField(child=serializers.CharField())
    comparison_methods = serializers.ListField(child=serializers.CharField())
