# Hotel Platform Frontend

A professional, minimal frontend for the Basic Hotel Platform built with React, TypeScript, and Vite.

## Features

- **Authentication**: JWT-based login with auto-logout on token expiration
- **Hotel Management**: View hotel listings and detailed information
- **Room Types**: Display room types with base rates
- **Rate Adjustments**: Create rate adjustments for room types with date and reason tracking
- **Responsive Design**: Clean, minimal UI with light theme
- **Type Safety**: Full TypeScript implementation matching backend schemas

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and build
- **React Router v6** for client-side routing
- **Axios** for HTTP requests with interceptors
- **Vanilla CSS** with CSS custom properties for theming

## Prerequisites

- Node.js 20.19.0+ or 22.12.0+
- Backend API running on `http://localhost:8000`

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment** (optional):
   
   Create a `.env` file in the root and set the API URL:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Access the application**:
   
   Open [http://localhost:5173](http://localhost:5173) in your browser.

## Login

Use the credentials created in the backend seed data. If using default seeds:

- **Username**: `admin`
- **Password**: `admin123`

## Project Structure

```
src/
├── api/              # API client and endpoint definitions
│   ├── client.ts     # Axios instance with interceptors
│   ├── auth.ts       # Authentication endpoints
│   ├── hotels.ts     # Hotel endpoints
│   ├── rooms.ts      # Room type and rate adjustment endpoints
│   └── types.ts      # TypeScript interfaces
├── components/       # Reusable UI components
│   ├── common/       # Button, Input, Card, Modal, Loader
│   └── layout/       # Navbar, MainLayout
├── context/          # React Context providers
│   └── AuthContext.tsx
├── pages/            # Page components
│   ├── Login.tsx
│   ├── HotelList.tsx
│   ├── HotelDetail.tsx
│   └── NotFound.tsx
├── styles/           # Global styles and theme
│   ├── theme.css     # CSS custom properties
│   └── main.css      # Base styles and reset
├── App.tsx           # Main app with routing
└── main.tsx          # Application entry point
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Walkthrough

### Authentication
- Login page at `/login`
- JWT stored in localStorage
- Auto-redirect to `/hotels` after login
- Auto-logout on 401 responses

### Hotel List
- Grid display of all hotels
- Shows hotel name, location, and active status
- Click "View Details" to navigate to hotel detail page

### Hotel Detail
- Displays hotel information
- Lists all room types with base rates
- "Adjust Rate" button opens modal for creating rate adjustments

### Rate Adjustment
- Modal form with fields:
  - Adjustment Amount (positive or negative)
  - Effective Date
  - Reason for adjustment
- Form validation and error handling
- Success notification on submission

## Design Philosophy

- **Minimal but Professional**: Clean interface without unnecessary elements
- **Accessible**: Proper ARIA labels, keyboard navigation, focus states
- **Responsive**: Works on desktop and mobile
- **Performant**: Optimized component rendering and lazy loading where appropriate
- **Type-Safe**: Full TypeScript coverage for compile-time safety

## Contributing

Code follows these principles:
- Components are small and focused
- Logic is separated from presentation
- CSS follows BEM-like naming conventions
- No hardcoded values - use CSS custom properties
