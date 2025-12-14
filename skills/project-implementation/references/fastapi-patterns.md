# FastAPI Development Patterns

Comprehensive guide for FastAPI development in personal projects.

## Basic Application Structure

### Simple API
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Complete Application with Dependency Injection
```python
# src/main.py
from fastapi import FastAPI
from src.services.data_service import DataService
from src.repositories.data_repository import DataRepository

def create_app():
    # Initialize dependencies
    repository = DataRepository()
    service = DataService(repository)

    # Create application
    app = FastAPI()
    app.state.service = service

    return app

app = create_app()
```

## Pydantic Models

### Request/Response Validation
```python
from pydantic import BaseModel, Field
from typing import Optional

class UserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True
```

## Dependency Injection

### FastAPI Dependencies
```python
from fastapi import Depends
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Application"
    debug: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}
```

### Service Dependencies
```python
from fastapi import Depends
from src.services.data_service import DataService

def get_data_service() -> DataService:
    # Initialize and return service
    return DataService()

@app.get("/data/{item_id}")
async def get_data(
    item_id: str,
    service: DataService = Depends(get_data_service)
):
    return await service.fetch_data(item_id)
```

## Async/Await Patterns

### Async Route Handlers
```python
import aiohttp

@app.get("/external/{resource_id}")
async def fetch_external(resource_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{resource_id}") as response:
            data = await response.json()
            return data
```

### Async Database Operations
```python
from databases import Database

database = Database("postgresql://localhost/db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    return await database.fetch_one(query=query, values={"user_id": user_id})
```

## Error Handling

### HTTP Exceptions
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        result = await fetch_data(item_id)
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
        return result
    except ValueError as e:
        logger.error("Invalid data: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error processing %s", item_id)
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Custom Exception Handlers
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error: {exc.name}"}
    )
```

## OpenAPI Documentation

### Automatic Documentation
FastAPI automatically generates OpenAPI documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Enhanced Documentation
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description with **markdown** support",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Sebastien MORAND",
        "email": "sebastien.morand@loreal.com",
    },
)

@app.get(
    "/items/{item_id}",
    summary="Get item by ID",
    description="Retrieve detailed information about a specific item",
    response_description="Item details",
)
async def get_item(item_id: str):
    return {"item_id": item_id}
```

## Configuration Management

### Environment Variables with Pydantic Settings
```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Application"
    admin_email: str = "admin@example.com"
    items_per_page: int = 50
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage in routes
from fastapi import Depends

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_page": settings.items_per_page,
    }
```

## Running the Application

### Development
```bash
uv run uvicorn src.main:app --reload --port 8000
```

### Production
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Testing

### Basic Tests
```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_async_endpoint():
    response = client.get("/data/123")
    assert response.status_code == 200
```

## Best Practices

1. **Always use async/await** for I/O operations
2. **Validate all inputs** with Pydantic models
3. **Use dependency injection** for services and configuration
4. **Handle errors properly** with appropriate HTTP status codes
5. **Document endpoints** with docstrings and response models
6. **Use environment variables** for configuration
7. **Test endpoints** with TestClient
8. **Follow security best practices** (no credentials in code)
