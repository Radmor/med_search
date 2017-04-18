from django.db import models
from citations.models import Citation

class Qualifier(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    num = models.SmallIntegerField()
    sub = models.SmallIntegerField()
    major = models.BooleanField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'qualifiers'
        unique_together = (('pmid', 'num', 'sub'),)