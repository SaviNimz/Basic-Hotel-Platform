# Basic Hotel Platform

A minimal, senior-level internal hotel admin tool demonstrating clean domain modeling, backend fundamentals, and premium UI.

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

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Initialize Database and Migrations (Already configured):
   ```bash
   alembic upgrade head
   ```
4. Seed Admin User (Required for Login):
   ```bash
   python seed.py
   ```
   **Credentials**:
   - Username: `admin`
   - Password: `password123`

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   API will be available at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

   **Configuration**:
   - The backend uses a `.env` file to configure CORS origins.
   - Example `.env` is created automatically or you can create it manually:
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
3. Run the development server:
   ```bash
   npm run dev
   ```
   App will be available at `http://localhost:5173`.

   **Configuration**:
   - The frontend uses a `.env` file to configure the API URL.
   - Example `.env`:
     ```env
     VITE_API_URL=http://localhost:8000
     ```

## Verification
- **Backend Tests**: Run `pytest` in the `backend` directory.
- **Frontend Build**: Run `npm run build` in the `frontend` directory.

## Design Decisions & Trade-offs

### SQLite
**Decision**: Used SQLite instead of PostgreSQL.
**Reason**: Keeps the setup simple and self-contained for this assessment, avoiding the need for Docker or local Postgres installation. Demonstrates relational modeling equally well.

### Float for Currency
**Decision**: Used `Float` for price fields (`base_rate`, `adjustment_amount`).
**Reason**: While `Decimal` is standard for financial applications to avoid precision errors, `Float` was chosen for simplicity and ease of serialization with Pydantic/JSON for this specific scope.

### Unique Hotel Name Constraint
**Decision**: Added a Unique Constraint on `Hotel.name` as the second migration task.
**Reason**: Ensures data integrity and fulfilled the assessment requirement to demonstrate a follow-up migration.

### Minimal Authentication
**Decision**: Implemented access token only (no refresh token), single seeded user.
**Reason**: Focus is on the domain logic and admin functionality. A full auth system (registration, refresh, emailing) would be scope creep.

### Frontend Styling
**Decision**: Custom CSS with variables (Glassmorphism).
**Reason**: To demonstrate "Rich Aesthetics" and CSS proficiency without relying on heavy UI libraries like MUI or Tailwind (unless requested), resulting in a unique, premium look.