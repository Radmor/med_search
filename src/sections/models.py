from django.db import models
from citations.models import Citation


class Section(models.Model):
    id = models.BigAutoField(primary_key=True)
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid', blank=True, null=True, related_name='sections')
    source = models.TextField(blank=True, null=True)  # This field type is a guess.
    seq = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=64)
    label = models.CharField(max_length=256, blank=True, null=True)
    content = models.TextField()
    truncated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sections'
        unique_together = (('pmid', 'source', 'seq'),)
