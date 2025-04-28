# -*- coding: utf-8 -*-
"""
tests for searching compound data
"""
import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCompoundDataSearching:
    """Test harness for search/filtering by compound data"""

    @pytest.mark.parametrize("param, search_term, num_results", [("name", "aspirin", 1), ("is_drug", "no", 2)])
    def test_exact_string_match(self, param, search_term, num_results, api_client, setup_test_data):
        """Test search by exact match on string values"""
        url = f"{reverse('compound-list')}?data__{param}={search_term}"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == num_results

        for item in data:
            assert item["data"][param] == search_term

    @pytest.mark.parametrize("mw_value, result_name", [(151.16, "acetaminophen"), (52.03, "cyanide")])
    def test_exact_numeric_match(self, mw_value, result_name, api_client, setup_test_data):
        """Test search by exact numeric value"""
        url = f"{reverse('compound-list')}?data__mw={mw_value}"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["data"]["name"] == result_name

    def test_greater_than_filter(self, api_client, setup_test_data):
        """Test greater than operation on numeric values"""
        url = f"{reverse('compound-list')}?data__mw__gt=206.28"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

        assert data[0]["data"]["mw"] > 206.28

    def test_less_than_or_equal_filter(self, api_client, setup_test_data):
        """Test less than or equal operation on numeric values"""
        url = f"{reverse('compound-list')}?data__mw__gte=206.28"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        names = [item["data"]["name"] for item in data]
        assert "diphenhydramine" in names
        assert "ibuprofen" in names

    @pytest.mark.parametrize("search_term, name", [("caff", "caffeine"), ("alde", "formaldehyde")])
    def test_contains_string_filter(self, search_term, name, api_client, setup_test_data):
        """Test contains operation on string values"""
        url = f"{reverse('compound-list')}?data__name__contains={search_term}"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["data"]["name"] == name

    def test_startswith_filter(self, api_client, setup_test_data):
        """Test startswith operation on string values"""
        url = f"{reverse('compound-list')}?data__name__startswith=a"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        names = [item["data"]["name"] for item in data]
        assert "aspirin" in names
        assert "acetaminophen" in names

    def test_endswith_filter(self, api_client, setup_test_data):
        """Test startswith operation on string values"""
        url = f"{reverse('compound-list')}?data__name__endswith=ine"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        names = [item["data"]["name"] for item in data]
        assert "diphenhydramine" in names
        assert "caffeine" in names

    def test_has_key_filter(self, api_client, setup_test_data):
        """Test has_key operation to check for existence of a key"""
        url = f"{reverse('compound-list')}?data__has_key=brand_name"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        brand_names = [item["data"].get("brand_name") for item in data]
        assert "Tylenol" in brand_names
        assert "Lyrica" in brand_names
        assert "Benadryl" in brand_names

    def test_full_text_search(self, api_client, setup_test_data):
        """Test full-text search across all JSON values"""
        url = f"{reverse('compound-list')}?search=ri"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["data"]["name"] == "aspirin"
        assert data[1]["data"]["name"] == "pregabalin"  # matches on brand_name Lyrica

    def test_multiple_filters(self, api_client, setup_test_data):
        """Test combining multiple filters"""
        # this would include 2 more compounds based on mw, but they aren't drugs
        url = f"{reverse('compound-list')}?data__is_drug=yes&data__mw__lt=152"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["data"]["name"] == "acetaminophen"

    def test_nonexistent_key(self, api_client, setup_test_data):
        """Test filtering on a key that doesn't exist"""
        url = f"{reverse('compound-list')}?data__nonexistent=value"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
