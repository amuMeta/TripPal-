# TripPal

TripPal is a full-stack smart trip planning prototype with a Vue 3 frontend and a FastAPI backend.

The project accepts a city, travel dates, budget, transportation mode, and preferences, then returns a structured multi-day itinerary with attractions, hotel suggestions, meals, weather, and budget estimates.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Ant Design Vue
- Backend: FastAPI, Pydantic, Requests
- Optional integrations: AMap MCP, Unsplash, Hello Agents

## Repository Structure

```text
backend/
  app/
    agents/        multi-stage planning and provider parsing
    api/           FastAPI entrypoints and routes
    models/        Pydantic schemas
    services/      external service adapters
  tests/           backend unit and API tests

frontend/
  src/
    components/    result page UI modules
    composables/   client-side planning and export logic
    services/      API and storage helpers
    views/         Home and Result pages
```

## Features

- Trip planning API: `POST /api/trip/plan`
- Frontend form to generate travel plans
- Result page with budget, weather, itinerary, export, and map sections
- Fallback planning flow when external providers are unavailable
- Parser layer prepared for more realistic AMap/MCP payloads

## Local Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

### 3. Open the app

- Frontend: `http://127.0.0.1:3000`
- Backend docs: `http://127.0.0.1:8000/docs`

## Environment Variables

Backend example: `backend/.env.example`

Typical values:

```env
LLM_API_KEY=
AMAP_API_KEY=
AMAP_WEB_KEY=
UNSPLASH_ACCESS_KEY=
BACKEND_CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
```

Frontend local example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_AMAP_WEB_KEY=
```

## Testing

Run backend tests:

```bash
cd backend
python -m unittest discover -s tests -p "test_*.py"
```

Note: API tests are skipped automatically if `fastapi.testclient` is unavailable in the current environment.

## Current Notes

- The app can run without external API keys by using fallback itinerary data.
- Map rendering requires `VITE_AMAP_WEB_KEY`.
- Some optional integrations depend on local network access and third-party credentials.
