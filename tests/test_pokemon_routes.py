import pytest
from unittest.mock import patch, Mock
import httpx
from fastapi import status


class TestGetAllPokemons:
    """Test suite for GET /pokemons endpoint."""

    @pytest.mark.asyncio
    async def test_get_all_pokemons_success(
        self, client, mock_pokemon_list_response, reset_pokemon_service
    ):
        """Test successful retrieval of pokemon list."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_pokemon_list_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            response = client.get("/pokemons?limit=20&offset=0")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "count" in data
            assert "results" in data
            assert len(data["results"]) == 3
            assert data["results"][0]["name"] == "bulbasaur"

    @pytest.mark.asyncio
    async def test_get_all_pokemons_api_failure(self, client, reset_pokemon_service):
        """Test handling of external API failure when fetching pokemon list."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.HTTPError("API unavailable")

            response = client.get("/pokemons?limit=20&offset=0")

            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert (
                "Failed to fetch pokemons from external API"
                in response.json()["detail"]
            )


class TestGetPokemonById:
    """Test suite for GET /pokemons/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_pokemon_by_id_success(
        self, client, mock_pokemon_detail_response, reset_pokemon_service
    ):
        """Test successful retrieval of a specific pokemon by ID."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_pokemon_detail_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            response = client.get("/pokemons/1")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "bulbasaur"
            assert data["height"] == 7
            assert data["weight"] == 69
            assert "grass" in data["types"]
            assert "poison" in data["types"]

    @pytest.mark.asyncio
    async def test_get_pokemon_by_id_not_found(self, client, reset_pokemon_service):
        """Test handling of non-existent pokemon ID."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            http_error = httpx.HTTPError("Not found")
            http_error.response = mock_response
            mock_get.side_effect = http_error

            response = client.get("/pokemons/999999")

            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert "not found" in response.json()["detail"].lower()


class TestCreatePokemon:
    """Test suite for POST /pokemons endpoint."""

    def test_create_pokemon_success(
        self, client, valid_pokemon_create_data, reset_pokemon_service
    ):
        """Test successful creation of a new pokemon."""
        # Make request
        response = client.post("/pokemons", json=valid_pokemon_create_data)

        # Assertions
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 10001  # First local ID
        assert data["name"] == valid_pokemon_create_data["name"]
        assert data["height"] == valid_pokemon_create_data["height"]
        assert data["weight"] == valid_pokemon_create_data["weight"]
        assert data["types"] == valid_pokemon_create_data["types"]
        assert data["base_experience"] == valid_pokemon_create_data["base_experience"]

    def test_create_pokemon_validation_failure(
        self, client, invalid_pokemon_create_data, reset_pokemon_service
    ):
        """Test validation failure when creating pokemon with invalid data."""
        response = client.post("/pokemons", json=invalid_pokemon_create_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        # FastAPI returns validation errors in detail
        assert "detail" in response.json()


class TestPokemonIntegration:
    """Integration tests for Pokemon API."""

    def test_create_and_retrieve_local_pokemon(
        self, client, valid_pokemon_create_data, reset_pokemon_service
    ):
        """Test creating a pokemon and then retrieving it."""
        create_response = client.post("/pokemons", json=valid_pokemon_create_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_pokemon = create_response.json()
        pokemon_id = created_pokemon["id"]

        # Retrieve the created pokemon
        get_response = client.get(f"/pokemons/{pokemon_id}")
        assert get_response.status_code == status.HTTP_200_OK
        retrieved_pokemon = get_response.json()

        assert retrieved_pokemon["id"] == created_pokemon["id"]
        assert retrieved_pokemon["name"] == created_pokemon["name"]
        assert retrieved_pokemon["types"] == created_pokemon["types"]
