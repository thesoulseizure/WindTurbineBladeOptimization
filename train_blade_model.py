import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the synthetic dataset
df = pd.read_csv('wind_turbine_blade_data.csv')

# Features and targets
X = df[['youngs_modulus', 'density', 'poissons_ratio', 'thickness', 'length', 'pressure', 'frequency']]
y = df[['deformation', 'stress', 'strain', 'factor_of_safety', 'fatigue_life', 'damage']]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
train_score = rf_model.score(X_train, y_train)
test_score = rf_model.score(X_test, y_test)
print(f"Training R² Score: {train_score:.4f}")
print(f"Testing R² Score: {test_score:.4f}")

# Save the model
joblib.dump(rf_model, 'rf_blade_model.pkl')
print("Model saved as 'rf_blade_model.pkl'")