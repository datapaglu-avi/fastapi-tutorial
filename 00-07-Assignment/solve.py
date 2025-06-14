from typing import Annotated, Literal
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
import datetime


dummy_data = [
  {
    "id": 1,
    "title": "OpenAI launches GPT-4.5",
    "category": "technology",
    "media_house": "TechCrunch",
    "updated_at": "2025-06-12T10:00:00",
    "summary": "OpenAI has announced...",
    "keywords": ["AI", "GPT", "OpenAI"]
  },
  {
    "id": 2,
    "title": "New advancements in quantum computing",
    "category": "science",
    "media_house": "Science Daily",
    "updated_at": "2025-06-11T15:30:00",
    "summary": "Researchers have made significant progress...",
    "keywords": ["quantum", "computing", "research"]
  },
 {
    "id": 3,
    "title": "Global economic outlook for 2025",
    "category": "business",
    "media_house": "Financial Times",
    "updated_at": "2025-06-10T08:45:00",
    "summary": "The global economy is expected to...",
    }
]


app = FastAPI(title="NewsAPI", description="A simple clone for NewsAPI", version="0.1.0")

class NewsFilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # Forbid unknown/extra query params (useful in strict APIs)

    media_house: Annotated[str|None, Query(alias='media-house')] = None  # Filter by media house name
    category: str|None = None  # Filter by news category
    updated_after: datetime.datetime|None = None  # Filter news updated after this datetime
    keyword: str|None = None
    limit: int = Field(10, le=50)
    offset: int = Field(0, le=50)


@app.get('/news')
async def get_news(news_filter: Annotated[NewsFilterParams, Query()]): # annotated with Query to extract query parameters and not as request body
    filtered_news = dummy_data

    if news_filter.media_house:
        filtered_news = [news for news in filtered_news if news['media_house'] == news_filter.media_house]

    if news_filter.category:
        filtered_news = [news for news in filtered_news if news['category'] == news_filter.category]

    if news_filter.updated_after:
        filtered_news = [news for news in filtered_news if datetime.datetime.fromisoformat(news['updated_at']) > news_filter.updated_after]

    if news_filter.keyword:
        filtered_news = [news for news in filtered_news if news_filter.keyword.lower() in list(map(str.lower, news.get('keywords', [])))]

    return filtered_news[news_filter.offset:news_filter.offset + news_filter.limit]


@app.get('/news/{news_id}')
async def get_news_by_id(news_id: Annotated[int, Path(ge=1)]):
    for news in dummy_data:
        if news['id'] == news_id:
            return news
    return {"error": "News not found"}
