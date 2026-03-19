# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and follows semantic versioning where practical for this prototype stage.

## [v0.1.0] - 2026-03-19

### Added

- Initial full-stack TripPal project import.
- Vue 3 frontend with trip form, result page, export flow, and map-ready UI modules.
- FastAPI backend with trip planning endpoint and typed Pydantic response models.
- Multi-stage planning structure with orchestrator, attraction, hotel, weather, and planner agents.
- Parser utilities for more realistic AMap/MCP-style payload handling.
- Backend test suite covering orchestrator behavior, parser logic, and API test scaffolding.
- Project documentation via `README.md`.

### Changed

- Refactored backend planning logic from a single mock module into a modular orchestration flow.
- Refactored frontend result page into smaller components and composables.
- Switched frontend result transport from route param payload passing to session storage.
- Improved environment configuration handling and added `.env.example`.
- Refined repository ignore rules to exclude caches, local env files, and generated artifacts.

### Fixed

- Fixed frontend submit flow so trip generation is triggered reliably from the form.
- Fixed backend schema defaults to avoid mutable default list issues.
- Improved fallback itinerary generation when external services are unavailable.
- Cleaned repository artifacts that should not be committed, including local env and cache files.

### Notes

- The project runs without third-party API keys by falling back to generated itinerary data.
- Real map display still requires a valid `VITE_AMAP_WEB_KEY`.
- External MCP/Hello Agents integrations depend on environment setup and network availability.
