from fastapi import FastAPI, HTTPException
from recipe_scrapers import scrape_me, scrape_html

from models import IngredientGroup, RecipeResponse, HtmlRequest, UrlRequest

app = FastAPI(
    title="Recipe Scrapers API",
    description="Web API wrapper for recipe-scrapers library",
    version="0.1.0",
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
        if "https://www.cloudflare.com/privacypolicy/" in request.html:
            raise HTTPException(
                status_code=403,
                detail="Cloudflare protection detected. Cannot process HTML content.",
            )

        scraper = scrape_html(
            html=request.html, org_url=str(request.url), supported_only=False
        )

        if scraper.to_json().get("author") is None:  # type: ignore
            raise HTTPException(
                status_code=422,
                detail="Parsing recipe data failed",
            )

        return RecipeResponse.from_scraper(scraper)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error scraping HTML: {str(e)}")


@app.get("/demo-response", response_model=RecipeResponse)
def get_demo_response() -> RecipeResponse:
    return RecipeResponse(
        author="John Doe",
        canonical_url="https://www.example.com/recipe/123",
        category="Dessert",
        cook_time=30,
        cooking_method=None,
        cuisine="French",
        description="A delicious chocolate cake recipe.",
        dietary_restrictions=["Vegetarian"],
        equipment=["Oven", "Mixing Bowl"],
        host="www.example.com",
        image="https://www.example.com/images/chocolate-cake.jpg",
        ingredient_groups=[
            IngredientGroup(purpose="Cake", ingredients=["2 cups flour", "1 cup sugar"])
        ],
        ingredients=["2 cups flour", "1 cup sugar", "2 eggs"],
        instructions="Mix ingredients and bake.",
        instructions_list=["Mix ingredients.", "Bake at 350F for 30 minutes."],
        language="en",
        keywords=["chocolate", "cake", "dessert"],
        links=[{"rel": "self", "href": "https://www.example.com/recipe/123"}],
        nutrients={"calories": "250 kcal", "protein": "5g"},
        prep_time=15,
        ratings=4.5,
        ratings_count=120,
        site_name="Example Recipes",
        title="Chocolate Cake",
        total_time=45,
        yields="1 cake",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
