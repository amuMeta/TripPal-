import requests

from app.config import settings


class UnsplashService:
    def __init__(self) -> None:
        self.access_key = settings.unsplash_access_key
        self.base_url = "https://api.unsplash.com"

    def get_photo_url(self, query: str) -> str | None:
        if not self.access_key:
            return None

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
