from django.db import models
from citations.models import Citation

class Chemical(models.Model):
    id = models.BigAutoField(primary_key=True)
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid', blank=True, null=True)
    idx = models.SmallIntegerField(blank=True, null=True)
    uid = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'chemicals'
        unique_together = (('pmid', 'idx'),)