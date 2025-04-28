# -*- coding: utf-8 -*-
"""
DRF API viewsets
"""
from rest_framework import viewsets

from .filters import JSONFieldFilter
from .models import Compound
from .serializers import CompoundSerializer


class CompoundViewSet(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    filter_backends = [JSONFieldFilter]

    def __clean_data(self, data: dict) -> dict:
        """Remove all leading and trailing spaces from string values in data dictionary

        Args:
            data: the data dictionary attribute of a Compound object

        Returns:
            the data attribute with all leading and trailing spaces removed
        """
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    def create(self, request, *args, **kwargs):
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
