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

    def validate(self, attrs):
        """Validates that any compound data is either a string, int, or float"""
        if attrs.get("data"):
            compound_data = attrs.get("data")
            allowed_types = (str, int, float)
            invalid_keys = []
            for key, value in compound_data.items():
                if not isinstance(value, allowed_types):
                    invalid_keys.append(key)
            if invalid_keys:
                raise serializers.ValidationError(
                    {
                        "data": f"Compound data must be strings, integers, or floats. The following were not: {', '.join(invalid_keys)}"
                    }
                )
        return super().validate(attrs)
