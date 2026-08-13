"""
Prepares raw datasets by adding proper column headers and saving clean CSVs.
Run this once before train_models.py.
"""
import pandas as pd

# ---------- Diabetes ----------
diabetes_cols = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]
diabetes = pd.read_csv("data/diabetes.csv", names=diabetes_cols)
diabetes.to_csv("data/diabetes_clean.csv", index=False)
print(f"Diabetes dataset: {diabetes.shape[0]} rows, {diabetes.shape[1]} columns")

# ---------- Heart Disease ----------
heart = pd.read_csv("data/heart.csv", encoding="utf-8-sig")
heart.columns = heart.columns.str.strip()
heart.to_csv("data/heart_clean.csv", index=False)
print(f"Heart disease dataset: {heart.shape[0]} rows, {heart.shape[1]} columns")

# ---------- Parkinson's ----------
parkinsons = pd.read_csv("data/parkinsons.csv")
parkinsons.to_csv("data/parkinsons_clean.csv", index=False)
print(f"Parkinson's dataset: {parkinsons.shape[0]} rows, {parkinsons.shape[1]} columns")

print("\nAll datasets cleaned and saved.")
