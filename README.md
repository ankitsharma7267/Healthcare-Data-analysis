# 🩺 Multi-Disease Prediction System

A B.Tech final-year project that predicts **Diabetes**, **Heart Disease**, and
**Parkinson's Disease** from tabular clinical/voice measurements using
trained machine-learning models, wrapped in an interactive **Streamlit**
web application with a built-in **exploratory data-analysis dashboard**
and **model-performance comparison** page.

---

## ✨ Features

- **Three disease predictors** — Diabetes, Heart Disease, Parkinson's — each backed
  by the best of 5 compared ML algorithms (Logistic Regression, Random Forest,
  SVM, KNN, Decision Tree).
- **Data Analysis Dashboard** — class distribution, feature histograms/box
  plots, correlation heatmaps, and raw data download for each dataset.
- **Model Performance page** — accuracy / precision / recall / F1 / ROC-AUC
  comparison table, bar charts, and a radar chart across all 5 algorithms.
- **Risk-score gauges** — visual confidence meter for every prediction.
- Clean, form-based UI — no coding needed to use it.

---

## 🗂️ Project Structure

```
disease_prediction/
├── app.py                     # Main Streamlit application
├── train_models.py            # Trains & compares models, saves best ones
├── prepare_data.py            # Cleans raw CSVs, adds column headers
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml            # App theme
├── data/
│   ├── diabetes.csv / diabetes_clean.csv
│   ├── heart.csv / heart_clean.csv
│   └── parkinsons.csv / parkinsons_clean.csv
├── models/
│   ├── diabetes_model.pkl
│   ├── heart_model.pkl
│   ├── parkinsons_model.pkl
│   └── model_metrics.json     # All algorithms' metrics, for the dashboard
└── notebooks/
    └── EDA_and_Model_Building.ipynb   # Full walkthrough for your report
```

---

## 🚀 Setup & Run

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Only needed once, or if you change the data) Prepare data & train models
python prepare_data.py
python train_models.py

# 4. Launch the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 📊 Datasets Used

| Disease | Dataset | Records | Features | Source |
|---|---|---|---|---|
| Diabetes | Pima Indians Diabetes | 768 | 8 | National Institute of Diabetes and Digestive and Kidney Diseases |
| Heart Disease | UCI Cleveland Heart Disease | 303 | 13 | UCI Machine Learning Repository |
| Parkinson's | UCI Oxford Parkinson's Voice | 195 | 22 | Max Little, University of Oxford |

---

## 🤖 Model Training Methodology

For each disease:
1. Data is cleaned and split **80/20** into train/test sets (stratified).
2. Features are standardized with `StandardScaler`.
3. **5 algorithms** are trained and evaluated with **5-fold cross-validation**
   on the training set: Logistic Regression, Random Forest, SVM (RBF kernel),
   K-Nearest Neighbors, Decision Tree.
4. The algorithm with the **highest mean cross-validated accuracy** is selected
   as the production model for that disease, then evaluated on the held-out test set.
5. The chosen model + its scaler are pickled to `models/` for the app to load.

Achieved test accuracies (see `models/model_metrics.json` for full detail,
and the "Model Performance" page in the app for live comparison):

| Disease | Best Model | Test Accuracy |
|---|---|---|
| Diabetes | Logistic Regression | ~71–78% |
| Heart Disease | Random Forest | ~82–84% |
| Parkinson's | Random Forest | ~90–92% |

*(Exact numbers depend on the random train/test split seed; re-run
`train_models.py` to reproduce.)*

---

## 🧭 Suggested Extensions (for making this distinctly your own project)

- Add a 4th disease (e.g., breast cancer, chronic kidney disease) using the
  same `train_models.py` pattern.
- Add SHAP/feature-importance explainability to each prediction.
- Add user authentication and a database to store prediction history.
- Deploy to Streamlit Community Cloud, Render, or a college server for your demo.
- Expand the EDA notebook into your formal project report chapters
  (Introduction → Literature Review → Methodology → Results → Conclusion).

---

## ⚠️ Disclaimer

This project is built for **academic and educational purposes only**. It is
**not** a certified medical device and must not be used as a substitute for
professional medical advice, diagnosis, or treatment.
