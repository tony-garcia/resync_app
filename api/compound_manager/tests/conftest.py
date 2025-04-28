import pytest
from rest_framework.test import APIClient

from compound_manager.models import Compound


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def setup_test_data():
    """Set up test data for testing API"""
    test_data = [
        {
            "smiles": "CN(C)CCOC(C1=CC=CC=C1)C2=CC=CC=C2",
            "data": {"name": "diphenhydramine", "brand_name": "Benadryl", "mw": 255.35, "is_drug": "yes"},
        },
        {"smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "data": {"name": "ibuprofen", "mw": 206.28, "is_drug": "yes"}},
        {
            "smiles": "CC(=O)NC1=CC=C(C=C1)O",
            "data": {"name": "acetaminophen", "brand_name": "Tylenol", "mw": 151.16, "is_drug": "yes"},
        },
        {"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "data": {"name": "caffeine", "mw": 194.19, "is_drug": "yes"}},
        {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "data": {"name": "aspirin", "mw": 180.16, "is_drug": "yes"}},
        {
            "smiles": "CC(C)C[C@@H](CC(=O)O)CN",
            "data": {"name": "pregabalin", "brand_name": "Lyrica", "mw": 159.23, "is_drug": "yes"},
        },
        {"smiles": "[C-]#N.[C-]#N", "data": {"name": "cyanide", "mw": 52.03, "is_drug": "no"}},
        {"smiles": "C=O", "data": {"name": "formaldehyde", "mw": 30.026, "is_drug": "no"}},
    ]

    test_objects = [Compound(**data) for data in test_data]
    return Compound.objects.bulk_create(test_objects)
