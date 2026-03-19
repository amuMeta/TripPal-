import unittest

from app.agents.amap_parsers import extract_forecasts, extract_pois, parse_location


class AmapParserTestCase(unittest.TestCase):
    def test_extract_pois_supports_nested_result_shape(self):
        raw = {
            "result": {
                "data": {
                    "pois": [
                        {"name": "拙政园", "location": "120.635,31.324"},
                        {"name": "平江路", "location": "120.629,31.316"},
                    ]
                }
            }
        }

        pois = extract_pois(raw)

        self.assertEqual(len(pois), 2)
        self.assertEqual(pois[0]["name"], "拙政园")

    def test_extract_forecasts_supports_amap_shape(self):
        raw = {
            "data": {
                "forecasts": [
                    {
                        "casts": [
                            {"date": "2026-04-10", "dayweather": "晴", "nightweather": "多云"},
                            {"date": "2026-04-11", "dayweather": "阴", "nightweather": "晴"},
                        ]
                    }
                ]
            }
        }

        forecasts = extract_forecasts(raw)

        self.assertEqual(len(forecasts), 2)
        self.assertEqual(forecasts[1]["dayweather"], "阴")

    def test_parse_location_accepts_string_and_dict(self):
        from_string = parse_location("120.635,31.324")
        from_dict = parse_location({"lng": "120.629", "lat": "31.316"})

        self.assertIsNotNone(from_string)
        self.assertIsNotNone(from_dict)
        self.assertAlmostEqual(from_string.longitude, 120.635)
        self.assertAlmostEqual(from_dict.latitude, 31.316)


if __name__ == "__main__":
    unittest.main()
