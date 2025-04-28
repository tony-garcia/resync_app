# -*- coding: utf-8 -*-
"""
API resource urls
"""

from django.urls import path, include
from rest_framework import routers

from .views import CompoundViewSet

router = routers.DefaultRouter()
router.register(r"compounds", CompoundViewSet, basename="compound")

urlpatterns = [path("", include(router.urls))]
