# Basic Hotel Platform

A minimal internal hotel admin tool demonstrating domain modeling, backend API endpoints, and a simple UI.

## Features
- **Authentication**: JWT-based login with a seeded admin user.
- **Hotel Management**: Create and list hotels.
- **Room Types & Rates**: Manage room types with base rates.
- **Rate Adjustments**: Apply date-specific rate adjustments.
- **Effective Rate Calculation**: Automatically calculates the final rate based on the latest applicable adjustment.
- **Minimal UI**: MInimal design with responsive layout.

## Setup

### Prerequisites
- **Python** 3.10+ (backend)
- **Node.js** 18+ and **npm** (frontend)

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Seed the admin user (required for login):
   ```bash
   python seed.py
   ```
   **Credentials**:
   - Username: `admin`
   - Password: `password123`

6. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```
   API will be available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

   **Configuration**:
   - The backend uses a `.env` file to configure CORS origins.
   - Example `.env`:
     ```env
     BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
     ```

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
   App will be available at `http://localhost:5173`.

### Docker Compose 

Optionally you can run the application using Docker Compose:

1. **Prerequisites**: Docker and Docker Compose installed on your system

2. **Build and start services**:
   ```bash
   docker-compose up --build
   ```
   This will:
   - Build both backend and frontend Docker images
   - Run database migrations automatically
   - Seed the admin user
   - Start both services with health checks

3. **Access the application**:
   - **Frontend UI**: `http://localhost:5173`
   - **Backend API**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`

4. **Default credentials**:
   - Username: `admin`
   - Password: `password123`

**Note**: The Docker setup includes:
- Automatic database migrations on startup
- Hot-reload for backend development
- Health checks for all services
- Persistent SQLite database volume
- Proper networking between containers


## Documentation
**[Full Architecture Documentation](./docs/ARCHITECTURE.md)** - Comprehensive documentation including:
- Entity-Relationship (ER) diagrams
- API architecture and endpoints
- Sequence diagrams for key workflows (authentication, hotel creation, rate calculations)

## Database Migrations with Alembic

This project uses **Alembic** for version-controlled database migrations. Migration scripts in `backend/alembic/versions/` define incremental schema changes with `upgrade()` and `downgrade()` functions. Alembic can auto-generate migrations by comparing SQLAlchemy models to the current database state using `alembic revision --autogenerate -m "message"`, then apply them with `alembic upgrade head`.

## Design Patterns & Best Practices

**Backend**: Follows a clean architecture with Service Layer pattern for business logic (`app/services/`), Repository pattern via SQLAlchemy ORM, dependency injection for database sessions and authentication, Pydantic schemas for validation, and domain-driven design reflecting the business model.

**Frontend**: Implements component-based architecture with reusable UI components, Context API for authentication state management, a service layer for API abstraction (`services/api.js`), CSS variables for consistent theming and React Router for protected routing.

## Setup

### Prerequisites
- **Python** 3.10+ (backend)
- **Node.js** 18+ and **npm** (frontend)

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Seed the admin user (required for login):
   ```bash
   python seed.py
   ```
   **Credentials**:
   - Username: `admin`
   - Password: `password123`

6. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```
   API will be available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

   **Configuration**:
   - The backend uses a `.env` file to configure CORS origins.
   - Example `.env`:
     ```env
     BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
     ```

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
   App will be available at `http://localhost:5173`.

### Docker Compose 

Optionally you can run the application using Docker Compose:

1. **Prerequisites**: Docker and Docker Compose installed on your system

2. **Build and start services**:
   ```bash
   docker-compose up --build
   ```
   This will:
   - Build both backend and frontend Docker images
   - Run database migrations automatically
   - Seed the admin user
   - Start both services with health checks

3. **Access the application**:
   - **Frontend UI**: `http://localhost:5173`
   - **Backend API**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`

4. **Default credentials**:
   - Username: `admin`
   - Password: `password123`

**Note**: The Docker setup includes:
- Automatic database migrations on startup
- Hot-reload for backend development
- Health checks for all services
- Persistent SQLite database volume
- Proper networking between containers

## Verification
- **Backend tests**: Run `pytest` in the `backend` directory to execute the comprehensive test suite covering authentication, API endpoints, services, and security.
- **Frontend build**: Run `npm run build` in the `frontend` directory.

## Trade-offs
- **SQLite for portability**: SQLite keeps setup lightweight and reproducible. The trade-off is limited concurrency and fewer production-grade features compared to Postgres.
- **Float for currency**: Float is simple to serialize and sufficient for a demo. For production-grade billing, `Decimal` or a cents-based integer model would prevent rounding issues.
- **Single-role authentication**: A seeded admin user accelerates evaluation and onboarding. A real deployment would require role-based access, password rotation, and refresh tokens.
- **Minimal UI library usage**: Avoiding a heavy UI library reduces bundle size and keeps styles intentional. The trade-off is more manual styling work for complex components.
