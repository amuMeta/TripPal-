from app.agents.mcp_factory import get_mcp_factory


def test_amap_search():
    return get_mcp_factory().call(
        "amap_maps_text_search",
        {
            "keywords": "北京故宫",
            "city": "北京",
            "children": 1,
            "page": 1,
            "extensions": "base",
        },
    )


def test_amap_weather():
    return get_mcp_factory().call(
        "amap_maps_weather",
        {
            "city": "北京",
            "extensions": "base",
        },
    )


if __name__ == "__main__":
    print("search:", test_amap_search())
    print("weather:", test_amap_weather())
