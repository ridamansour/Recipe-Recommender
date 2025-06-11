import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
MODEL_PATH = "models/tfidf_vectorizer.pkl"
MATRIX_PATH = "models/tfidf_matrix.pkl"
DATABASE = "user_food.db"

# API Keys
CALORIE_NINJAS_API_KEY = os.getenv("CALORIE_NINJAS_API_KEY")