#!/usr/bin/env python3
"""
train_blade_model.py

Train a RandomForest multi-output regressor and save to models/.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import json

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def train(X, y, n_estimators=100, random_state=42):
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X, y)
    return model

def main():
    parser = argparse.ArgumentParser(description="Train blade model and save artifact.")
    parser.add_argument("--data", type=str, default="data/wind_turbine_blade_data.csv", help="Path to CSV dataset.")
    parser.add_argument("--out", type=str, default="models/rf_blade_model.pkl", help="Output model path.")
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    df = load_data(args.data)
    features = ['youngs_modulus', 'density', 'poissons_ratio', 'thickness', 'length', 'pressure', 'frequency']
    targets = ['deformation', 'stress', 'strain', 'factor_of_safety', 'fatigue_life', 'damage']

    X = df[features]
    y = df[targets]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.random_state)

    model = train(X_train, y_train, n_estimators=args.n_estimators, random_state=args.random_state)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)

    # Write a simple JSON metrics file
    metrics = {"train_r2": float(train_score), "test_r2": float(test_score)}
    with open(out_path.with_suffix(".metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Model saved to {out_path}")
    print(f"Metrics: train_r2={train_score:.4f}, test_r2={test_score:.4f}")

if __name__ == "__main__":
    main()
