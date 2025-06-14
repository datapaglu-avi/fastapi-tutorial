# 🧠 Assignment: Build a Minimal News API (Ch. 0–7)

Your goal is to build a basic News API using FastAPI, applying all concepts from Chapters 0 to 7.  
This project will also become the foundation for NewsAPI clone

---

## 📂 Assumptions

You already have a static `news_data.json` file with this structure:

```
[
  {
    "id": 1,
    "title": "OpenAI launches GPT-4.5",
    "category": "technology",
    "media_house": "TechCrunch",
    "updated_at": "2025-06-12T10:00:00",
    "summary": "OpenAI has announced...",
    "keywords": ["AI", "GPT", "OpenAI"]
  }
]
```

---

## ✅ Requirements

### 🔹 1. Endpoint: `/news/` (GET)

Supports **query parameters** to filter:

| Parameter        | Type       | Notes                                               |
|------------------|------------|-----------------------------------------------------|
| `media_house`    | `str`      | Optional. Exact match. Alias: `media-house`         |
| `category`       | `str`      | Optional. Exact match                               |
| `updated_after`  | `datetime` | Optional. Must be valid ISO string                  |
| `keyword`        | `str`      | Optional. Should match at least one keyword         |
| `limit`          | `int`      | Optional. Default = 10, Max = 50                    |
| `offset`         | `int`      | Optional. Default = 0                               |

---

### 🔹 2. Pydantic Models

- `NewsFilterParams` (for query parameters)
- `NewsItem` (for output JSON format)

Use `Annotated` and `Query` with metadata, aliases, and validation constraints.  
Reject extra query parameters using:

```python
model_config = {"extra": "forbid"}
```

---

### 🔹 3. Endpoint: `/news/{news_id}` (GET)

- Use `Path()` to validate `news_id >= 1`
- Return a single article matching that ID

---

## ✨ Bonus (Optional)

Support sorting:

| Parameter | Values           |
|-----------|------------------|
| `sort_by` | `updated_at`     |
| `order`   | `asc` / `desc`   |

---

## 🧪 Example Queries

```
/news/?media-house=TechCrunch&category=technology&limit=5
/news/?keyword=AI&updated_after=2025-06-01T00:00:00
/news/3
```

---

## 💡 Future Enhancements (Later Chapters)

- Add voting system (`/news/{id}/vote?type=fake/speculative/real`)
- Add comments per article (`/news/{id}/comments`)
- Add moderation/flagging system
