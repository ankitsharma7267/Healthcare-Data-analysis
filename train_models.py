"""
Trains classification models for Diabetes, Heart Disease, and Parkinson's
prediction. For each disease, several algorithms are compared and the
best-performing one (by cross-validated accuracy) is saved to disk along
with its scaler, for use by the Streamlit app.

Run:
    python train_models.py
"""
import json
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
) 
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

RANDOM_STATE = 42

CANDIDATE_MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
    "SVM (RBF)": SVC(probability=True, random_state=RANDOM_STATE),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE),
}


def train_disease_model(name, csv_path, feature_cols, target_col, drop_cols=None):
    print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
    df = pd.read_csv(csv_path)
    if drop_cols:
        df = df.drop(columns=drop_cols, errors="ignore")

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = {}
    fitted_models = {}

    for model_name, model in CANDIDATE_MODELS.items():
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="accuracy")
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        probs = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None

        metrics = {
            "cv_accuracy_mean": round(float(cv_scores.mean()), 4),
            "cv_accuracy_std": round(float(cv_scores.std()), 4),
            "test_accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "precision": round(float(precision_score(y_test, preds)), 4),
            "recall": round(float(recall_score(y_test, preds)), 4),
            "f1_score": round(float(f1_score(y_test, preds)), 4),
        }
        if probs is not None:
            metrics["roc_auc"] = round(float(roc_auc_score(y_test, probs)), 4)

        results[model_name] = metrics
        fitted_models[model_name] = model
        print(f"  {model_name:<22} CV acc: {metrics['cv_accuracy_mean']:.3f} "
              f"| Test acc: {metrics['test_accuracy']:.3f} | F1: {metrics['f1_score']:.3f}")

    # Pick best model by cross-validated accuracy (more robust than single test split)
    best_model_name = max(results, key=lambda m: results[m]["cv_accuracy_mean"])
    best_model = fitted_models[best_model_name]
    print(f"\n  --> Best model: {best_model_name} "
          f"(CV acc: {results[best_model_name]['cv_accuracy_mean']:.3f})")

    return {
        "best_model_name": best_model_name,
        "model": best_model,
        "scaler": scaler,
        "feature_cols": feature_cols,
        "all_results": results,
    }


def main():
    all_metrics = {}

    # ---------------- Diabetes ----------------
    diabetes_features = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ]
    diabetes_result = train_disease_model(
        "DIABETES", "data/diabetes_clean.csv", diabetes_features, "Outcome"
    )
    with open("models/diabetes_model.pkl", "wb") as f:
        pickle.dump({
            "model": diabetes_result["model"],
            "scaler": diabetes_result["scaler"],
            "features": diabetes_result["feature_cols"],
            "model_name": diabetes_result["best_model_name"],
        }, f)
    all_metrics["diabetes"] = diabetes_result["all_results"]
    all_metrics["diabetes"]["best_model"] = diabetes_result["best_model_name"]

    # ---------------- Heart Disease ----------------
    heart_df = pd.read_csv("data/heart_clean.csv")
    heart_features = [c for c in heart_df.columns if c != "target"]
    heart_result = train_disease_model(
        "HEART DISEASE", "data/heart_clean.csv", heart_features, "target"
    )
    with open("models/heart_model.pkl", "wb") as f:
        pickle.dump({
            "model": heart_result["model"],
            "scaler": heart_result["scaler"],
            "features": heart_result["feature_cols"],
            "model_name": heart_result["best_model_name"],
        }, f)
    all_metrics["heart"] = heart_result["all_results"]
    all_metrics["heart"]["best_model"] = heart_result["best_model_name"]

    # ---------------- Parkinson's ----------------
    parkinsons_df = pd.read_csv("data/parkinsons_clean.csv")
    parkinsons_features = [c for c in parkinsons_df.columns if c not in ("name", "status")]
    parkinsons_result = train_disease_model(
        "PARKINSON'S DISEASE", "data/parkinsons_clean.csv",
        parkinsons_features, "status", drop_cols=["name"]
    )
    with open("models/parkinsons_model.pkl", "wb") as f:
        pickle.dump({
            "model": parkinsons_result["model"],
            "scaler": parkinsons_result["scaler"],
            "features": parkinsons_result["feature_cols"],
            "model_name": parkinsons_result["best_model_name"],
        }, f)
    all_metrics["parkinsons"] = parkinsons_result["all_results"]
    all_metrics["parkinsons"]["best_model"] = parkinsons_result["best_model_name"]

    # Save all metrics for the dashboard "Model Performance" page
    with open("models/model_metrics.json", "w") as f:
        json.dump(all_metrics, f, indent=2)

    print("\n" + "=" * 60)
    print("All models trained and saved to models/")
    print("=" * 60)


if __name__ == "__main__":
    main()
