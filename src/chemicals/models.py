from django.db import models
from citations.models import Citation

class Chemical(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    idx = models.SmallIntegerField()
    uid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'chemicals'
        unique_together = (('pmid', 'idx'),)