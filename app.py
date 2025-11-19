#!/usr/bin/env python3
"""
app.py - Flask app for Wind Turbine Blade Predictor.

Improvements:
- MODEL_PATH can be configured via MODEL_PATH env var
- Accepts form POST and JSON POST
- Input validation and ranges
- Clear logging and structured error responses (JSON for API)
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Dict, Any

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd


# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("windblade")


# App
app = Flask(__name__, template_folder="templates")


# Config: MODEL_PATH env var or default
BASE_DIR = Path(__file__).parent.resolve()
MODEL_PATH = Path(os.environ.get("MODEL_PATH", BASE_DIR / "models" / "rf_blade_model.pkl"))


def load_model(path: Path):
    if not path.exists():
        logger.warning("Model not found at %s", path)
        return None
    try:
        model = joblib.load(path)
        logger.info("Loaded model from %s", path)
        return model
    except Exception as exc:
        logger.exception("Failed to load model: %s", exc)
        return None


rf_model = load_model(MODEL_PATH)


# Input validation ranges (example)
RANGES = {
    "youngs_modulus": (1, 1e4),
    "density": (1, 1e5),
    "poissons_ratio": (0.0, 1.0),
    "thickness": (0.001, 1e3),
    "length": (0.001, 1e4),
    "pressure": (0, 1e7),
    "frequency": (0, 1e6),
}

FEATURE_ORDER = [
    "youngs_modulus",
    "density",
    "poissons_ratio",
    "thickness",
    "length",
    "pressure",
    "frequency",
]


def parse_and_validate(data: Dict[str, Any]) -> pd.DataFrame:
    vals = {}
    for f in FEATURE_ORDER:
        if f not in data:
            raise ValueError(f"Missing input: {f}")
        try:
            v = float(data[f])
        except Exception:
            raise ValueError(f"Invalid numeric value for {f}: {data[f]}")
        low, high = RANGES[f]
        if not (low <= v <= high):
            raise ValueError(f"Value for {f} out of range [{low}, {high}]: {v}")
        vals[f] = v
    return pd.DataFrame([vals])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Support form submission or JSON
    if rf_model is None:
        return (
            render_template("error.html", message="Model is not available on server. Contact admin."),
            503,
        )

    try:
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.form.to_dict()

        input_df = parse_and_validate(payload)

        preds = rf_model.predict(input_df)
        row = preds[0] if hasattr(preds, "__len__") else preds

        if len(row) < 6:
            raise RuntimeError("Model returned unexpected output shape")

        results = {
            "deformation": float(row[0]),
            "stress": float(row[1]),
            "strain": float(row[2]),
            "factor_of_safety": float(row[3]),
            "fatigue_life": float(row[4]),
            "damage": float(row[5]),
        }

        # If request wants JSON, return it; otherwise render template
        if request.is_json:
            return jsonify({"success": True, "predictions": results})
        return render_template("result.html", **results)
    except Exception as exc:
        logger.exception("Prediction error: %s", exc)
        # For form requests show template; for API requests return JSON error
        if request.is_json:
            return jsonify({"success": False, "error": str(exc)}), 400
        return render_template("error.html", message=str(exc)), 400


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": rf_model is not None})


if __name__ == "__main__":
    # Run only for local development. Production use gunicorn and set MODEL_PATH env var.
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5002)),
        debug=bool(os.environ.get("FLASK_DEBUG", "false").lower() in ["1", "true"]),
    )
