from django.db import models
from citations.models import Citation

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid', blank=True, null=True)
    pos = models.SmallIntegerField(blank=True, null=True)
    name = models.TextField()
    initials = models.CharField(max_length=128, blank=True, null=True)
    forename = models.CharField(max_length=256, blank=True, null=True)
    suffix = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'
        unique_together = (('pmid', 'pos'),)