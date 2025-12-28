# FitTrack API

FitTrack is a powerful and modern fitness tracking API built with FastAPI. It allows users to track their workouts, monitor progress through weekly statistics, and manage a custom database of exercises with image support.

## 🚀 Features

- **Authentication**: Secure JWT-based registration and login system.
- **UUID Identifiers**: All entities use UUIDv4 for improved security and scalability.
- **Exercise Management**: Create and list exercises with support for image uploads for better visualization.
- **Workout Tracking**: Log workouts with multiple sets, including data points like reps, weight, and RPE (Rate of Perceived Exertion).
- **Automated Statistics**: Background tasks to calculate weekly volume and performance metrics.
- **AI-Powered**: Integrates with Google Gemini to log workouts via natural language and receive weekly training feedback.
- **Aesthetics & Performance**: Built-in middleware for request processing time headers and file size limits.
- **Flexible UI Support**: Integrated CORS for seamless connection with frontend applications.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **AI/LLM**: [Google Gemini](https://ai.google.dev/) (via Google Generative AI SDK)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- **Auth**: Python-jose (JWT) & Passlib (Bcrypt)

## 🔧 Installation & Setup

### Prerequisites
- Python 3.13+
- PostgreSQL
- Docker (optional)
- **Google Cloud API Key** (for Gemini AI features)

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
   GOOGLE_API_KEY=your_google_gemini_api_key
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

### 🤖 AI Endpoints

-   `POST /ai/workouts/log`: Log a full workout using natural language (e.g., "Bench press 3x8 at 80kg"). The AI parses exercises, sets, reps, and weights, creating them in the database if they don't exist.
-   `GET /ai/coach/weekly`: Get a personalized weekly summary and coaching feedback based on your logged volume and intensity (RPE).

## 📂 Project Structure

```text
fittrack/
├── ai/                # AI logic with Google Gemini (schemas, clients)
├── alembic/           # Database migration history
├── core/              # Core logic (security, exceptions, pagination)
├── db/                # Database connection and base models
├── mcp/               # Model Context Protocol agents (parsers, resolvers)
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
