import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from imblearn.over_sampling import SMOTE

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

print("=" * 50)
print("MODEL TRAINING STARTED")
print("=" * 50)

# ----------------------------------
# Target
# ----------------------------------

y = df["Class"]

# ----------------------------------
# Drop Columns
# ----------------------------------

drop_columns = [
    "Class",
    "TransactionID",
    "UserID",
    "CustomerName",
    "CustomerEmail",
    "CustomerPhone",
    "HomeLocation",
    "TransactionTimestamp"
]

X = df.drop(columns=drop_columns)

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
    for col in X.columns
    if col not in categorical_features
]

# ----------------------------------
# Train Test Split
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("\nTrain Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

# ----------------------------------
# Preprocessing
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

# ----------------------------------
# Fit Preprocessor
# ----------------------------------

X_train_processed = preprocessor.fit_transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)

print(
    "\nProcessed Train Shape:",
    X_train_processed.shape
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

print(
    "\nBalanced Train Shape:",
    X_train_balanced.shape
)

print(
    "\nFraud Count After SMOTE:"
)

print(
    pd.Series(y_train_balanced)
      .value_counts()
)

# ----------------------------------
# Models
# ----------------------------------

models = {

    "logistic_regression":
        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

    "random_forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        ),

    "xgboost":
        XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric="logloss"
        )
}

# ----------------------------------
# Create Artifacts Folder
# ----------------------------------

os.makedirs(
    "artifacts",
    exist_ok=True
)

# ----------------------------------
# Save Preprocessor
# ----------------------------------

joblib.dump(
    preprocessor,
    "artifacts/preprocessor.pkl"
)

# ----------------------------------
# Train Models
# ----------------------------------

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(
        X_train_balanced,
        y_train_balanced
    )

    model_path = (
        f"artifacts/{name}.pkl"
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        f"Saved: {model_path}"
    )

print("\nMODEL TRAINING COMPLETED")