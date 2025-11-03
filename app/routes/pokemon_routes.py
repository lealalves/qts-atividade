from fastapi import APIRouter, HTTPException, status, Query
import httpx
from app.models.pokemon import (
    PokemonListResponse,
    PokemonCreate,
    PokemonResponse,
)
from app.services.pokemon_service import pokemon_service

router = APIRouter(prefix="/pokemons", tags=["pokemons"])


@router.get(
    "",
    response_model=PokemonListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all pokemons",
    description="Fetch a list of all pokemons from PokeAPI with pagination support.",
)
async def get_all_pokemons(
    limit: int = Query(20, ge=1, le=100, description="Number of pokemons to fetch"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    List all pokemons from PokeAPI.

    - **limit**: Number of pokemons to fetch (1-100)
    - **offset**: Offset for pagination
    """
    try:
        return await pokemon_service.get_all_pokemons(limit=limit, offset=offset)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch pokemons from external API: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    status_code=status.HTTP_200_OK,
    summary="Get pokemon by ID",
    description="Fetch a specific pokemon by its ID from PokeAPI or local storage.",
)
async def get_pokemon_by_id(pokemon_id: int):
    """
    Get a specific pokemon by ID.

    - **pokemon_id**: ID of the pokemon to fetch
      - IDs 1-10000: Fetched from PokeAPI
      - IDs 10001+: Fetched from local storage
    """
    try:
        pokemon = await pokemon_service.get_pokemon_by_id(pokemon_id)
        if not pokemon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pokemon with ID {pokemon_id} not found",
            )
        return pokemon
    except HTTPException:
        raise
    except httpx.HTTPError as e:
        if hasattr(e, "response") and e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pokemon with ID {pokemon_id} not found",
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pokemon with ID {pokemon_id} not found",
            )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch pokemon from external API: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.post(
    "",
    response_model=PokemonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new pokemon",
    description="Create a new pokemon and store it locally (not in external API).",
)
def create_pokemon(pokemon_data: PokemonCreate):
    """
    Create a new pokemon (stored locally).

    - **name**: Name of the pokemon (1-50 characters)
    - **height**: Height of the pokemon (must be positive)
    - **weight**: Weight of the pokemon (must be positive)
    - **types**: List of pokemon types (1-2 types)
    - **base_experience**: Base experience points (optional, must be non-negative)
    """
    try:
        return pokemon_service.create_pokemon(pokemon_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pokemon: {str(e)}",
        )
