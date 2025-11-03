from typing import Dict, Optional
import httpx
from app.models.pokemon import (
    PokemonListResponse,
    PokemonCreate,
    PokemonResponse,
)


class PokemonService:
    """Service for interacting with PokeAPI and managing local pokemons."""

    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(self):
        """Initialize the Pokemon service with local storage."""
        self.local_pokemons: Dict[int, PokemonResponse] = {}
        self.next_id = 10001

    async def get_all_pokemons(
        self, limit: int = 20, offset: int = 0
    ) -> PokemonListResponse:
        """
        Fetch list of all pokemons from PokeAPI.

        Args:
            limit: Number of pokemons to fetch
            offset: Offset for pagination

        Returns:
            PokemonListResponse with list of pokemons

        Raises:
            httpx.HTTPError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/pokemon", params={"limit": limit, "offset": offset}
            )
            response.raise_for_status()
            return PokemonListResponse(**response.json())

    async def get_pokemon_by_id(self, pokemon_id: int) -> Optional[PokemonResponse]:
        """
        Fetch specific pokemon by ID from PokeAPI or local storage.

        Args:
            pokemon_id: ID of the pokemon to fetch

        Returns:
            PokemonResponse if found, None otherwise

        Raises:
            httpx.HTTPError: If API request fails
        """
        # Check if it's a local pokemon
        if pokemon_id >= 10001:
            return self.local_pokemons.get(pokemon_id)

        # Fetch from PokeAPI
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/pokemon/{pokemon_id}")
            response.raise_for_status()
            pokemon_data = response.json()

            return PokemonResponse(
                id=pokemon_data["id"],
                name=pokemon_data["name"],
                height=pokemon_data["height"],
                weight=pokemon_data["weight"],
                types=[t["type"]["name"] for t in pokemon_data["types"]],
                base_experience=pokemon_data.get("base_experience"),
                sprites=pokemon_data.get("sprites"),
            )

    def create_pokemon(self, pokemon_data: PokemonCreate) -> PokemonResponse:
        """
        Create a new pokemon and store it locally.

        Args:
            pokemon_data: Pokemon data to create

        Returns:
            Created PokemonResponse with assigned ID
        """
        new_pokemon = PokemonResponse(
            id=self.next_id,
            name=pokemon_data.name,
            height=pokemon_data.height,
            weight=pokemon_data.weight,
            types=pokemon_data.types,
            base_experience=pokemon_data.base_experience,
            sprites=None,
        )

        self.local_pokemons[self.next_id] = new_pokemon
        self.next_id += 1

        return new_pokemon
pokemon_service = PokemonService()
