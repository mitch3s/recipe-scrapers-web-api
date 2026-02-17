# Recipe Scrapers Web API

Small web API wrapper around [hhursev/recipe-scrapers](https://github.com/hhursev/recipe-scrapers).

## Installation

```bash
uv sync
```

## Running the API

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs are available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

```bash
# Scrape from URL
curl -X POST "http://localhost:8000/scrape-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/12345/example/"}'

# Scrape from HTML
curl -X POST "http://localhost:8000/scrape-html" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/12345/", "html": "<html>...</html>"}'
```

## Response

The response looks like this:

```json
{
  "author": "John Doe",
  "canonical_url": "https://www.example.com/recipe/123",
  "category": "Dessert",
  "cook_time": 30,
  "cuisine": "French",
  "description": "A delicious chocolate cake recipe.",
  "host": "www.example.com",
  "image": "https://www.example.com/images/chocolate-cake.jpg",
  "ingredient_groups": [
    {
      "group_name": "Cake",
      "ingredients": ["2 cups flour", "1 cup sugar"]
    }
  ],
  "ingredients": ["2 cups flour", "1 cup sugar", "2 eggs"],
  "instructions": "Mix ingredients and bake.",
  "instructions_list": ["Mix ingredients.", "Bake at 350F for 30 minutes."],
  "language": "en",
  "nutrients": {
    "calories": "250 kcal",
    "protein": "5g"
  },
  "prep_time": 15,
  "ratings": 4.5,
  "ratings_count": 120,
  "site_name": "Example Recipes",
  "title": "Chocolate Cake",
  "total_time": 45,
  "yields": "1 cake"
}
```

# Docker

```
docker build -t recipe-scrapers-api .
docker run -p 8000:8000 recipe-scrapers-api
```
