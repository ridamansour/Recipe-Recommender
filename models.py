import polars as pl
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from config import MODEL_PATH, MATRIX_PATH
import os

# Load the Parquet dataset
recipes_df: pl.DataFrame = pl.read_parquet("data/recipes.parquet")

# Load or create the TF-IDF vectorizer and matrix
if os.path.exists(MODEL_PATH) and os.path.exists(MATRIX_PATH):
    # Load the pre-trained model and matrix
    vectorizer = joblib.load(MODEL_PATH)
    tfidf_matrix = joblib.load(MATRIX_PATH)
else:
    # Preprocess ingredients
    recipes_df = recipes_df.with_columns(
        (pl.col("ingredients") + " " + pl.col("NER")).str.to_lowercase().alias("ingredients_processed")
    )

    # Create TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(recipes_df["ingredients_processed"].to_list())

    # Save the model and matrix
    os.makedirs("models", exist_ok=True)
    joblib.dump(vectorizer, MODEL_PATH)
    joblib.dump(tfidf_matrix, MATRIX_PATH)