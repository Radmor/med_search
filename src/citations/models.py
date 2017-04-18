from django.db import models


class Citation(models.Model):
    pmid = models.BigIntegerField(primary_key=True)
    status = models.TextField()  # This field type is a guess.
    year = models.SmallIntegerField()
    title = models.TextField()
    journal = models.CharField(max_length=256)
    pub_date = models.CharField(max_length=256)
    issue = models.CharField(max_length=256, blank=True, null=True)
    pagination = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateField()
    completed = models.DateField(blank=True, null=True)
    revised = models.DateField(blank=True, null=True)
    modified = models.DateField()

    class Meta:
        managed = False
        db_table = 'citations'



class Abstract(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    source = models.TextField()  # This field type is a guess.
    copyright = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'abstracts'
        unique_together = (('pmid', 'source'),)

class Database(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    name = models.CharField(max_length=256)
    accession = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'databases'
        unique_together = (('pmid', 'name', 'accession'),)


class Descriptor(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    num = models.SmallIntegerField()
    major = models.BooleanField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'descriptors'
        unique_together = (('pmid', 'num'),)


class Identifier(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    namespace = models.CharField(max_length=32)
    value = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'identifiers'
        unique_together = (('pmid', 'namespace'),)


class Keyword(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    owner = models.TextField()  # This field type is a guess.
    cnt = models.SmallIntegerField()
    major = models.BooleanField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'keywords'
        unique_together = (('pmid', 'owner', 'cnt'),)


class PublicationType(models.Model):
    pmid = models.ForeignKey(Citation, models.DO_NOTHING, db_column='pmid')
    value = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'publication_types'
        unique_together = (('pmid', 'value'),)