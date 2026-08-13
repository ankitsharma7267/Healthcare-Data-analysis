"""Generates notebooks/EDA_and_Model_Building.ipynb"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

md("""# Multi-Disease Prediction System — EDA & Model Building
### B.Tech Final Year Project

This notebook walks through the exploratory data analysis and model-building
process for three disease-prediction tasks:

1. **Diabetes** (Pima Indians Diabetes dataset)
2. **Heart Disease** (UCI Cleveland dataset)
3. **Parkinson's Disease** (UCI Oxford voice dataset)

Use this notebook as the basis for your project report's "Methodology" and
"Results" chapters — every plot and metric here can be dropped straight into
your report with a screenshot or exported figure.
""")

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix, roc_curve, auc)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)
RANDOM_STATE = 42
""")

md("---\n## 1. Diabetes Dataset")

code("""diabetes = pd.read_csv("../data/diabetes_clean.csv")
diabetes.head()
""")

code("""diabetes.info()
diabetes.describe()
""")

code("""print("Missing values (encoded as 0 in several columns):")
zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for c in zero_cols:
    print(f"  {c}: {(diabetes[c] == 0).sum()} zero entries")
""")

code("""fig, ax = plt.subplots()
diabetes["Outcome"].value_counts().plot(kind="bar", color=["#16A34A", "#DC2626"], ax=ax)
ax.set_xticklabels(["No Diabetes", "Diabetes"], rotation=0)
ax.set_title("Class Distribution — Diabetes")
plt.show()
""")

code("""corr = diabetes.corr()
plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0)
plt.title("Correlation Heatmap — Diabetes")
plt.show()
""")

code("""fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for ax, col in zip(axes.flat, diabetes.columns[:-1]):
    sns.histplot(data=diabetes, x=col, hue="Outcome", kde=True, ax=ax, palette=["#16A34A", "#DC2626"])
    ax.set_title(col)
plt.tight_layout()
plt.show()
""")

md("---\n## 2. Heart Disease Dataset")

code("""heart = pd.read_csv("../data/heart_clean.csv")
heart.head()
""")

code("""heart.info()
heart.describe()
""")

code("""fig, ax = plt.subplots()
heart["target"].value_counts().plot(kind="bar", color=["#16A34A", "#DC2626"], ax=ax)
ax.set_xticklabels(["No Disease", "Disease"], rotation=0)
ax.set_title("Class Distribution — Heart Disease")
plt.show()
""")

code("""plt.figure(figsize=(11, 9))
sns.heatmap(heart.corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
plt.title("Correlation Heatmap — Heart Disease")
plt.show()
""")

md("---\n## 3. Parkinson's Disease Dataset")

code("""parkinsons = pd.read_csv("../data/parkinsons_clean.csv")
parkinsons.head()
""")

code("""parkinsons.drop(columns=["name"]).describe()
""")

code("""fig, ax = plt.subplots()
parkinsons["status"].value_counts().plot(kind="bar", color=["#16A34A", "#DC2626"], ax=ax)
ax.set_xticklabels(["Healthy", "Parkinson's"], rotation=0)
ax.set_title("Class Distribution — Parkinson's")
plt.show()
""")

code("""plt.figure(figsize=(14, 11))
sns.heatmap(parkinsons.drop(columns=["name"]).corr(), cmap="RdBu_r", center=0)
plt.title("Correlation Heatmap — Parkinson's")
plt.show()
""")

md("""---
## 4. Model Building — Shared Pipeline

For every disease, we follow the same pipeline:

1. Split data 80/20 (stratified).
2. Standardize features with `StandardScaler`.
3. Train & 5-fold cross-validate 5 candidate algorithms.
4. Select the best model by mean CV accuracy.
5. Evaluate the chosen model on the held-out test set.

The helper function below is reused for all three diseases.
""")

code("""def evaluate_disease(df, feature_cols, target_col, title):
    X = df[feature_cols]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
        "SVM (RBF)": SVC(probability=True, random_state=RANDOM_STATE),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE),
    }

    results = {}
    for name, model in models.items():
        cv = cross_val_score(model, X_train_s, y_train, cv=5, scoring="accuracy")
        model.fit(X_train_s, y_train)
        preds = model.predict(X_test_s)
        acc = accuracy_score(y_test, preds)
        results[name] = {"cv_acc": cv.mean(), "test_acc": acc, "model": model}
        print(f"{name:<22} CV acc: {cv.mean():.3f}  Test acc: {acc:.3f}")

    best_name = max(results, key=lambda k: results[k]["cv_acc"])
    best_model = results[best_name]["model"]
    print(f"\\nBest model for {title}: {best_name}")

    preds = best_model.predict(X_test_s)
    print("\\n", classification_report(y_test, preds))

    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(4, 3.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix — {title} ({best_name})")
    plt.xlabel("Predicted"); plt.ylabel("Actual")
    plt.show()

    if hasattr(best_model, "predict_proba"):
        proba = best_model.predict_proba(X_test_s)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, proba)
        roc_auc = auc(fpr, tpr)
        plt.figure(figsize=(5, 4))
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
        plt.plot([0, 1], [0, 1], "--", color="gray")
        plt.xlabel("False Positive Rate"); plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve — {title}")
        plt.legend()
        plt.show()

    return results, best_name
""")

code("""diabetes_features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                      "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
diabetes_results, diabetes_best = evaluate_disease(diabetes, diabetes_features, "Outcome", "Diabetes")
""")

code("""heart_features = [c for c in heart.columns if c != "target"]
heart_results, heart_best = evaluate_disease(heart, heart_features, "target", "Heart Disease")
""")

code("""parkinsons_features = [c for c in parkinsons.columns if c not in ("name", "status")]
parkinsons_results, parkinsons_best = evaluate_disease(parkinsons, parkinsons_features, "status", "Parkinson's")
""")

md("""---
## 5. Conclusion

| Disease | Best Model |
|---|---|
| Diabetes | *(see output above)* |
| Heart Disease | *(see output above)* |
| Parkinson's | *(see output above)* |

These models are saved by `train_models.py` into `models/*.pkl` and are loaded
directly by the Streamlit app (`app.py`) for real-time prediction.

### Next steps for your report
- Discuss **why** certain features correlate strongly with each disease
  (tie back to the correlation heatmaps above).
- Discuss **model selection trade-offs** (e.g., Random Forest vs. Logistic
  Regression — interpretability vs. accuracy).
- Add **limitations**: small dataset sizes (especially Parkinson's, n=195),
  potential class imbalance, and the need for external clinical validation
  before any real-world deployment.
""")

nb["cells"] = cells
with open("notebooks/EDA_and_Model_Building.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook written to notebooks/EDA_and_Model_Building.ipynb")
