from flask import Flask, render_template, request, flash, redirect, url_for
from sklearn.metrics.pairwise import cosine_similarity
import polars as pl

from database import get_db_connection, init_db
from models import recipes_df, vectorizer, tfidf_matrix
from nutrition import get_nutrition
from utils import split_ingredients, split_instructions
from config import DATABASE

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# Initialize the database
init_db()

@app.route("/")
def home():
    """
    Render the home page with the user's food items and available tags.

    Returns:
        str: The rendered HTML template for the home page.
    """
    user_id = "default_user"  # Replace with actual user ID in a real app
    with get_db_connection() as conn:
        food_items = conn.execute("SELECT food_item FROM user_food WHERE user_id = ?", (user_id,)).fetchall()

    # Get unique meal courses and dietary tags from the dataset
    meal_courses = [col.replace("meal_course_", "") for col in recipes_df.columns if col.startswith("meal_course_")]
    dietary_tags = [col.replace("dietary_tags_", "") for col in recipes_df.columns if col.startswith("dietary_tags_")]

    return render_template("index.html", food_items=food_items, meal_course_tags=meal_courses, dietary_tags=dietary_tags)

@app.route("/add_food", methods=["POST"])
def add_food():
    """
    Add food items to the user's food list.

    Returns:
        Response: A redirect to the home page.
    """
    user_id = "default_user"  # Replace with actual user ID in a real app
    food_input = request.form["food_item"].strip().lower()  # Get the input and normalize it

    if not food_input:
        flash("Food item cannot be empty!", "error")
    else:
        # Split the input by commas and strip whitespace
        food_items = [item.strip() for item in food_input.split(",")]

        # Add each food item individually
        with get_db_connection() as conn:
            for food_item in food_items:
                if food_item:  # Ensure the item is not empty
                    conn.execute(
                        "INSERT INTO user_food (user_id, food_item) VALUES (?, ?)",
                        (user_id, food_item),
                    )
            conn.commit()

        # Flash a success message
        flash(f"Added {len(food_items)} item(s) to your food list!", "success")

    return redirect(url_for("home"))

@app.route("/remove_food", methods=["POST"])
def remove_food():
    """
    Remove selected food items from the user's food list.

    Returns:
        Response: A redirect to the home page.
    """
    user_id = "default_user"  # Replace with actual user ID in a real app
    food_items_to_remove = request.form.getlist("food_items")

    if not food_items_to_remove:
        flash("No food items selected for removal!", "error")
    else:
        with get_db_connection() as conn:
            for food_item in food_items_to_remove:
                conn.execute("DELETE FROM user_food WHERE user_id = ? AND food_item = ?", (user_id, food_item))
            conn.commit()
        flash(f"Removed {len(food_items_to_remove)} food item(s)!", "success")

    return redirect(url_for("home"))

@app.route("/recommend", methods=["POST"])
def recommend() -> str:
    """
    Generate recipe recommendations based on the user's food items and selected filters.

    Returns:
        str: The rendered HTML template for the recommendation page.
    """
    user_id = "default_user"  # Replace it with actual user ID in a real app

    # Get user's food items from the database
    with get_db_connection() as conn:
        food_items = conn.execute("SELECT food_item FROM user_food WHERE user_id = ?", (user_id,)).fetchall()

    # Combine food items into a single string
    user_ingredients = ", ".join(item["food_item"] for item in food_items).lower()

    # Transform user input into TF-IDF vector
    user_tfidf = vectorizer.transform([user_ingredients])

    # Calculate cosine similarity for all recipes
    similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

    # Add similarity scores to the original DataFrame
    global recipes_df
    recipes_df = recipes_df.with_columns(pl.Series("similarity", similarities))

    # Create a copy of the DataFrame for filtering
    filtered_df = recipes_df.clone()

    # Filter by meal course (if provided)
    meal_courses = request.form.getlist("meal_course_tags")
    if meal_courses:
        # Apply filter for each selected meal course
        for course in meal_courses:
            filtered_df = filtered_df.filter(pl.col(f"meal_course_{course}") == 1)

    # Filter by dietary tag (if provided)
    dietary_tags = request.form.getlist("dietary_tags")
    if dietary_tags:
        # Apply filter for each selected dietary tag
        for tag in dietary_tags:
            filtered_df = filtered_df.filter(pl.col(f"dietary_tags_{tag}") == 1)

    # Sort the filtered DataFrame by similarity and get the top 5 recipes
    top_recipes = filtered_df.sort("similarity", descending=True).head(5)

    # Add nutritional data and tags to each recipe
    recipes_with_nutrition = []
    for recipe in top_recipes.to_dicts():
        # Split ingredients and instructions by "|"
        if isinstance(recipe["ingredients"], str):
            recipe["ingredients"] = split_ingredients(recipe["ingredients"])
        if isinstance(recipe["instructions"], str):
            recipe["instructions"] = split_instructions(recipe["instructions"])

        # Add nutrition data
        recipe["nutrition"] = get_nutrition(recipe["name"])

        # Extract all meal course tags
        meal_tags = [course.replace("meal_course_", "") for course in recipes_df.columns
                     if course.startswith("meal_course_") and recipe.get(course) == 1]

        # Extract all dietary tags
        diet_tags = [tag.replace("dietary_tags_", "") for tag in recipes_df.columns
                     if tag.startswith("dietary_tags_") and recipe.get(tag) == 1]

        recipe["meal_tags"] = meal_tags
        recipe["diet_tags"] = diet_tags

        recipes_with_nutrition.append(recipe)

    return render_template("recommendations.html", recipes=recipes_with_nutrition)