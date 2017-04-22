from haystack import indexes

from .models import Citation


class CitationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Citation