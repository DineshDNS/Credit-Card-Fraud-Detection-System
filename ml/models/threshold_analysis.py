import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
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
# Load Artifacts
# ----------------------------------

preprocessor = joblib.load(
    "artifacts/preprocessor.pkl"
)

model = joblib.load(
    "artifacts/random_forest.pkl"
)

X_test_processed = preprocessor.transform(
    X_test
)

# ----------------------------------
# Probability Scores
# ----------------------------------

y_prob = model.predict_proba(
    X_test_processed
)[:, 1]

# ----------------------------------
# Threshold Testing
# ----------------------------------

thresholds = [
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

print("=" * 80)
print("THRESHOLD ANALYSIS")
print("=" * 80)

for threshold in thresholds:

    y_pred = (
        y_prob >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred
    )

    f1 = f1_score(
        y_test,
        y_pred
    )

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        y_pred
    ).ravel()

    print("\n" + "-" * 50)
    print(f"Threshold: {threshold}")

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall: {recall:.4f}"
    )

    print(
        f"F1 Score: {f1:.4f}"
    )

    print(
        f"False Positives: {fp}"
    )

    print(
        f"False Negatives: {fn}"
    )

    print(
        f"True Positives: {tp}"
    )