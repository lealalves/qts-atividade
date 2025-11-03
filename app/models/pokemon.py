from typing import List, Optional
from pydantic import BaseModel, Field


class PokemonType(BaseModel):
    """Model for Pokemon type information."""

    name: str
    url: str


class PokemonTypeSlot(BaseModel):
    """Model for Pokemon type slot."""

    slot: int
    type: PokemonType


class PokemonSprites(BaseModel):
    """Model for Pokemon sprites."""

    front_default: Optional[str] = None
    back_default: Optional[str] = None


class PokemonStat(BaseModel):
    """Model for Pokemon stat."""

    name: str
    base_stat: int


class Pokemon(BaseModel):
    """Complete Pokemon model from PokeAPI."""

    id: int
    name: str
    height: int
    weight: int
    types: List[PokemonTypeSlot]
    sprites: Optional[PokemonSprites] = None
    base_experience: Optional[int] = None


class PokemonListItem(BaseModel):
    """Model for Pokemon list item."""

    name: str
    url: str


class PokemonListResponse(BaseModel):
    """Response model for list of pokemons."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[PokemonListItem]


class PokemonCreate(BaseModel):
    """Model for creating a new Pokemon."""

    name: str = Field(..., min_length=1, max_length=50)
    height: int = Field(..., gt=0)
    weight: int = Field(..., gt=0)
    types: List[str] = Field(..., min_length=1, max_length=2)
    base_experience: Optional[int] = Field(None, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "custom-pokemon",
                "height": 10,
                "weight": 100,
                "types": ["fire", "flying"],
                "base_experience": 200,
            }
        }


class PokemonResponse(BaseModel):
    """Response model for Pokemon data."""

    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    base_experience: Optional[int] = None
    sprites: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "bulbasaur",
                "height": 7,
                "weight": 69,
                "types": ["grass", "poison"],
                "base_experience": 64,
                "sprites": {"front_default": "https://example.com/sprite.png"},
            }
        }
