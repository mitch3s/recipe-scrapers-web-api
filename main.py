from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from recipe_scrapers import AbstractScraper, scrape_me, scrape_html
from typing import Any, Optional
from typing import cast

app = FastAPI(
    title="Recipe Scrapers API",
    description="Web API wrapper for recipe-scrapers library",
    version="0.1.0"
)


class UrlRequest(BaseModel):
    url: HttpUrl


class HtmlRequest(BaseModel):
    url: str
    html: str


"""
Recipe response model using Pydantic

Example response:
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
            "ingredients": [
                "2 cups flour",
                "1 cup sugar"
            ]
        }
    ],
    "ingredients": [
        "2 cups flour",
        "1 cup sugar",
        "2 eggs"
    ],
    "instructions": "Mix ingredients and bake.",
    "instructions_list": [
        "Mix ingredients.",
        "Bake at 350F for 30 minutes."
    ],
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
"""
class RecipeResponse(BaseModel):
    """Typed model for recipe data"""
    author: Optional[str] = None
    canonicalUrl: Optional[str] = None
    category: Optional[str] = None
    cookTime: Optional[int] = None
    cuisine: Optional[str] = None
    description: Optional[str] = None
    host: Optional[str] = None
    image: Optional[str] = None
    ingredientGroups: Optional[list[Any]] = None
    ingredients: Optional[list[str]] = None
    instructions: Optional[str] = None
    instructionsList: Optional[list[str]] = None
    language: Optional[str] = None
    nutrients: Optional[dict[str, str]] = None
    prepTime: Optional[int] = None
    ratings: Optional[float] = None
    ratingsCount: Optional[int] = None
    siteName: Optional[str] = None
    title: Optional[str] = None
    totalTime: Optional[int] = None
    yields: Optional[str] = None
    
    @classmethod
    def from_scraper(cls, scraper: AbstractScraper) -> "RecipeResponse":
        """Initialize RecipeResponse from AbstractScraper instance"""

        def _safe_get(method_name: str, cast_type: Any) -> Any:
            """Safely call a scraper method and cast its result, or return None if not available."""
            if hasattr(scraper, method_name):
                method = getattr(scraper, method_name)
                if callable(method):
                    return cast(cast_type, method()) # type: ignore
            return None

        return cls(
            author=_safe_get('author', Optional[str]),
            canonicalUrl=_safe_get('canonical_url', Optional[str]),
            category=_safe_get('category', Optional[str]),
            cookTime=_safe_get('cook_time', Optional[int]),
            cuisine=_safe_get('cuisine', Optional[str]),
            description=_safe_get('description', Optional[str]),
            host=_safe_get('host', Optional[str]),
            image=_safe_get('image', Optional[str]),
            ingredientGroups=_safe_get('ingredient_groups', Optional[list[Any]]),
            ingredients=_safe_get('ingredients', Optional[list[str]]),
            instructions=_safe_get('instructions', Optional[str]),
            instructionsList=_safe_get('instructions_list', Optional[list[str]]),
            language=_safe_get('language', Optional[str]),
            nutrients=_safe_get('nutrients', Optional[dict[str, str]]),
            prepTime=_safe_get('prep_time', Optional[int]),
            ratings=_safe_get('ratings', Optional[float]),
            ratingsCount=_safe_get('ratings_count', Optional[int]),
            siteName=_safe_get('site_name', Optional[str]),
            title=_safe_get('title', Optional[str]),
            totalTime=_safe_get('total_time', Optional[int]),
            yields=_safe_get('yields', Optional[str]),
        )


@app.post("/scrape-url", response_model=RecipeResponse)
def scrape_from_url(request: UrlRequest) -> RecipeResponse:
    """
    Scrape recipe data from a URL using the scrape_me method.
    
    Example:
    ```
    {
        "url": "https://www.allrecipes.com/recipe/123456/example-recipe/"
    }
    ```
    """
    try:
        scraper = scrape_me(str(request.url))
        return RecipeResponse.from_scraper(scraper)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scraping URL: {str(e)}")


@app.post("/scrape-html", response_model=RecipeResponse)
def scrape_from_html(request: HtmlRequest) -> RecipeResponse:
    """
    Scrape recipe data from HTML content using the scrape_html method.
    
    Example:
    ```
    {
        "url": "https://www.allrecipes.com/recipe/123456/example-recipe/",
        "html": "<html>...</html>"
    }
    ```
    """
    try:

        # write to file
        with open("test.html", "w", encoding="utf-8") as file:
            file.write(request.html)

        scraper = scrape_html(html=request.html, org_url=str(request.url))
        return RecipeResponse.from_scraper(scraper)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scraping HTML: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
