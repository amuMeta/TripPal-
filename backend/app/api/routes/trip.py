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
                image_url = unsplash_service.get_photo_url(f"{attraction.name} {trip_plan.city}")
                if image_url:
                    attraction.image_url = image_url
        return trip_plan
    except Exception as exc:  # pragma: no cover - API guard rail
        raise HTTPException(status_code=500, detail=f"生成行程计划失败: {exc}") from exc
