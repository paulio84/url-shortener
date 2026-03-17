# UrlMe — Flask API

The backend REST API for UrlMe. Built with Flask using the Application Factory pattern, Blueprints, and a Repository/Service architecture.

## Tech Stack

| Tool                    | Purpose                              |
| ----------------------- | ------------------------------------ |
| Python 3.12             | Language                             |
| Flask                   | Web framework                        |
| SQLAlchemy              | ORM                                  |
| Flask-Migrate / Alembic | Database migrations                  |
| Flask-JWT-Extended      | JWT authentication                   |
| Flask-Bcrypt            | Password hashing                     |
| Flask-CORS              | Cross-origin resource sharing        |
| Marshmallow             | Request validation and serialisation |
| Gunicorn                | Production WSGI server               |
| uv                      | Package management                   |
| pytest                  | Test suite                           |
| Docker                  | Local development database           |

## Project Structure
```
app/
├── blueprints/
│   ├── auth/       # POST /api/auth/register, /api/auth/login, /api/auth/refresh
│   ├── urls/       # POST /api/shorten, GET /api/urls, GET /api/urls/<short_code>
│   ├── redirect/   # GET /<short_code>
│   └── status/     # GET /api/status
├── models/
│   ├── url.py      # URL model
│   └── user.py     # User model
├── schemas/
│   ├── url.py      # URL request/response schemas
│   └── user.py     # User request/response schemas
├── config.py       # Environment-based configuration
├── extensions.py   # Flask extensions
├── errors.py       # Centralised error handling
└── __init__.py     # Application factory
bruno/              # Bruno API tests
tests/              # Pytest unit tests
```

Each blueprint follows a three-layer pattern:
```
Route → Service → Repository
```

## API Endpoints
| Method | Endpoint                 | Auth          | Description                    |
| ------ | ------------------------ | ------------- | ------------------------------ |
| POST   | `/api/auth/register`     | No            | Register a new user            |
| POST   | `/api/auth/login`        | No            | Login and receive JWT tokens   |
| POST   | `/api/auth/refresh`      | Refresh token | Refresh access token           |
| POST   | `/api/shorten`           | Yes           | Shorten a URL                  |
| GET    | `/api/urls`              | Yes           | List authenticated user's URLs |
| GET    | `/api/urls/<short_code>` | Yes           | Get a single URL               |
| GET    | `/<short_code>`          | No            | Redirect to original URL       |
| GET    | `/api/status`            | No            | Health check                   |

## Local Development

### Prerequisites

- Python 3.12
- Docker Desktop
- uv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/paulio84/url-shortener.git
cd url-shortener/flask-url
```

2. Install dependencies:
```bash
uv sync
```

3. Create `.env` from the example:
```bash
cp .env.example .env
```

4. Fill in the required values in `.env`:
```
FLASK_APP=wsgi:flask_app
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/urlme_dev
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/urlme_test
SECRET_KEY=<generate with: openssl rand -hex 32>
JWT_SECRET_KEY=<generate with: openssl rand -hex 32>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=urlme_dev
POSTGRES_DB_TEST=urlme_test
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

5. Start the development database:
```bash
make docker-dev-up
```

6. Run migrations:
```bash
make upgrade
```

7. Start the development server:
```bash
make run
```

The API will be available at `http://127.0.0.1:5000`.

## Running Tests
```bash
make test
```

Tests run against a separate test database on port 5433. The test suite covers authentication, URL shortening, redirects, and the status endpoint.

## Staging Environment

To run the full stack locally in a production-like environment:
```bash
make docker-stage-up
```

This builds the Docker image and runs the application with Gunicorn, mirroring the production setup on Render.

## Deployment

The API is deployed to [Render](https://render.com) and triggered automatically when changes to `flask-url/` are merged to `main`.

### Required environment variables on Render
```
FLASK_APP=wsgi:flask_app
FLASK_ENV=production
DATABASE_URL=<Neon connection string>
SECRET_KEY=<strong random value>
JWT_SECRET_KEY=<strong random value>
CORS_ALLOWED_ORIGINS=<Vercel frontend URL>
```
