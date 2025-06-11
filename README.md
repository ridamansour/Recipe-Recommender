# 🧠 Smart Recipe Recommender

A Flask-based web app that recommends recipes based on ingredients you have, using natural language processing (TF-IDF), and provides nutritional info via API.

---

## 🚀 Features

- 🧾 **Smart Recipe Matching**  
  Uses TF-IDF to recommend recipes based on ingredient similarity.

- 📊 **Massive Dataset**  
  Backed by a dataset of **over 2 million recipes**, enabling diverse and accurate suggestions.

- 🧂 **Ingredient Parsing**  
  Parses and normalizes ingredients to enhance match accuracy.

- 🥗 **Nutrition Data**  
  Fetches nutrition info for recommended recipes via external API.

- 🧰 **Modular Architecture**  
  Clean separation of concerns with `routes`, `models`, `utils`, and `database`.

---

## 🗂️ Project Structure

```

.
├── app.py                  # Flask entry point
├── routes.py              # Main application routes
├── models.py              # TF-IDF model loading/creation
├── database.py            # DB connection + init
├── nutrition.py           # Nutrition API fetch logic
├── utils.py               # Ingredient/instruction parsing
├── config.py              # Constants and environment paths
├── testyy.ipynb           # Dataset manipulations 
├── data/
│   └── recipes.parquet    # Recipe dataset
├── models/
│   ├── tfidf_vectorizer.pkl
│   └── tfidf_matrix.pkl
├── templates/
│   ├── index.html
│   ├── manage_food.html
│   └── recommendations.html
├── .env                   # API keys
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ridamansour/smart-recipe-recommender.git
cd smart-recipe-recommender
````

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file in the project root:

```env
NUTRITION_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
python app.py
```

App runs at `http://127.0.0.1:5000`.

---

## 🧠 How It Works

* **TF-IDF Vectorization**
  Recipe ingredients are transformed using TF-IDF; cosine similarity scores suggest the closest matches.

* **Ingredient Matching**
  Input ingredients are matched against dataset recipes using cosine similarity.

* **Nutrition Lookup**
  Once a recipe is chosen, its ingredients are sent to a nutrition API for real-time analysis.

---

## 📦 Dependencies (requirements.txt)

```txt
Flask
joblib
requests
scikit-learn
python-dotenv
polars
```

---

## 🛣️ Route Overview

| Route              | Method | Description                     |
| ------------------ | ------ | ------------------------------- |
| `/`                | GET    | Home page with ingredient input |
| `/recommendations` | POST   | Shows top recipe matches        |

---

## 🔮 Future Improvements

* [ ] User accounts for saving preferences
* [ ] Ingredient auto-suggestions with autocomplete
* [ ] Support for allergies and dietary restrictions
* [ ] Mobile-first redesign

---

## 📸 Screenshots


<img src="./screenshots/Smart Recipe Recommender.png" alt="Recipe Recommender Home page" width="1000"/>
<img src="./screenshots/Recipe Recommendations.png" alt="Recommendaions" width="1000"/>

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b new-feature`
3. Commit: `git commit -m 'add feature'`
4. Push: `git push origin new-feature`
5. Open a Pull Request

---

## 📜 License

Open-sourced.
