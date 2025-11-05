import pandas as pd
import numpy as np
import pickle
import textwrap
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
LOGIC_DIR = BASE_DIR / "logic"
MODEL_DIR.mkdir(exist_ok=True)
LOGIC_DIR.mkdir(exist_ok=True)

DATA_PATH = BASE_DIR / "indian_liver_patient.csv"
df = pd.read_csv(DATA_PATH)
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Albumin_and_Globulin_Ratio'].fillna(df['Albumin_and_Globulin_Ratio'].mean(), inplace=True)
df['target'] = df['Dataset'].map({1: 1, 2: 0})
X = df.drop(columns=['Dataset', 'target'])
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
print(f" Model trained successfully with accuracy: {acc:.2f}")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, digits=3))
with open(MODEL_DIR / "liver_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open(MODEL_DIR / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print(f" Saved model and scaler inside '{MODEL_DIR}/'")
print("\n All setup completed successfully!")
