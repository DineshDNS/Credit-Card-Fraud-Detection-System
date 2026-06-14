import pandas as pd
import random
import numpy as np
from faker import Faker

random.seed(42)
np.random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("data/raw/creditcard.csv")

# -----------------------------
# Master Locations
# -----------------------------

locations = [
    "Chennai",
    "Mumbai",
    "Madurai",
    "Trichy",
    "Mayiladuthurai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Kolkata",
    "Ahmedabad"
]

# -----------------------------
# Create User Master
# -----------------------------

NUM_USERS = 5000

users = []

for i in range(1, NUM_USERS + 1):
    users.append({
        "UserID": f"U{i:05}",
        "CustomerName": fake.name(),
        "CustomerEmail": fake.email(),
        "CustomerPhone": fake.msisdn()[:10],
        "HomeLocation": random.choice(locations)
    })

users_df = pd.DataFrame(users)

# -----------------------------
# Assign Users To Transactions
# -----------------------------

assigned_users = users_df.sample(
    n=len(df),
    replace=True,
    random_state=42
).reset_index(drop=True)

# -----------------------------
# Transaction ID
# -----------------------------

df["TransactionID"] = [
    f"TXN{i:07}"
    for i in range(1, len(df) + 1)
]

# -----------------------------
# User Details
# -----------------------------

df["UserID"] = assigned_users["UserID"]
df["CustomerName"] = assigned_users["CustomerName"]
df["CustomerEmail"] = assigned_users["CustomerEmail"]
df["CustomerPhone"] = assigned_users["CustomerPhone"]
df["HomeLocation"] = assigned_users["HomeLocation"]

# -----------------------------
# Merchants
# -----------------------------

merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Reliance",
    "Myntra",
    "BigBasket",
    "Croma",
    "Ajio",
    "Meesho"
]

df["Merchant"] = [
    random.choice(merchants)
    for _ in range(len(df))
]

# -----------------------------
# Transaction Location
# 90% Home Location
# 10% Other Location
# -----------------------------

transaction_locations = []

for home_location in df["HomeLocation"]:

    if random.random() < 0.90:

        transaction_locations.append(
            home_location
        )

    else:

        other_locations = [
            loc
            for loc in locations
            if loc != home_location
        ]

        transaction_locations.append(
            random.choice(other_locations)
        )

df["Location"] = transaction_locations

# -----------------------------
# Transaction Type
# -----------------------------

df["TransactionType"] = random.choices(
    ["Online", "Offline"],
    weights=[70, 30],
    k=len(df)
)

# -----------------------------
# Transaction Timestamp
# -----------------------------

base_time = pd.Timestamp(
    "2025-01-01 00:00:00"
)

df["TransactionTimestamp"] = (
    base_time +
    pd.to_timedelta(df["Time"], unit="s")
)

# -----------------------------
# Inject High Value Transactions
# -----------------------------

high_value_count = int(
    len(df) * 0.01
)

high_value_indices = np.random.choice(
    df.index,
    high_value_count,
    replace=False
)

df.loc[
    high_value_indices,
    "Amount"
] = np.random.randint(
    50000,
    200001,
    high_value_count
)

print(
    f"Injected {high_value_count} high-value transactions"
)

# -----------------------------
# Save Dataset
# -----------------------------

output_path = (
    "data/processed/enhanced_creditcard.csv"
)

df.to_csv(
    output_path,
    index=False
)

# -----------------------------
# Validation Summary
# -----------------------------

home_match_percentage = (
    (df["Location"] == df["HomeLocation"])
    .mean()
    * 100
)

print("\nEnhanced dataset created successfully")
print("Shape:", df.shape)

print(
    "\nTransactions > 50000:",
    (df["Amount"] > 50000).sum()
)

print(
    "Maximum Amount:",
    df["Amount"].max()
)

print(
    f"Home Location Match: {home_match_percentage:.2f}%"
)

print("\nSample Data:")

print(
    df[
        [
            "TransactionID",
            "UserID",
            "HomeLocation",
            "Location",
            "Amount"
        ]
    ].head()
)