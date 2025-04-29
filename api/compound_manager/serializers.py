# -*- coding: utf-8 -*-
"""
Django REST framework serializers
"""
from rdkit import Chem
from rest_framework import serializers

from .models import Compound


class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ["compound_id", "smiles", "data"]

    def validate(self, attrs):
        """Validates syntactically valid SMILES and that any compound data is either a string, int, or float"""
        errors = {}
        if attrs.get("smiles"):
            mol = Chem.MolFromSmiles(attrs.get("smiles"), sanitize=False)
            if mol is None:
                errors["smiles"] = "Invalid SMILES string entered"
        if attrs.get("data"):
            compound_data = attrs.get("data")
            allowed_types = (str, int, float)
            invalid_keys = []
            for key, value in compound_data.items():
                # for some reason isinstance(True/False, allowe_types) returns True so we have to check booleans explicitly
                if isinstance(value, bool) or not isinstance(value, allowed_types):
                    invalid_keys.append(key)
            if invalid_keys:
                errors["data"] = (
                    f"Compound data must be strings, integers, or floats. The following were not: {', '.join(invalid_keys)}"
                )
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)
