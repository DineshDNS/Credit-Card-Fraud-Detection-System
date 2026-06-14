import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report
)

from imblearn.over_sampling import SMOTE

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

print("=" * 50)
print("PRODUCTION MODEL TRAINING")
print("=" * 50)

# ----------------------------------
# Target
# ----------------------------------

y = df["Class"]

# ----------------------------------
# Production Features Only
# ----------------------------------

feature_columns = [

    "Amount",

    "Merchant",
    "Location",
    "TransactionType",

    "TransactionFrequency",
    "UserAvgAmount",
    "TimeGap",
    "LocationDeviation",
    "UnusualSpending",
    "Hour",
    "NightTransaction",
    "HighAmountFlag",
    "RapidTransaction"
]

X = df[feature_columns]

# ----------------------------------
# Feature Types
# ----------------------------------

categorical_features = [
    "Merchant",
    "Location",
    "TransactionType"
]

numerical_features = [
    col
    for col in feature_columns
    if col not in categorical_features
]

# ----------------------------------
# Split
# ----------------------------------

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
)

# ----------------------------------
# Preprocessor
# ----------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)

X_train_processed = (
    preprocessor.fit_transform(
        X_train
    )
)

X_test_processed = (
    preprocessor.transform(
        X_test
    )
)

# ----------------------------------
# SMOTE
# ----------------------------------

smote = SMOTE(
    random_state=42
)

X_train_balanced, y_train_balanced = (
    smote.fit_resample(
        X_train_processed,
        y_train
    )
)

# ----------------------------------
# Model
# ----------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train_balanced,
    y_train_balanced
)

# ----------------------------------
# Evaluation
# ----------------------------------

y_pred = model.predict(
    X_test_processed
)

print(
    classification_report(
        y_test,
        y_pred
    )
)

# ----------------------------------
# Save
# ----------------------------------

os.makedirs(
    "artifacts",
    exist_ok=True
)

joblib.dump(
    model,
    "artifacts/production_random_forest.pkl"
)

joblib.dump(
    preprocessor,
    "artifacts/production_preprocessor.pkl"
)

print(
    "\nProduction Model Saved"
)