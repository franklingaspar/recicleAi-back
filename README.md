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
- SQLite (or PostgreSQL)

### Installation (Local Development)

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
   export DATABASE_URL="sqlite+aiosqlite:///./waste_collection.db"
   export SECRET_KEY="your-secret-key"
   ```
5. Initialize the database:
   ```
   python -m scripts.init_db
   ```
6. Start the application:
   ```
   uvicorn app.main:app --reload
   ```

### Deployment with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/seu-usuario/recicleAi-back.git
   cd recicleAi-back
   ```

2. Configure environment variables (optional):
   Create a `.env` file in the project root with:
   ```
   SECRET_KEY=your_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Verify the API is working:
   ```bash
   curl http://localhost:8001/api
   ```

5. Access the API documentation:
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

### API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

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

## Maintenance

### View logs

```bash
docker-compose logs -f
```

### Restart the API

```bash
docker-compose restart api
```

### Stop the API

```bash
docker-compose down
```

### Update the API

```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Database Backup

The SQLite database is stored in the `./data` volume. To backup, simply copy the `waste_collection.db` file from this directory.

```bash
cp ./data/waste_collection.db ./backup/waste_collection_$(date +%Y%m%d).db
```

## API Endpoints

All API endpoints are available at `http://localhost:8001/api/`.

### Authentication

- `POST /api/token` - Get access token
- `POST /api/refresh` - Refresh access token

### Users

- `GET /api/users/me` - Get current user
- `GET /api/users` - List users (admin)
- `GET /api/users/{user_id}` - Get user by ID (admin)
- `POST /api/users` - Create user (admin)
- `PUT /api/users/{user_id}` - Update user (admin)
- `DELETE /api/users/{user_id}` - Delete user (admin)

### Companies

- `GET /api/companies` - List companies
- `GET /api/companies/{company_id}` - Get company by ID
- `POST /api/companies` - Create company (admin)
- `PUT /api/companies/{company_id}` - Update company (admin)
- `DELETE /api/companies/{company_id}` - Delete company (admin)

### Collections

- `GET /api/collections` - List collections
- `GET /api/collections/{collection_id}` - Get collection by ID
- `POST /api/collections` - Create collection
- `POST /api/collections/{collection_id}/assign` - Assign collection to a collector
- `POST /api/collections/{collection_id}/status` - Update collection status
