import requests

from app.config import settings


class UnsplashService:
    def __init__(self) -> None:
        self.access_key = settings.unsplash_access_key
        self.base_url = "https://api.unsplash.com"

    def get_photo_url(self, query: str, fallback_queries: list[str] | None = None) -> str | None:
        if not self.access_key:
            return None

        queries = [query]
        if fallback_queries:
            queries.extend(fallback_queries)

        for current_query in queries:
            image_url = self._search_once(current_query)
            if image_url:
                return image_url
        return None

    def _search_once(self, query: str) -> str | None:
        try:
            response = requests.get(
                f"{self.base_url}/search/photos",
                params={"query": query, "per_page": 1, "client_id": self.access_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                return data["results"][0]["urls"]["regular"]
        except Exception:
            return None
        return None
