# -*- coding: utf-8 -*-
"""
Django REST framework serializers
"""
from rest_framework import serializers
from .models import Compound


class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ["compound_id", "smiles", "data"]
