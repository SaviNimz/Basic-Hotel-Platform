# Basic Hotel Platform - Architecture Documentation


## Overview

The Basic Hotel Platform is a full-stack hotel administration application designed to manage hotels, room types, and dynamic rate adjustments. The system follows a clean, layered architecture with clear separation between frontend, backend API, and data persistence layers.

### Key Features
- **JWT-based Authentication**: Secure login with token-based authentication
- **Hotel Management**: CRUD operations for hotels
- **Room Type Management**: Define and manage different room types per hotel
- **Dynamic Rate Adjustments**: Apply date-specific rate modifications
- **Effective Rate Calculation**: Automatic calculation of final rates based on base rates and adjustments

---

## Domain Model

The system is built around four core domain entities:

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string password_hash
    }
    
    class Hotel {
        +int id
        +string name
        +string location
        +boolean is_active
        +List~RoomType~ room_types
    }
    
    class RoomType {
        +int id
        +int hotel_id
        +string name
        +float base_rate
        +List~RateAdjustment~ adjustments
    }
    
    class RateAdjustment {
        +int id
        +int room_type_id
        +float adjustment_amount
        +date effective_date
        +string reason
    }
    
    Hotel "1" --> "0..*" RoomType : contains
    RoomType "1" --> "0..*" RateAdjustment : has
    User ..> Hotel : manages
```

### Entity Descriptions

- **User**: Admin users who can authenticate and manage the system
- **Hotel**: Physical hotel properties with name, location, and active status
- **RoomType**: Categories of rooms within a hotel (e.g., Deluxe, Suite) with base pricing
- **RateAdjustment**: Date-specific rate modifications applied to room types

---

## Database Schema (ER Diagram)

```mermaid
erDiagram
    users ||--o{ hotels : manages
    hotels ||--o{ room_types : contains
    room_types ||--o{ rate_adjustments : has

    users {
        int id PK
        string username UK
        string password_hash
    }

    hotels {
        int id PK
        string name UK
        string location
        boolean is_active
    }

    room_types {
        int id PK
        int hotel_id FK
        string name
        float base_rate
    }

    rate_adjustments {
        int id PK
        int room_type_id FK
        float adjustment_amount
        date effective_date
        string reason
    }
```

### Relationships

- **users ↔ hotels**: Implicit relationship through authentication (all operations require authenticated user)
- **hotels ↔ room_types**: One-to-Many (A hotel can have multiple room types)
- **room_types ↔ rate_adjustments**: One-to-Many (A room type can have multiple rate adjustments over time)

### Indexes
- `users.username`: Unique index for fast user lookup
- `hotels.name`: Unique index for hotel identification
- Primary keys on all tables

---

## API Architecture

### API Structure

```
/api/v1/
├── /auth
│   └── POST /token              # Login & get JWT token
├── /hotels
│   ├── POST /hotels/            # Create hotel
│   ├── GET /hotels/             # List hotels
│   ├── GET /hotels/{id}         # Get hotel details
│   ├── PUT /hotels/{id}         # Update hotel
│   └── DELETE /hotels/{id}      # Delete hotel
├── /rooms
│   ├── POST /room-types/        # Create room type
│   ├── GET /room-types/         # List room types
│   ├── GET /room-types/{id}     # Get room type details
│   ├── PUT /room-types/{id}     # Update room type
│   └── DELETE /room-types/{id}  # Delete room type
└── /rates
    ├── POST /rate-adjustments/  # Create rate adjustment
    ├── GET /rate-adjustments/   # List rate adjustments
    └── GET /effective-rate/     # Calculate effective rate for date
```

### Request/Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router
    participant Dependency
    participant Service
    participant Database

    Client->>Router: HTTP Request
    Router->>Dependency: get_current_user()
    Dependency->>Dependency: Verify JWT Token
    Dependency-->>Router: User object
    Router->>Service: call service method
    Service->>Database: SQLAlchemy Query
    Database-->>Service: Result
    Service-->>Router: Processed Data
    Router-->>Client: Pydantic Response Model
```

---

## Frontend Architecture

### Component Structure

```
src/
├── api/                    # API client layer
│   ├── auth.ts            # Authentication API calls
│   ├── hotels.ts          # Hotel API calls
│   ├── rooms.ts           # Room type API calls
│   └── rates.ts           # Rate adjustment API calls
├── components/            # Reusable UI components
│   ├── Header.tsx
│   ├── HotelCard.tsx
│   ├── RoomTypeCard.tsx
│   └── RateAdjustmentForm.tsx
├── context/              # React Context
│   └── AuthContext.tsx   # Authentication state
├── pages/                # Page components
│   ├── LoginPage.tsx
│   ├── HotelListPage.tsx
│   └── HotelDetailPage.tsx
├── styles/               # CSS modules
└── App.tsx              # Main app component
```

### State Management

- **Authentication State**: Managed via React Context (`AuthContext`)
- **Local State**: Component-level state with `useState` hooks
- **API State**: Handled through async/await with axios

---

## Sequence Diagrams

### 1. User Authentication Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as React App
    participant API as FastAPI Backend
    participant Auth as JWT Service
    participant DB as Database

    User->>UI: Enter credentials
    UI->>API: POST /api/v1/auth/token
    API->>DB: Query user by username
    DB-->>API: User record
    API->>Auth: Verify password hash
    Auth-->>API: Password valid
    API->>Auth: Generate JWT token
    Auth-->>API: Access token
    API-->>UI: {access_token, token_type}
    UI->>UI: Store token in localStorage
    UI->>UI: Update AuthContext
    UI-->>User: Redirect to Hotel List
```

### 2. Create Hotel Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as React App
    participant API as FastAPI Backend
    participant Service as HotelService
    participant DB as Database

    User->>UI: Fill hotel form & submit
    UI->>API: POST /api/v1/hotels/<br/>Header: Bearer {token}
    API->>API: Validate JWT token
    API->>API: Parse & validate request body
    API->>Service: hotel.create(obj_in)
    Service->>DB: INSERT INTO hotels
    DB-->>Service: Hotel record
    Service-->>API: Hotel object
    API-->>UI: Hotel response (JSON)
    UI->>UI: Update hotel list
    UI-->>User: Show success message
```

### 3. Create Room Type with Rate Adjustment Flow

```mermaid
sequenceDiagram
    actor Admin
    participant UI as React App
    participant API as FastAPI Backend
    participant RoomService as RoomService
    participant RateService as RateService
    participant DB as Database

    Admin->>UI: Navigate to Hotel Detail
    UI->>API: GET /api/v1/hotels/{id}
    API-->>UI: Hotel data with room types
    
    Admin->>UI: Create new room type
    UI->>API: POST /api/v1/room-types/
    API->>RoomService: create(room_type_data)
    RoomService->>DB: INSERT INTO room_types
    DB-->>RoomService: RoomType record
    RoomService-->>API: RoomType object
    API-->>UI: RoomType response
    
    Admin->>UI: Add rate adjustment
    UI->>API: POST /api/v1/rate-adjustments/
    API->>RateService: create(adjustment_data)
    RateService->>DB: INSERT INTO rate_adjustments
    DB-->>RateService: RateAdjustment record
    RateService-->>API: RateAdjustment object
    API-->>UI: RateAdjustment response
    UI-->>Admin: Show updated rates
```

### 4. Calculate Effective Rate Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as React App
    participant API as FastAPI Backend
    participant RateService as RateService
    participant DB as Database

    User->>UI: Select room type & date
    UI->>API: GET /api/v1/effective-rate/<br/>?room_type_id={id}&date={date}
    API->>RateService: get_effective_rate(room_type_id, date)
    RateService->>DB: SELECT base_rate FROM room_types
    DB-->>RateService: base_rate
    RateService->>DB: SELECT adjustments WHERE<br/>room_type_id={id} AND<br/>effective_date <= {date}<br/>ORDER BY effective_date DESC
    DB-->>RateService: List of adjustments
    RateService->>RateService: Calculate:<br/>effective_rate = base_rate +<br/>latest_adjustment.amount
    RateService-->>API: effective_rate
    API-->>UI: {effective_rate, base_rate,<br/>adjustment_applied}
    UI-->>User: Display calculated rate
```

### 5. Update Hotel Flow

```mermaid
sequenceDiagram
    actor Admin
    participant UI as React App
    participant API as FastAPI Backend
    participant Service as HotelService
    participant DB as Database

    Admin->>UI: Edit hotel details
    UI->>API: PUT /api/v1/hotels/{id}<br/>Header: Bearer {token}
    API->>API: Validate JWT token
    API->>Service: hotel.get(id)
    Service->>DB: SELECT * FROM hotels WHERE id={id}
    DB-->>Service: Hotel record
    Service-->>API: Hotel object or None
    
    alt Hotel exists
        API->>Service: hotel.update(db_obj, obj_in)
        Service->>DB: UPDATE hotels SET ...
        DB-->>Service: Updated hotel
        Service-->>API: Hotel object
        API-->>UI: Updated hotel (JSON)
        UI-->>Admin: Show success
    else Hotel not found
        API-->>UI: 404 Not Found
        UI-->>Admin: Show error
    end
```

## Configuration & Environment

### Backend Configuration

Configuration loaded from environment variables:

```env
# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:5173"]

# JWT Settings
SECRET_KEY=<secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./hotel.db
```

### Frontend Configuration

```env
# API Base URL
VITE_API_URL=http://localhost:8000
```

---

## Deployment Architecture

### Development Setup

```mermaid
graph TB
    subgraph "Development Environment"
        FE[Frontend Dev Server<br/>Vite @ :5173]
        BE[Backend Dev Server<br/>Uvicorn @ :8000]
        DB[(SQLite File<br/>hotel.db)]
    end
    
    FE -->|CORS-enabled requests| BE
    BE --> DB
    
    style FE fill:#e1f5ff
    style BE fill:#fff4e1
    style DB fill:#e1ffe1
```

### Docker Compose Setup

```mermaid
graph TB
    subgraph "Docker Environment"
        FEC[Frontend Container<br/>:5173]
        BEC[Backend Container<br/>:8000]
        VOL[Volume: SQLite DB]
    end
    
    FEC -->|Internal Network| BEC
    BEC --> VOL
    
    style FEC fill:#e1f5ff
    style BEC fill:#fff4e1
    style VOL fill:#e1ffe1
```

