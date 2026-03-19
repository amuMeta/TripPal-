import unittest
from unittest.mock import patch

try:
    from fastapi.testclient import TestClient
except ImportError:  # pragma: no cover - optional in local env
    TestClient = None

if TestClient is not None:
    from app.api.main import app
    from app.models.schemas import Budget, DayPlan, TripPlan, WeatherInfo


@unittest.skipIf(TestClient is None, "fastapi.testclient is unavailable in this environment")
class TripApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.routes.trip.unsplash_service.get_photo_url", return_value=None)
    @patch("app.api.routes.trip.trip_planner.plan_trip")
    def test_plan_endpoint_returns_trip_plan(self, mock_plan_trip, _mock_unsplash):
        mock_plan_trip.return_value = TripPlan(
            city="上海",
            start_date="2026-05-01",
            end_date="2026-05-02",
            days=[
                DayPlan(
                    date="2026-05-01",
                    day_index=1,
                    description="第 1 天城市漫步",
                    transportation="公共交通",
                    accommodation="中档酒店",
                    attractions=[],
                    meals=[],
                )
            ],
            weather_info=[
                WeatherInfo(
                    date="2026-05-01",
                    day_weather="晴",
                    night_weather="多云",
                    day_temp=25,
                    night_temp=18,
                )
            ],
            overall_suggestions="适合步行和轻松游览。",
            budget=Budget(
                total_attractions=0,
                total_hotels=500,
                total_meals=120,
                total_transportation=80,
                total=700,
            ),
        )

        response = self.client.post(
            "/api/trip/plan",
            json={
                "city": "上海",
                "start_date": "2026-05-01",
                "end_date": "2026-05-02",
                "days": 2,
                "preferences": "美食",
                "budget": "舒适型",
                "transportation": "公共交通",
                "accommodation": "中档酒店",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["city"], "上海")
        self.assertEqual(payload["budget"]["total"], 700)


if __name__ == "__main__":
    unittest.main()
