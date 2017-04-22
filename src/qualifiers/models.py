from django.db import models
from citations.models import Citation


class Qualifier(models.Model):
    id = models.BigAutoField(primary_key=True)
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid', blank=True, null=True)
    num = models.SmallIntegerField(blank=True, null=True)
    sub = models.SmallIntegerField(blank=True, null=True)
    major = models.BooleanField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'qualifiers'
        unique_together = (('pmid', 'num', 'sub'),)
