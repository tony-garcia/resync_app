# -*- coding: utf-8 -*-
"""
DRF filter backends
"""
from rest_framework import filters


class JSONFieldFilter(filters.BaseFilterBackend):
    """Filter that enables searching on arbitrary JSON field values dynamically"""

    # operations that can be applied to values
    OPERATIONS = {
        "eq": "",  # equal (default)
        "gt": "__gt",  # greater than
        "gte": "__gte",  # greater than or equal
        "lt": "__lt",  # less than
        "lte": "__lte",  # less than or equal
        "contains": "__icontains",  # contains (case-insensitive)
        "startswith": "__startswith",  # starts with
        "endswith": "__endswith",  # ends with
        "has_key": "__has_key",  # JSON key exists
    }

    def filter_queryset(self, request, queryset, view):
        json_field = getattr(view, "json_field", "data")
        filter_conditions = {}

        # let's parse the query parameters
        for prop, value in request.query_params.items():
            # JSON field filter parameter format is field__key__operation
            parts = prop.split("__")

            # let's see if this is a JSON field filter
            if len(parts) >= 2 and parts[0] == json_field:
                key = parts[1]

                # Get the operation and default it to equality
                operation = ""
                if len(parts) >= 3 and parts[2] in self.OPERATIONS:
                    operation = self.OPERATIONS[parts[2]]

                # now let's determine the type of the value
                typed_value = self._parse_value(value)

                # build the filter key
                filter_key = f"{json_field}__{key}{operation}"
                filter_conditions[filter_key] = typed_value

            # full-text search
            elif prop == "search" and value:
                queryset = queryset.extra(where=[f"{json_field}::text ILIKE %s"], params=[f"%{value}%"])
        if filter_conditions:
            queryset = queryset.filter(**filter_conditions)

        return queryset

    def _parse_value(self, value: str) -> str | int | float:
        """Try to parse value to correct type"""

        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            # return string by default
            return value
