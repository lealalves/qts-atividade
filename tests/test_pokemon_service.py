import pytest
from unittest.mock import patch, Mock
from app.services.pokemon_service import PokemonService
from app.models.pokemon import PokemonCreate


class TestPokemonService:
    """Test suite for PokemonService class."""

    @pytest.fixture
    def service(self):
        """Fixture to provide a fresh PokemonService instance."""
        return PokemonService()

    @pytest.mark.asyncio
    async def test_get_all_pokemons_success(self, service, mock_pokemon_list_response):
        """Test successful retrieval of all pokemons."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_pokemon_list_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = await service.get_all_pokemons(limit=20, offset=0)

            assert result.count == 1302
            assert len(result.results) == 3
            assert result.results[0].name == "bulbasaur"

    @pytest.mark.asyncio
    async def test_get_pokemon_by_id_from_api(
        self, service, mock_pokemon_detail_response
    ):
        """Test retrieving pokemon by ID from external API."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_pokemon_detail_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = await service.get_pokemon_by_id(1)

            assert result is not None
            assert result.id == 1
            assert result.name == "bulbasaur"
            assert "grass" in result.types
            assert "poison" in result.types

    def test_get_pokemon_by_id_from_local_storage(
        self, service, valid_pokemon_create_data
    ):
        """Test retrieving pokemon by ID from local storage."""
        created = service.create_pokemon(PokemonCreate(**valid_pokemon_create_data))

        result = service.local_pokemons.get(created.id)

        assert result is not None
        assert result.id == created.id
        assert result.name == valid_pokemon_create_data["name"]

    def test_create_pokemon_success(self, service, valid_pokemon_create_data):
        """Test successful creation of a new pokemon."""
        # Create pokemon
        pokemon_data = PokemonCreate(**valid_pokemon_create_data)
        result = service.create_pokemon(pokemon_data)

        assert result.id == 10001
        assert result.name == valid_pokemon_create_data["name"]
        assert result.height == valid_pokemon_create_data["height"]
        assert result.weight == valid_pokemon_create_data["weight"]
        assert result.types == valid_pokemon_create_data["types"]

        assert result.id in service.local_pokemons

    def test_create_multiple_pokemons_increments_id(
        self, service, valid_pokemon_create_data
    ):
        """Test that creating multiple pokemons increments IDs correctly."""
        pokemon1 = service.create_pokemon(PokemonCreate(**valid_pokemon_create_data))

        data2 = valid_pokemon_create_data.copy()
        data2["name"] = "testmon2"
        pokemon2 = service.create_pokemon(PokemonCreate(**data2))

        assert pokemon1.id == 10001
        assert pokemon2.id == 10002
        assert len(service.local_pokemons) == 2
