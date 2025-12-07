import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib


df = pd.read_csv("cyber_dataset.csv")
df = df.drop(columns=["session_id"])


label_encoders = {}
for col in ["protocol_type", "encryption_used", "browser_type"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le


X = df.drop(columns=["attack_detected"])
y = df["attack_detected"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(f"Model trained successfully with accuracy: {acc:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))


metrics = {
    "accuracy": acc,
    "confusion_matrix": cm.tolist(),
    "feature_importances": list(model.feature_importances_),
    "features": list(X.columns)
}

joblib.dump(model, "cyber_ai_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(metrics, "metrics.pkl")

print("Model, encoders, and metrics saved successfully!")
