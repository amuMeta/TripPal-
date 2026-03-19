from __future__ import annotations

from datetime import datetime
from typing import Any

from app.models.schemas import Location


def unwrap_payload(raw: Any) -> Any:
    # Some MCP wrappers nest useful data under one or more generic keys.
    # Unwrap only known transport keys so domain payloads are left intact.
    current = raw
    for _ in range(3):
        if isinstance(current, dict) and len(current) == 1:
            only_key, only_value = next(iter(current.items()))
            if only_key not in {"data", "result", "payload"}:
                break
            if isinstance(only_value, (dict, list)):
                current = only_value
                continue
        break
    return current


def extract_pois(raw: Any) -> list[dict[str, Any]]:
    current = unwrap_payload(raw)
    if isinstance(current, dict):
        if isinstance(current.get("pois"), list):
            return [item for item in current["pois"] if isinstance(item, dict)]
        if isinstance(current.get("data"), dict):
            return extract_pois(current["data"])
        if isinstance(current.get("result"), dict):
            return extract_pois(current["result"])
        if isinstance(current.get("results"), list):
            return [item for item in current["results"] if isinstance(item, dict)]
    if isinstance(current, list):
        return [item for item in current if isinstance(item, dict)]
    return []


def extract_forecasts(raw: Any) -> list[dict[str, Any]]:
    current = unwrap_payload(raw)
    if isinstance(current, dict):
        if isinstance(current.get("forecasts"), list) and current["forecasts"]:
            first = current["forecasts"][0]
            if isinstance(first, dict) and isinstance(first.get("casts"), list):
                return [item for item in first["casts"] if isinstance(item, dict)]
            return [item for item in current["forecasts"] if isinstance(item, dict)]
        if isinstance(current.get("lives"), list):
            return [item for item in current["lives"] if isinstance(item, dict)]
        if isinstance(current.get("data"), dict):
            return extract_forecasts(current["data"])
        if isinstance(current.get("result"), dict):
            return extract_forecasts(current["result"])
    return []


def parse_location(value: Any) -> Location | None:
    if isinstance(value, str) and "," in value:
        longitude, latitude = value.split(",", 1)
        return _build_location(longitude, latitude)
    if isinstance(value, dict):
        longitude = value.get("lng") or value.get("lon") or value.get("longitude")
        latitude = value.get("lat") or value.get("latitude")
        if longitude is not None and latitude is not None:
            return _build_location(longitude, latitude)
    if isinstance(value, list) and len(value) >= 2:
        return _build_location(value[0], value[1])
    return None


def parse_rating(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_price(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        digits = "".join(ch for ch in value if ch.isdigit())
        if digits:
            return int(digits)
    return None


def normalize_date(value: Any, fallback: str) -> str:
    if not value:
        return fallback
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date().isoformat()
        except ValueError:
            return value
    return fallback


def _build_location(longitude: Any, latitude: Any) -> Location | None:
    try:
        return Location(longitude=float(longitude), latitude=float(latitude))
    except (TypeError, ValueError):
        return None
