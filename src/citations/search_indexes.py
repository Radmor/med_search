from haystack import indexes

from .models import Citation


class CitationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.MultiValueField()

    def get_model(self):
        return Citation

    def prepare_content(self, obj):
        return [section.content for section in obj.sections.all()]
