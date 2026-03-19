from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")


class Attraction(BaseModel):
    name: str = Field(..., description="景点名称")
    address: str = Field(..., description="地址")
    location: Location
    visit_duration: int = Field(..., gt=0, description="建议游览时长（分钟）")
    description: str
    category: Optional[str] = "景点"
    rating: Optional[float] = Field(None, ge=0, le=5)
    image_url: Optional[str] = None
    ticket_price: int = Field(default=0, ge=0)


class Meal(BaseModel):
    type: str = Field(..., description="breakfast/lunch/dinner/snack")
    name: str
    address: Optional[str] = None
    location: Optional[Location] = None
    estimated_cost: int = 0


class Hotel(BaseModel):
    name: str
    address: str
    location: Optional[Location] = None
    price_range: str
    rating: str
    estimated_cost: int = 0


class Budget(BaseModel):
    total_attractions: int = 0
    total_hotels: int = 0
    total_meals: int = 0
    total_transportation: int = 0
    total: int = 0


class WeatherInfo(BaseModel):
    date: str
    day_weather: str
    night_weather: str
    day_temp: int
    night_temp: int

    @field_validator("day_temp", "night_temp", mode="before")
    @classmethod
    def parse_temperature(cls, value: int | str) -> int:
        if isinstance(value, str):
            cleaned = value.replace("°C", "").replace("掳C", "").strip()
            return int(cleaned)
        return value


class DayPlan(BaseModel):
    date: str
    day_index: int
    description: str
    transportation: str
    accommodation: str
    hotel: Optional[Hotel] = None
    attractions: List[Attraction] = Field(default_factory=list)
    meals: List[Meal] = Field(default_factory=list)


class TripPlan(BaseModel):
    city: str
    start_date: str
    end_date: str
    days: List[DayPlan] = Field(default_factory=list)
    weather_info: List[WeatherInfo] = Field(default_factory=list)
    overall_suggestions: str
    budget: Optional[Budget] = None


class TripPlanRequest(BaseModel):
    city: str
    start_date: str
    end_date: str
    days: int
    preferences: str
    budget: str
    transportation: str
    accommodation: str
