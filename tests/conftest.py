import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.pokemon_service import pokemon_service


@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_pokemon_service():
    """Fixture to reset the pokemon service state before each test."""
    pokemon_service.local_pokemons = {}
    pokemon_service.next_id = 10001
    yield pokemon_service
    pokemon_service.local_pokemons = {}
    pokemon_service.next_id = 10001


@pytest.fixture
def mock_pokemon_list_response():
    """Fixture providing mock response for pokemon list."""
    return {
        "count": 1302,
        "next": "https://pokeapi.co/api/v2/pokemon?offset=20&limit=20",
        "previous": None,
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
        ],
    }


@pytest.fixture
def mock_pokemon_detail_response():
    """Fixture providing mock response for individual pokemon."""
    return {
        "id": 1,
        "name": "bulbasaur",
        "height": 7,
        "weight": 69,
        "base_experience": 64,
        "types": [
            {
                "slot": 1,
                "type": {
                    "name": "grass",
                    "url": "https://pokeapi.co/api/v2/type/12/",
                },
            },
            {
                "slot": 2,
                "type": {
                    "name": "poison",
                    "url": "https://pokeapi.co/api/v2/type/4/",
                },
            },
        ],
        "sprites": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
        },
    }


@pytest.fixture
def valid_pokemon_create_data():
    """Fixture providing valid data for creating a pokemon."""
    return {
        "name": "testmon",
        "height": 15,
        "weight": 250,
        "types": ["fire", "flying"],
        "base_experience": 180,
    }


@pytest.fixture
def invalid_pokemon_create_data():
    """Fixture providing invalid data for creating a pokemon."""
    return {
        "name": "",  # Invalid: empty name
        "height": -5,  # Invalid: negative height
        "weight": 0,  # Invalid: zero weight
        "types": [],  # Invalid: empty types list
    }
