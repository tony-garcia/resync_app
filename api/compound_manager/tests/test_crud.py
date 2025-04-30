# -*- coding: utf-8 -*-
"""
Tests for CRUD API
"""
from unittest.mock import patch

import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status

from compound_manager.models import Compound

# Test data
VALID_SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
INVALID_SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O]["  # Invalid syntax
VALID_COMPOUND_DATA = {
    "name": "aspirin",
    "formula": "C9H8O4",
    "weight": 180.16,
    "logP": 1.23,
    "solubility": "slightly soluble in water",
}
INVALID_COMPOUND_DATA = {"name": "Invalid Compound", "properties": {"soluble": True}}  # Nested dict not allowed

COMPOUND_URL = reverse("compound-list")


@pytest.fixture
def compound_data():
    """Create a single compound for testing"""
    return Compound.objects.create(smiles=VALID_SMILES, data=VALID_COMPOUND_DATA)


@pytest.mark.django_db
class TestCompoundCRUD:
    """Test harness for testing CRUD API"""

    # CREATE tests
    def test_create_compound_valid(self, api_client):
        """Test creating a compound with valid data"""
        url = COMPOUND_URL
        data = {
            "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",  # Ibuprofen
            "data": {"name": "Ibuprofen", "type": "NSAID", "score": 88},
        }
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Compound.objects.count() == 1
        assert Compound.objects.get().smiles == "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
        assert Compound.objects.get().data["name"] == "Ibuprofen"

    def test_create_compound_invalid_smiles(self, api_client):
        """Test creating a compound with invalid SMILES"""
        url = COMPOUND_URL
        data = {"smiles": INVALID_SMILES, "data": VALID_COMPOUND_DATA}
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "smiles" in response.data
        assert Compound.objects.count() == 0

    def test_create_compound_invalid_data(self, api_client):
        """Test creating a compound with invalid data types"""
        url = COMPOUND_URL
        data = {"smiles": VALID_SMILES, "data": INVALID_COMPOUND_DATA}
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "data" in response.data
        assert Compound.objects.count() == 0

    def test_create_compound_strip_whitespace(self, api_client):
        """Test that string values in data have whitespace stripped"""
        url = COMPOUND_URL
        data = {"smiles": VALID_SMILES, "data": {"name": "  Aspirin  ", "type": " NSAID ", "score": 85}}
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        compound = Compound.objects.get()
        assert compound.data["name"] == "Aspirin"
        assert compound.data["type"] == "NSAID"

    def test_bulk_create_compounds(self, api_client):
        """Test bulk creation of multiple compounds"""
        payload = [
            {"smiles": "CCO", "data": {"name": "ethanol", "source": "lab "}},
            {"smiles": "C1=CC=CC=C1", "data": {"name": " benzene", "source": "catalog"}},
        ]

        response = api_client.post(COMPOUND_URL, payload, content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, list)
        assert len(response.data) == 2

        # Check that strings in data were stripped
        compound_1 = Compound.objects.get(smiles="CCO")
        compound_2 = Compound.objects.get(smiles="C1=CC=CC=C1")

        assert compound_1.data["source"] == "lab"
        assert compound_2.data["name"] == "benzene"

    def test_bulk_create_rejects_invalid_input(self, api_client):
        """Test validation of bulk creation"""
        payload = [
            {"smiles": "CO", "data": {"info": "valid"}},
            {"smiles": "CO", "data": {"info": "duplicate"}},  # duplicate SMILES
        ]

        with pytest.raises(IntegrityError):  # fails SMILES string uniqueness
            response = api_client.post(COMPOUND_URL, payload, content_type="application/json")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "smiles" in str(response.data).lower()
            assert Compound.objects.count() == 0  # Nothing should be inserted

    # READ tests
    def test_list_compounds(self, api_client, setup_test_data):
        """Test listing all compounds"""
        url = COMPOUND_URL
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 8

    def test_retrieve_compound(self, api_client, compound_data):
        """Test retrieving a single compound"""
        url = reverse("compound-detail", args=[compound_data.compound_id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["smiles"] == VALID_SMILES
        assert response.data["data"] == VALID_COMPOUND_DATA

    # UPDATE tests
    def test_update_compound_full(self, api_client, compound_data):
        """Test fully updating a compound (PUT)"""
        url = reverse("compound-detail", args=[compound_data.compound_id])
        updated_data = {
            "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",  # Changed to Ibuprofen
            "data": {"name": "Ibuprofen", "formula": "C13H18O2", "weight": 206.29},
        }
        response = api_client.put(url, data=updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        compound = Compound.objects.get(compound_id=compound_data.compound_id)
        assert compound.smiles == "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
        assert compound.data["name"] == "Ibuprofen"
        assert "solubility" not in compound.data  # Old fields should be removed in PUT

    def test_partial_update_compound(self, api_client, compound_data):
        """Test partially updating a compound (PATCH)"""
        url = reverse("compound-detail", args=[compound_data.compound_id])
        patch_data = {"data": {"name": "Modified Aspirin", "new_field": "New Value"}}
        response = api_client.patch(url, data=patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        compound = Compound.objects.get(compound_id=compound_data.compound_id)
        assert compound.data["name"] == "Modified Aspirin"
        assert compound.data["new_field"] == "New Value"
        assert compound.data["formula"] == "C9H8O4"  # Original fields should be preserved

    def test_update_empty_values_removed(self, api_client, compound_data):
        """Test that empty data values are removed when updating"""
        url = reverse("compound-detail", args=[compound_data.compound_id])
        patch_data = {
            "data": {
                "name": "Modified Aspirin",
                "formula": "",  # Empty string should be removed
                "weight": None,  # None should be removed
            }
        }
        response = api_client.patch(url, data=patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        compound = Compound.objects.get(compound_id=compound_data.compound_id)
        assert compound.data["name"] == "Modified Aspirin"
        assert "formula" not in compound.data
        assert "weight" not in compound.data
        assert "logP" in compound.data  # Other fields should remain

    # DELETE tests
    def test_delete_compound(self, api_client, compound_data):
        """Test deleting a compound"""
        url = reverse("compound-detail", args=[compound_data.compound_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Compound.objects.count() == 0

    # VALIDATION tests
    @patch("rdkit.Chem.MolFromSmiles")
    def test_rdkit_validation_called(self, mock_mol_from_smiles, api_client):
        """Test that RDKit validation is called during serializer validation"""
        mock_mol_from_smiles.return_value = "Valid Molecule"
        url = COMPOUND_URL
        data = {"smiles": VALID_SMILES, "data": VALID_COMPOUND_DATA}
        api_client.post(url, data=data, format="json")
        mock_mol_from_smiles.assert_called_once_with(VALID_SMILES, sanitize=False)

    def test_unique_smiles_constraint(self, api_client, compound_data):
        """Test that duplicate SMILES strings are rejected"""
        url = COMPOUND_URL
        data = {"smiles": VALID_SMILES, "data": {"name": "Duplicate Compound"}}  # Same as the one in compound_data
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "smiles" in response.data

    def test_data_types_validation(self, api_client):
        """Test validation of data types in compound data"""
        url = COMPOUND_URL
        data = {
            "smiles": VALID_SMILES,
            "data": {
                "name": "Valid Name",
                "score": 85,
                "ratio": 3.14,
                "invalid": [1, 2, 3],
                "bool": False,
            },  # Lists and bools are not allowed
        }
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "data" in response.data
        assert "invalid" in response.data["data"][0]
        assert "bool" in response.data["data"][0]
