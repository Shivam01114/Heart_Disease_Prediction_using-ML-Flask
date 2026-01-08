import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load dataset
heart_data = pd.read_csv("heart.csv")

X = heart_data.drop(columns='target', axis=1)
Y = heart_data['target']

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=2
)

# Train model
model = LogisticRegression(solver='liblinear')
model.fit(X_train, Y_train)

# Save model
with open("heart_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model trained & saved as heart_model.pkl")
