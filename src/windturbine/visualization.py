#!/usr/bin/env python3
"""
visualization.py

Generates scientific plots for the wind turbine blade dataset and model.
All plots are saved under: reports/figures/

Run:
    python -m src.windturbine.visualization
"""

from __future__ import annotations
import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = Path("data/wind_turbine_blade_data.csv")
MODEL_PATH = Path("models/rf_blade_model.pkl")


def savefig(name: str):
    """Utility wrapper to save high-quality figures."""
    plt.tight_layout()
    out = FIG_DIR / name
    plt.savefig(out, dpi=300)
    print(f"[saved] {out}")
    plt.close()


def plot_distributions(df: pd.DataFrame):
    """Plot distributions of key input variables."""
    numeric_cols = [
        "youngs_modulus", "density", "poissons_ratio",
        "thickness", "length", "pressure", "frequency"
    ]

    df[numeric_cols].hist(figsize=(14, 10), bins=20)
    savefig("input_distributions.png")


def plot_scatter_relations(df: pd.DataFrame):
    """Plot scatter relationships for a few important pairs."""
    pairs = [
        ("pressure", "frequency"),
        ("thickness", "length"),
        ("youngs_modulus", "deformation"),
        ("stress", "strain"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for ax, (x, y) in zip(axes.flat, pairs):
        ax.scatter(df[x], df[y], alpha=0.5)
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    savefig("scatter_relations.png")


def plot_corr_heatmap(df: pd.DataFrame):
    """Correlation heatmap of all variables."""
    plt.figure(figsize=(14, 12))
    sns.heatmap(df.corr(), annot=False, cmap="coolwarm")
    savefig("correlation_heatmap.png")


def plot_feature_importance(model, feature_names):
    """Plot RandomForest feature importances."""
    importances = model.feature_importances_

    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances, y=feature_names)
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("RandomForest Feature Importance")

    savefig("feature_importance.png")


def plot_actual_vs_pred(df: pd.DataFrame, model):
    """Plot actual vs predicted for each of the 6 outputs."""
    target_cols = [
        "deformation", "stress", "strain",
        "factor_of_safety", "fatigue_life", "damage"
    ]

    X = df[
        ["youngs_modulus", "density", "poissons_ratio",
         "thickness", "length", "pressure", "frequency"]
    ]
    y = df[target_cols]

    pred = model.predict(X)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for ax, idx in zip(axes.flat, range(len(target_cols))):
        ax.scatter(y.iloc[:, idx], pred[:, idx], alpha=0.5)
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title(target_cols[idx])

    savefig("actual_vs_predicted.png")


def plot_residuals(df: pd.DataFrame, model):
    """Residual error histograms."""
    target_cols = [
        "deformation", "stress", "strain",
        "factor_of_safety", "fatigue_life", "damage"
    ]

    X = df[
        ["youngs_modulus", "density", "poissons_ratio",
         "thickness", "length", "pressure", "frequency"]
    ]
    y = df[target_cols]

    pred = model.predict(X)
    residuals = y.values - pred

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for ax, idx in zip(axes.flat, range(residuals.shape[1])):
        ax.hist(residuals[:, idx], bins=20, alpha=0.7)
        ax.set_title(f"Residuals - {target_cols[idx]}")

    savefig("residual_histograms.png")


def plot_engineering_curves(df: pd.DataFrame):
    """Engineering-style visualizations."""
    plt.figure(figsize=(10, 6))
    plt.plot(df["length"], df["deformation"], "o", alpha=0.6)
    plt.xlabel("Blade Length (m)")
    plt.ylabel("Deformation (m)")
    plt.title("Deformation vs Blade Length")
    savefig("deformation_vs_length.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df["pressure"], df["stress"], "o", alpha=0.6)
    plt.xlabel("Pressure (Pa)")
    plt.ylabel("Stress (MPa)")
    plt.title("Stress vs Pressure")
    savefig("stress_vs_pressure.png")

    plt.figure(figsize=(10, 6))
    plt.plot(df["stress"], df["fatigue_life"], "o", alpha=0.6)
    plt.xlabel("Stress (MPa)")
    plt.ylabel("Fatigue Life (cycles)")
    plt.title("Fatigue Life vs Stress")
    savefig("fatigue_vs_stress.png")


def main():
    print("[loading data]")
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print("[loading model]")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    print("[generate plots]")

    plot_distributions(df)
    plot_scatter_relations(df)
    plot_corr_heatmap(df)
    plot_feature_importance(
        model, feature_names=[
            "youngs_modulus", "density", "poissons_ratio",
            "thickness", "length", "pressure", "frequency"
        ]
    )
    plot_actual_vs_pred(df, model)
    plot_residuals(df, model)
    plot_engineering_curves(df)

    print("\nAll plots saved under reports/figures/")


if __name__ == "__main__":
    main()
