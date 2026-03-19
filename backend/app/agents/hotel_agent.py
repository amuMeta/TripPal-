from __future__ import annotations

from app.agents.amap_parsers import extract_pois, parse_location, parse_price, parse_rating
from app.agents.mcp_factory import MCPFactory
from app.models.schemas import Hotel, Location, TripPlanRequest


class HotelAgent:
    def __init__(self, mcp_factory: MCPFactory) -> None:
        self.mcp_factory = mcp_factory

    def recommend(self, request: TripPlanRequest) -> Hotel:
        hotel = self._recommend_with_mcp(request)
        return hotel or self._fallback_hotel(request)

    def _recommend_with_mcp(self, request: TripPlanRequest) -> Hotel | None:
        queries = [f"{request.accommodation} 酒店", "酒店", "住宿"]
        for keywords in queries:
            try:
                raw = self.mcp_factory.call(
                    "amap_maps_text_search",
                    {
                        "keywords": keywords,
                        "city": request.city,
                        "children": 1,
                        "page": 1,
                        "offset": 10,
                        "extensions": "all",
                    },
                )
            except Exception:
                continue

            hotels = [self._build_hotel(poi, request) for poi in extract_pois(raw)]
            hotels = [hotel for hotel in hotels if hotel is not None]
            if hotels:
                hotels.sort(key=lambda item: abs(item.estimated_cost - self._nightly_cost(request.budget)))
                return hotels[0]
        return None

    def _build_hotel(self, poi: dict, request: TripPlanRequest) -> Hotel | None:
        location = parse_location(poi.get("location")) or Location(longitude=120.1551, latitude=30.2741)
        nightly_cost = (
            parse_price((poi.get("biz_ext") or {}).get("cost"))
            or parse_price(poi.get("cost"))
            or self._nightly_cost(request.budget)
        )
        rating = parse_rating((poi.get("biz_ext") or {}).get("rating") or poi.get("rating")) or 4.4
        district = poi.get("pname") or poi.get("cityname") or request.city
        return Hotel(
            name=poi.get("name") or f"{request.city} 推荐酒店",
            address=poi.get("address") or district,
            location=location,
            price_range=self._price_range_from_cost(nightly_cost),
            rating=f"{rating:.1f}",
            estimated_cost=nightly_cost,
        )

    @staticmethod
    def _nightly_cost(budget: str) -> int:
        mapping = {"经济型": 350, "舒适型": 700, "豪华型": 1200}
        return mapping.get(budget, 700)

    @staticmethod
    def _price_range_from_cost(cost: int) -> str:
        low = max(cost - 120, 0)
        high = cost + 180
        return f"{low}-{high} 元/晚"

    @classmethod
    def _fallback_hotel(cls, request: TripPlanRequest) -> Hotel:
        nightly_cost = cls._nightly_cost(request.budget)
        return Hotel(
            name=f"{request.city}{request.accommodation}推荐酒店",
            address=f"{request.city} 市中心交通便利区域",
            location=Location(longitude=120.1625, latitude=30.2677),
            price_range=cls._price_range_from_cost(nightly_cost),
            rating="4.5",
            estimated_cost=nightly_cost,
        )
