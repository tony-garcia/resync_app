from django.db import models


class Compound(models.Model):
    compound_id = models.AutoField(primary_key=True)
    smiles = models.CharField(unique=True)
    data = models.JSONField(null=True)
