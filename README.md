# Waste Collection API

A backend application for a waste collection service with three user types: admin, collector, and regular user.

## Features

- User management with different roles (admin, collector, regular)
- Company management for collection services
- Collection request management
- ZIP code-based service area assignment
- Authentication and authorization
- RESTful API

## Architecture

This project follows Clean Architecture principles and SOLID design patterns:

- **Domain Layer**: Contains business entities, value objects, and repository interfaces
- **Application Layer**: Contains use cases and services
- **Infrastructure Layer**: Contains implementations of repositories, database configuration, and external services
- **Interface Layer**: Contains API controllers, request/response schemas, and middleware

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy (with async support)
- Alembic for migrations
- PostgreSQL
- JWT for authentication
- Pytest for testing

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```
   export DATABASE_URL="postgresql+asyncpg://username:password@localhost/waste_collection"
   export SECRET_KEY="your-secret-key"
   ```
5. Run database migrations:
   ```
   alembic upgrade head
   ```
6. Start the application:
   ```
   uvicorn app.main:app --reload
   ```

### API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:

```
pytest
```

Run tests with coverage:

```
pytest --cov=app
```

## Project Structure

```
.
├── app
│   ├── domain
│   │   ├── entities
│   │   ├── repositories
│   │   └── value_objects
│   ├── application
│   │   ├── services
│   │   └── use_cases
│   ├── infrastructure
│   │   ├── database
│   │   ├── auth
│   │   └── repositories
│   └── interfaces
│       └── api
│           ├── controllers
│           ├── schemas
│           └── middlewares
├── migrations
│   └── versions
├── tests
│   ├── unit
│   └── integration
└── alembic.ini
```

## License

This project is licensed under the MIT License.
