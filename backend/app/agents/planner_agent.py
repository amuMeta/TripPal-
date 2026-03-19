from __future__ import annotations

from datetime import datetime, timedelta

from app.models.schemas import Attraction, Budget, DayPlan, Hotel, Meal, TripPlan, TripPlanRequest, WeatherInfo


class PlannerAgent:
    def build_plan(
        self,
        request: TripPlanRequest,
        attractions: list[Attraction],
        hotel: Hotel,
        weather_info: list[WeatherInfo],
    ) -> TripPlan:
        days = self._build_days(request, attractions, hotel)
        budget = self._build_budget(days, hotel)
        return TripPlan(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
            days=days,
            weather_info=weather_info,
            overall_suggestions=self._overall_suggestions(request, weather_info),
            budget=budget,
        )

    def _build_days(self, request: TripPlanRequest, attractions: list[Attraction], hotel: Hotel) -> list[DayPlan]:
        start = datetime.strptime(request.start_date, "%Y-%m-%d").date()
        group_size = max(1, (len(attractions) + request.days - 1) // max(request.days, 1))
        days: list[DayPlan] = []

        for index in range(request.days):
            date_str = (start + timedelta(days=index)).isoformat()
            begin = index * group_size
            end = begin + group_size
            day_attractions = attractions[begin:end] or attractions[: min(2, len(attractions))]
            days.append(
                DayPlan(
                    date=date_str,
                    day_index=index + 1,
                    description=f"第 {index + 1} 天围绕 {request.preferences or '城市经典体验'} 安排行程。",
                    transportation=request.transportation,
                    accommodation=request.accommodation,
                    hotel=hotel,
                    attractions=day_attractions,
                    meals=self._build_meals(request, hotel.address),
                )
            )
        return days

    @staticmethod
    def _build_meals(request: TripPlanRequest, area: str) -> list[Meal]:
        meal_cost = {"经济型": 50, "舒适型": 90, "豪华型": 160}.get(request.budget, 90)
        return [
            Meal(type="breakfast", name="酒店早餐", address=area, estimated_cost=meal_cost // 2),
            Meal(type="lunch", name=f"{request.city} 特色午餐", address=area, estimated_cost=meal_cost),
            Meal(type="dinner", name=f"{request.city} 特色晚餐", address=area, estimated_cost=meal_cost + 20),
        ]

    @staticmethod
    def _build_budget(days: list[DayPlan], hotel: Hotel) -> Budget:
        total_attractions = sum(attraction.ticket_price for day in days for attraction in day.attractions)
        total_meals = sum(meal.estimated_cost for day in days for meal in day.meals)
        total_hotels = hotel.estimated_cost * len(days)
        total_transportation = 80 * len(days)
        return Budget(
            total_attractions=total_attractions,
            total_hotels=total_hotels,
            total_meals=total_meals,
            total_transportation=total_transportation,
            total=total_attractions + total_hotels + total_meals + total_transportation,
        )

    @staticmethod
    def _overall_suggestions(request: TripPlanRequest, weather_info: list[WeatherInfo]) -> str:
        weather_hint = ""
        if weather_info:
            weather_hint = f"首日天气为 {weather_info[0].day_weather}，建议提前准备合适衣物。"
        return (
            f"本次行程以 {request.preferences or '经典游'} 为主，"
            f"整体按 {request.budget} 预算和 {request.transportation} 出行方式安排。"
            f"{weather_hint}"
        )
