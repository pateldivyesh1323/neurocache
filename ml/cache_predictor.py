import pandas as pd
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "access_log.jsonl")
df = pd.read_json(data_path, lines=True)

df = df.sort_values(["session", "key", "timestamp"])
df["next_access_gap"] = df.groupby(["session", "key"])["timestamp"].shift(-1) - df["timestamp"]
df["was_reused"] = df["next_access_gap"].notna().astype(int)

dataset = df[[
    "time_since_last_access",
    "access_count",
    "was_reused"
]].copy()

dataset["time_since_last_access"] = dataset["time_since_last_access"].fillna(0)

output_path = os.path.join(script_dir, "../data/cache_training_data.csv")
dataset.to_csv(output_path, index=False)

print("Training Data:")
print(dataset)

X = dataset[["time_since_last_access", "access_count"]]
y = dataset["was_reused"]

if len(dataset) >= 4:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
else:
    X_train, X_test, y_train, y_test = X, X, y, y

model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"\nModel trained successfully!")
print(f"Training accuracy: {train_score:.2%}")
print(f"Testing accuracy: {test_score:.2%}")

model_path = os.path.join(script_dir, "../data/eviction_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"\nModel saved to: {model_path}")