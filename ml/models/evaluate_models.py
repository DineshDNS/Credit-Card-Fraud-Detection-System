import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from sklearn.model_selection import train_test_split

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

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
# Train/Test Split
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ----------------------------------
# Load Preprocessor
# ----------------------------------

preprocessor = joblib.load(
    "artifacts/preprocessor.pkl"
)

X_test_processed = preprocessor.transform(
    X_test
)

# ----------------------------------
# Models
# ----------------------------------

models = {
    "Logistic Regression":
        "artifacts/logistic_regression.pkl",

    "Random Forest":
        "artifacts/random_forest.pkl",

    "XGBoost":
        "artifacts/xgboost.pkl"
}

# ----------------------------------
# Evaluate
# ----------------------------------

for name, path in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model = joblib.load(path)

    y_pred = model.predict(
        X_test_processed
    )

    y_prob = model.predict_proba(
        X_test_processed
    )[:, 1]

    print(
        "\nClassification Report"
    )

    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print(
        "\nConfusion Matrix"
    )

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print(
        "\nROC AUC Score"
    )

    print(
        roc_auc_score(
            y_test,
            y_prob
        )
    )