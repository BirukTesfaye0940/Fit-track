# FitTrack API

FitTrack is a powerful and modern fitness tracking API built with FastAPI. It allows users to track their workouts, monitor progress through weekly statistics, and manage a custom database of exercises with image support.

## 🚀 Features

- **Authentication**: Secure JWT-based registration and login system.
- **UUID Identifiers**: All entities use UUIDv4 for improved security and scalability.
- **Exercise Management**: Create and list exercises with support for image uploads for better visualization.
- **Workout Tracking**: Log workouts with multiple sets, including data points like reps, weight, and RPE (Rate of Perceived Exertion).
- **Automated Statistics**: Background tasks to calculate weekly volume and performance metrics.
- **Aesthetics & Performance**: Built-in middleware for request processing time headers and file size limits.
- **Flexible UI Support**: Integrated CORS for seamless connection with frontend applications.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- **Auth**: Python-jose (JWT) & Passlib (Bcrypt)

## 🔧 Installation & Setup

### Prerequisites
- Python 3.13+
- PostgreSQL
- Docker (optional)

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fittrack
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the `fittrack` directory:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fittrack
   SECRET_KEY=your_super_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

### Running with Docker

The project includes a `docker-compose.yml` for quick setup:

```bash
docker-compose up --build
```
This will spin up both the FastAPI application and a PostgreSQL database.

## 📖 API Documentation

Once the server is running, you can access the interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📂 Project Structure

```text
fittrack/
├── alembic/           # Database migration history
├── core/              # Core logic (security, exceptions, pagination)
├── db/                # Database connection and base models
├── models/            # SQLAlchemy database models
├── routers/           # API route handlers
├── schemas/           # Pydantic data models
├── services/          # Business logic and background tasks
├── main.py            # FastAPI application entry point
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker orchestration
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
