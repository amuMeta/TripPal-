from fastapi import APIRouter, HTTPException

from app.agents.orchestrator import TripPlannerOrchestrator
from app.models.schemas import TripPlan, TripPlanRequest
from app.services.unsplash_service import UnsplashService

router = APIRouter()
trip_planner = TripPlannerOrchestrator()
unsplash_service = UnsplashService()


@router.post("/plan", response_model=TripPlan)
async def plan_trip(request: TripPlanRequest) -> TripPlan:
    try:
        trip_plan = trip_planner.plan_trip(request)
        for day in trip_plan.days:
            for attraction in day.attractions:
                if attraction.image_url:
                    continue
                image_url = unsplash_service.get_photo_url(
                    f"{attraction.name} {trip_plan.city}",
                    fallback_queries=_build_image_queries(trip_plan.city, attraction.category or ""),
                )
                if image_url:
                    attraction.image_url = image_url
        return trip_plan
    except Exception as exc:  # pragma: no cover - API guard rail
        raise HTTPException(status_code=500, detail=f"生成行程计划失败: {exc}") from exc


def _build_image_queries(city: str, category: str) -> list[str]:
    lowered = category.lower()
    if "博物馆" in category or "museum" in lowered:
        topic = "museum architecture"
    elif "公园" in category or "自然" in category or "park" in lowered or "nature" in lowered:
        topic = "park landscape"
    elif "夜" in category or "购物" in category or "market" in lowered:
        topic = "night market"
    else:
        topic = "city landmark"

    return [
        f"{city} travel",
        f"{city} {topic}",
        topic,
        "china travel",
    ]
