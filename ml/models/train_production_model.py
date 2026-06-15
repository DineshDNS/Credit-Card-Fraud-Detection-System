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
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)

from imblearn.over_sampling import SMOTE

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/business_fraud_dataset.csv"
)

print("=" * 50)
print("PRODUCTION MODEL TRAINING")
print("=" * 50)

# ----------------------------------
# Target
# ----------------------------------

y = df["BusinessClass"]

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

y_prob = model.predict_proba(
    X_test_processed
)[:, 1]

print("\n" + "=" * 50)
print("MODEL EVALUATION")
print("=" * 50)

print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\nPrecision")

print(
    precision_score(
        y_test,
        y_pred
    )
)

print("\nRecall")

print(
    recall_score(
        y_test,
        y_pred
    )
)

print("\nF1 Score")

print(
    f1_score(
        y_test,
        y_pred
    )
)

print("\nROC-AUC")

print(
    roc_auc_score(
        y_test,
        y_prob
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
    "artifacts/business_random_forest.pkl"
)

joblib.dump(
    preprocessor,
    "artifacts/business_preprocessor.pkl"
)

print(
    "\nProduction Model Saved"
)