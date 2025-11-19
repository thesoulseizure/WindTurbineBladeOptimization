#!/usr/bin/env python3
from __future__ import annotations
"""
model.py

Model loading and prediction utilities.
"""

from pathlib import Path
import os
from typing import Dict, Any, List

import joblib
import pandas as pd


DEFAULT_MODEL_PATH = os.environ.get("MODEL_PATH", "models/rf_blade_model.pkl")
FEATURE_ORDER = ["youngs_modulus", "density", "poissons_ratio", "thickness", "length", "pressure", "frequency"]


def load_model(path: str = DEFAULT_MODEL_PATH):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model not found at {p}")
    return joblib.load(p)


def predict_from_dict(model, data: Dict[str, Any]) -> Dict[str, float]:
    """Given a loaded model and a dict of features, return named predictions."""
    # Ensure feature order and types
    xs = [float(data[k]) for k in FEATURE_ORDER]
    df = pd.DataFrame([xs], columns=FEATURE_ORDER)
    preds = model.predict(df)
    if preds.ndim == 2:
        row = preds[0]
    else:
        row = preds
    return {
        "deformation": float(row[0]),
        "stress": float(row[1]),
        "strain": float(row[2]),
        "factor_of_safety": float(row[3]),
        "fatigue_life": float(row[4]),
        "damage": float(row[5]),
    }
