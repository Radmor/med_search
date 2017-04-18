from django.db import models
from citations.models import Citation


class Section(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    source = models.TextField()  # This field type is a guess.
    seq = models.SmallIntegerField()
    name = models.CharField(max_length=64)
    label = models.CharField(max_length=256, blank=True, null=True)
    content = models.TextField()
    truncated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sections'
        unique_together = (('pmid', 'source', 'seq'),)
