# Basic Hotel Platform

A minimal internal hotel admin tool demonstrating domain modeling, backend API endpoints, and a simple UI.

## Features
- **Authentication**: JWT-based login with a seeded admin user.
- **Hotel Management**: Create and list hotels.
- **Room Types & Rates**: Manage room types with base rates.
- **Rate Adjustments**: Apply date-specific rate adjustments.
- **Effective Rate Calculation**: Automatically calculates the final rate based on the latest applicable adjustment.
- **Premium UI**: Glassmorphism design with responsive layout.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy (SQLite), Alembic, Pydantic, PyJWT.
- **Frontend**: React, Vite, TypeScript, Vanilla CSS (Glassmorphism).

## Setup & Running

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

### Optional: Docker Compose
If you prefer, you can run the services via Docker Compose (from the repo root):
```bash
docker-compose up --build
```

## Verification
- **Backend tests**: Run `pytest` in the `backend` directory.
- **Frontend build**: Run `npm run build` in the `frontend` directory.

## Design Choices (Frontend)
- **Component focus over framework complexity**: The UI is built with React + TypeScript and light composition. This keeps the view layer easy to navigate and avoids coupling to a large component library.
- **Custom CSS with design tokens**: The glassmorphism theme uses CSS variables for color, spacing, and shadows, making the UI visually consistent and easy to iterate without introducing a styling dependency.
- **Responsive layout by default**: Layouts are implemented with flexible grids and spacing to keep common admin workflows usable on smaller screens.

## Design Choices (Backend)
- **FastAPI + SQLAlchemy**: A small, predictable stack that supports typed request/response models and straightforward CRUD + domain logic.
- **Alembic migrations**: Ensures schema changes are tracked and reproducible for local or CI environments.
- **JWT auth with a seeded admin**: Keeps focus on domain workflows without the overhead of user management or identity providers for this scope.

## Trade-offs
- **SQLite for portability**: SQLite keeps setup lightweight and reproducible. The trade-off is limited concurrency and fewer production-grade features compared to Postgres.
- **Float for currency**: Float is simple to serialize and sufficient for a demo. For production-grade billing, `Decimal` or a cents-based integer model would prevent rounding issues.
- **Single-role authentication**: A seeded admin user accelerates evaluation and onboarding. A real deployment would require role-based access, password rotation, and refresh tokens.
- **Minimal UI library usage**: Avoiding a heavy UI library reduces bundle size and keeps styles intentional. The trade-off is more manual styling work for complex components.
