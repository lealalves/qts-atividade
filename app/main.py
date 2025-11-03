from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import pokemon_routes

app = FastAPI(
    title="Pokemon API",
    description="A FastAPI application that integrates with PokeAPI to manage pokemon data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(pokemon_routes.router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Pokemon API is running"}
