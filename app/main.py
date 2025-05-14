from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config import get_settings
from app.interfaces.api.controllers import auth, users, companies, collections

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(collections.router, prefix="/collections", tags=["collections"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Waste Collection API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
