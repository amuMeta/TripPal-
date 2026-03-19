from __future__ import annotations

from app.agents.amap_parsers import extract_pois, parse_location, parse_price, parse_rating
from app.agents.mcp_factory import MCPFactory
from app.models.schemas import Attraction, Location, TripPlanRequest


class AttractionSearchAgent:
    def __init__(self, mcp_factory: MCPFactory) -> None:
        self.mcp_factory = mcp_factory

    def search(self, request: TripPlanRequest) -> list[Attraction]:
        results = self._search_with_mcp(request)
        return results or self._fallback_attractions(request)

    def _search_with_mcp(self, request: TripPlanRequest) -> list[Attraction]:
        queries = self._build_queries(request)
        seen: set[str] = set()
        attractions: list[Attraction] = []

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

            for poi in extract_pois(raw):
                attraction = self._build_attraction(poi, request)
                if attraction is None:
                    continue
                unique_key = f"{attraction.name}|{attraction.address}"
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                attractions.append(attraction)
                if len(attractions) >= max(request.days * 4, 6):
                    return attractions
        return attractions

    def _build_attraction(self, poi: dict, request: TripPlanRequest) -> Attraction | None:
        location = parse_location(poi.get("location"))
        if location is None:
            return None

        category = poi.get("type") or poi.get("typecode") or poi.get("biz_type") or "景点"
        ticket_price = (
            parse_price(poi.get("ticket_ordering"))
            or parse_price(poi.get("cost"))
            or parse_price(poi.get("ticket_price"))
            or 0
        )
        duration = 120
        if "博物馆" in category or "展览" in category:
            duration = 180
        elif "公园" in category or "自然" in category or "风景" in category:
            duration = 240

        district = poi.get("pname") or poi.get("cityname") or request.city
        short_desc = poi.get("type") or poi.get("tag") or "城市热门景点"
        return Attraction(
            name=poi.get("name") or "推荐景点",
            address=poi.get("address") or district,
            location=location,
            visit_duration=duration,
            description=f"位于{district}，适合安排为{short_desc}主题游览。",
            category=category.split(";")[0],
            rating=parse_rating((poi.get("biz_ext") or {}).get("rating") or poi.get("rating")),
            ticket_price=ticket_price,
        )

    @staticmethod
    def _build_queries(request: TripPlanRequest) -> list[str]:
        base = [request.preferences.strip(), f"{request.city} 景点", f"{request.city} {request.preferences.strip()}"]
        return [item for item in base if item and item.strip()]

    @staticmethod
    def _fallback_attractions(request: TripPlanRequest) -> list[Attraction]:
        return [
            Attraction(
                name=f"{request.city} 城市地标",
                address=f"{request.city} 市中心",
                location=Location(longitude=120.1551, latitude=30.2741),
                visit_duration=120,
                description="适合第一天熟悉城市节奏和主要动线。",
                category="城市观光",
                rating=4.6,
                ticket_price=0,
            ),
            Attraction(
                name=f"{request.city} 博物馆",
                address=f"{request.city} 文化区",
                location=Location(longitude=120.1612, latitude=30.2523),
                visit_duration=180,
                description="适合半日的文化历史主题游览。",
                category="文化历史",
                rating=4.7,
                ticket_price=50,
            ),
            Attraction(
                name=f"{request.city} 风景公园",
                address=f"{request.city} 景观带",
                location=Location(longitude=120.1434, latitude=30.2361),
                visit_duration=240,
                description="适合步行、拍照和慢节奏游览。",
                category="自然风光",
                rating=4.5,
                ticket_price=30,
            ),
            Attraction(
                name=f"{request.city} 夜游商圈",
                address=f"{request.city} 热门商圈",
                location=Location(longitude=120.1768, latitude=30.2576),
                visit_duration=150,
                description="适合安排晚间餐饮和自由活动。",
                category="休闲购物",
                rating=4.4,
                ticket_price=0,
            ),
        ]
