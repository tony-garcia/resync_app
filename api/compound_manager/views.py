# -*- coding: utf-8 -*-
"""
DRF API viewsets
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from .filters import JSONFieldFilter
from .models import Compound
from .serializers import CompoundSerializer


class CompoundViewSet(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    filter_backends = [JSONFieldFilter]

    def __clean_data(self, data: dict) -> dict:
        """Remove all leading and trailing spaces from string values in data dictionary."""
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)

        if is_bulk:
            for entry in request.data:
                if "data" in entry and isinstance(entry["data"], dict):
                    entry["data"] = self.__clean_data(entry["data"])

            # run validations with many=True on serializer
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)

            # use postgres bulk_create to create instances (but don't save yet)
            compounds = [Compound(**item) for item in serializer.validated_data]
            Compound.objects.bulk_create(compounds)

            # Re-serialize for response (include IDs)
            response_serializer = self.get_serializer(compounds, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        else:
            if request.data.get("data"):
                request.data["data"] = self.__clean_data(request.data.get("data"))
            return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """If compound data is being partially updated (PATCH), merge any changes into the existing data.
        Data key/values are removed if the value is falsey (empty string or None)
        """
        kwargs["partial"] = True
        if request.data.get("data"):
            new_data = self.__clean_data(request.data.get("data"))
            instance = self.get_object()
            updated_data = {**(instance.data or {}), **new_data}
            request.data["data"] = {k: v for k, v in updated_data.items() if v} or None
        return super().update(request, *args, **kwargs)
