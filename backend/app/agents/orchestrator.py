from __future__ import annotations

from app.agents.attraction_agent import AttractionSearchAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.mcp_factory import get_mcp_factory
from app.agents.planner_agent import PlannerAgent
from app.agents.weather_agent import WeatherQueryAgent
from app.models.schemas import TripPlan, TripPlanRequest


class TripPlannerOrchestrator:
    def __init__(self) -> None:
        mcp_factory = get_mcp_factory()
        self.attraction_agent = AttractionSearchAgent(mcp_factory)
        self.weather_agent = WeatherQueryAgent(mcp_factory)
        self.hotel_agent = HotelAgent(mcp_factory)
        self.planner_agent = PlannerAgent()

    def plan_trip(self, request: TripPlanRequest) -> TripPlan:
        attractions = self.attraction_agent.search(request)
        weather_info = self.weather_agent.query(request)
        hotel = self.hotel_agent.recommend(request)
        return self.planner_agent.build_plan(request, attractions, hotel, weather_info)
