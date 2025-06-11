import requests
from functools import lru_cache
from config import CALORIE_NINJAS_API_KEY


@lru_cache(maxsize=128)
def get_nutrition(recipe_name: str, debug=False) -> dict:
    """
    Fetch nutritional data for a recipe using the CalorieNinjas API.

    Args:
        recipe_name (str): The name of the recipe to fetch nutrition data for.
        debug (bool): If True, return placeholder data instead of making an API call.

    Returns:
        dict: A dictionary containing nutritional data for the recipe.
    """
    if not debug:
        api_url = "https://api.calorieninjas.com/v1/nutrition?query="
        response = requests.get(
            api_url + recipe_name,
            headers={"X-Api-Key": CALORIE_NINJAS_API_KEY}
        )
        if response.status_code == requests.codes.ok:
            print(response.json())
            try:
                return response.json()["items"][0]
            except Exception as e:
                print(e)
        print("Error:", response.status_code, response.text)
    return {
        "name": recipe_name,
        "calories": -1,
        "serving_size_g": -1,
        "fat_total_g": -1,
        "fat_saturated_g": -1,
        "protein_g": -1,
        "sodium_mg": -1,
        "potassium_mg": -1,
        "cholesterol_mg": -1,
        "carbohydrates_total_g": -1,
        "fiber_g": -1,
        "sugar_g": -1
    }