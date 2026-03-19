import unittest

from app.agents.orchestrator import TripPlannerOrchestrator
from app.models.schemas import TripPlanRequest


class OrchestratorTestCase(unittest.TestCase):
    def test_plan_trip_returns_complete_plan(self):
        request = TripPlanRequest(
            city="杭州",
            start_date="2026-04-01",
            end_date="2026-04-03",
            days=3,
            preferences="美食和城市漫步",
            budget="舒适型",
            transportation="公共交通",
            accommodation="中档酒店",
        )

        plan = TripPlannerOrchestrator().plan_trip(request)

        self.assertEqual(plan.city, "杭州")
        self.assertEqual(len(plan.days), 3)
        self.assertTrue(plan.days[0].attractions)
        self.assertIsNotNone(plan.budget)
        self.assertGreater(plan.budget.total, 0)


if __name__ == "__main__":
    unittest.main()
