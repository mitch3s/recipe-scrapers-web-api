from fastapi_camelcase import CamelModel
from pydantic import HttpUrl, Field, ConfigDict
from recipe_scrapers import AbstractScraper
from typing import Optional


class UrlRequest(CamelModel):
    url: HttpUrl


class HtmlRequest(CamelModel):
    url: str
    html: str


class IngredientGroup(CamelModel):
    """Model for grouped ingredients"""

    model_config = ConfigDict(populate_by_name=True)

    purpose: Optional[str] = Field(
        None, description="The purpose or name of this ingredient group"
    )
    ingredients: list[str] = Field(
        default_factory=list, description="List of ingredients in this group"
    )


class RecipeResponse(CamelModel):
    """Typed model for recipe data"""

    model_config = ConfigDict(populate_by_name=True)

    author: str = Field(
        description="Recipe author name",
    )
    canonical_url: str = Field(
        description="Canonical URL of the recipe",
    )
    category: Optional[str] = Field(
        None,
        description="Recipe category (e.g., Dessert, Main Course)",
    )
    cook_time: Optional[int] = Field(
        None,
        description="Cooking time in minutes",
    )
    cooking_method: Optional[str] = Field(
        None, description="The method of cooking the recipe"
    )
    cuisine: Optional[str] = Field(
        None, description="Cuisine type (e.g., Italian, French)"
    )
    description: Optional[str] = Field(
        None,
        description="Recipe description",
    )
    dietary_restrictions: Optional[list[str]] = Field(
        None, description="List of dietary restrictions (e.g., Vegan, Gluten-Free)"
    )
    equipment: Optional[list[str]] = Field(
        None,
        description="List of equipment needed for the recipe",
    )
    host: str = Field(
        description="Host domain of the recipe",
    )
    image: Optional[str] = Field(
        None,
        description="URL of the recipe image",
    )
    ingredient_groups: list[IngredientGroup] = Field(
        description="Grouped ingredients",
    )
    ingredients: Optional[list[str]] = Field(
        None, description="List of all ingredients"
    )
    instructions: str = Field(
        description="Recipe instructions as a single string",
    )
    instructions_list: list[str] = Field(
        description="Recipe instructions as a list of steps"
    )
    keywords: Optional[list[str]] = Field(
        None, description="List of keywords associated with the recipe"
    )
    language: Optional[str] = Field(
        None, description="Language code (e.g., 'en', 'fr')"
    )
    links: list[dict[str, str]] = Field(
        default_factory=list[dict[str, str]],
        description="List of links related to the recipe",
    )
    nutrients: dict[str, str] = Field(
        default_factory=dict[str, str], description="Nutritional information"
    )
    prep_time: Optional[int] = Field(
        None,
        description="Preparation time in minutes",
    )
    ratings: Optional[float] = Field(
        None,
        description="Average rating score",
    )
    ratings_count: Optional[int] = Field(
        None,
        description="Number of ratings",
    )
    site_name: Optional[str] = Field(
        None,
        description="Name of the recipe site",
    )
    title: Optional[str] = Field(
        None,
        description="Recipe title",
    )
    total_time: Optional[int] = Field(
        None,
        description="Total time in minutes",
    )
    yields: Optional[str] = Field(
        None, description="Recipe yield (e.g., '4 servings', '1 cake')"
    )

    @classmethod
    def from_scraper(cls, scraper: AbstractScraper) -> "RecipeResponse":
        """Initialize RecipeResponse from AbstractScraper instance"""
        return cls.model_validate(scraper.to_json())
