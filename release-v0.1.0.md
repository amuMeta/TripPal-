# TripPal v0.1.0

## Summary

First publishable release of TripPal, a full-stack smart trip planning prototype built with Vue 3 and FastAPI.

## Highlights

- Added an end-to-end trip planning workflow with frontend form submission and backend itinerary generation.
- Introduced modular planning agents for attractions, hotels, weather, and final itinerary assembly.
- Added parser utilities for more realistic AMap and MCP-style provider payloads.
- Refactored the frontend into reusable components and composables for result display, export, and state handling.
- Added backend tests for parser behavior and planning orchestration.
- Added project documentation and cleaned repository metadata for public publishing.

## Included In This Release

- Vue 3 + TypeScript frontend
- FastAPI + Pydantic backend
- Fallback planning flow without external API keys
- Session-based result persistence on the frontend
- Export support for PNG and PDF
- Initial GitHub-ready repository structure and documentation

## Notes

- A valid AMap web key is still required for real map rendering.
- If third-party service keys are missing, the application falls back to generated itinerary data.
