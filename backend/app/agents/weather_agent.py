from __future__ import annotations

from datetime import datetime, timedelta

from app.agents.amap_parsers import extract_forecasts, normalize_date
from app.agents.mcp_factory import MCPFactory
from app.models.schemas import TripPlanRequest, WeatherInfo


class WeatherQueryAgent:
    def __init__(self, mcp_factory: MCPFactory) -> None:
        self.mcp_factory = mcp_factory

    def query(self, request: TripPlanRequest) -> list[WeatherInfo]:
        weather = self._query_with_mcp(request)
        return weather or self._fallback_weather(request)

    def _query_with_mcp(self, request: TripPlanRequest) -> list[WeatherInfo]:
        try:
            raw = self.mcp_factory.call(
                "amap_maps_weather",
                {"city": request.city, "extensions": "all"},
            )
        except Exception:
            return []

        items: list[WeatherInfo] = []
        for forecast in extract_forecasts(raw)[: request.days]:
            items.append(
                WeatherInfo(
                    date=normalize_date(forecast.get("date"), request.start_date),
                    day_weather=forecast.get("dayweather") or forecast.get("weather") or "晴",
                    night_weather=forecast.get("nightweather") or forecast.get("weather") or "晴",
                    day_temp=forecast.get("daytemp") or forecast.get("temperature") or 26,
                    night_temp=forecast.get("nighttemp") or forecast.get("temperature_float") or 18,
                )
            )
        return items

    @staticmethod
    def _fallback_weather(request: TripPlanRequest) -> list[WeatherInfo]:
        start = datetime.strptime(request.start_date, "%Y-%m-%d").date()
        template = [
            ("晴", "多云", 26, 18),
            ("多云", "晴", 24, 17),
            ("小雨", "多云", 22, 16),
            ("阴", "晴", 23, 17),
        ]
        result: list[WeatherInfo] = []
        for index in range(request.days):
            day_weather, night_weather, day_temp, night_temp = template[index % len(template)]
            result.append(
                WeatherInfo(
                    date=(start + timedelta(days=index)).isoformat(),
                    day_weather=day_weather,
                    night_weather=night_weather,
                    day_temp=day_temp,
                    night_temp=night_temp,
                )
            )
        return result
