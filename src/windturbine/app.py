#!/usr/bin/env python3
from __future__ import annotations
"""
Flask app for Wind Turbine Blade Predictor.

Loads joblib model (MODEL_PATH env var or default: models/rf_blade_model.pkl)
and exposes:

GET  /        → Input form
POST /predict → Prediction results
GET  /health  → JSON server/model status
"""

import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

# ----------------------------------------------------------------------
# Logging setup
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("windturbine.app")

# ----------------------------------------------------------------------
# Template folder resolution
# ----------------------------------------------------------------------
PACKAGE_TEMPLATES = Path(__file__).resolve().parent / "templates"
REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_TEMPLATES = REPO_ROOT / "templates"

if PACKAGE_TEMPLATES.exists():
    TEMPLATE_FOLDER = PACKAGE_TEMPLATES
    logger.info("Using package templates: %s", PACKAGE_TEMPLATES)
elif REPO_TEMPLATES.exists():
    TEMPLATE_FOLDER = REPO_TEMPLATES
    logger.info("Using repo-root templates: %s", REPO_TEMPLATES)
else:
    TEMPLATE_FOLDER = PACKAGE_TEMPLATES
    logger.warning(
        "No templates found. Expected one of:\n  - %s\n  - %s",
        PACKAGE_TEMPLATES,
        REPO_TEMPLATES,
    )

app = Flask(__name__, template_folder=str(TEMPLATE_FOLDER))

# ----------------------------------------------------------------------
# Model + features
# ----------------------------------------------------------------------
FEATURE_ORDER = [
    "youngs_modulus",
    "density",
    "poissons_ratio",
    "thickness",
    "length",
    "pressure",
    "frequency",
]

DEFAULT_MODEL_PATH = os.environ.get(
    "MODEL_PATH", "models/rf_blade_model.pkl"
)


def load_model(path: Optional[str] = None):
    """Load joblib model with caching."""
    if path is None:
        path = DEFAULT_MODEL_PATH

    if hasattr(load_model, "_cache"):
        return load_model._cache

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model not found at: {p}")

    logger.info("Loading model from %s", p)
    model = joblib.load(p)
    load_model._cache = model
    return model


# ----------------------------------------------------------------------
# Prediction logic
# ----------------------------------------------------------------------
def safe_predict(model, values: Dict[str, Any]) -> Dict[str, float]:
    """Validate input, run prediction, return dict of results."""
    try:
        row = [float(values[k]) for k in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e}") from e
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}") from e

    df = pd.DataFrame([row], columns=FEATURE_ORDER)
    preds = model.predict(df)

    if getattr(preds, "ndim", 1) == 2:
        preds = preds[0]

    if len(preds) < 6:
        raise ValueError("Model output incomplete (expected ≥6 values).")

    return {
        "deformation": float(preds[0]),
        "stress": float(preds[1]),
        "strain": float(preds[2]),
        "factor_of_safety": float(preds[3]),
        "fatigue_life": float(preds[4]),
        "damage": float(preds[5]),
    }


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def _parse_form(req) -> Dict[str, float]:
    """Extract required form values and convert to floats."""
    result = {}
    for key in FEATURE_ORDER:
        val = req.form.get(key)
        if val is None or val.strip() == "":
            raise ValueError(f"Missing value: {key}")
        result[key] = float(val)
    return result


@app.route("/predict", methods=["POST"])
def predict():
    try:
        try:
            model = load_model()
        except FileNotFoundError:
            return (
                render_template(
                    "error.html",
                    message="Model not found on server. Please train it.",
                ),
                500,
            )

        data = _parse_form(request)
        preds = safe_predict(model, data)
        return render_template("result.html", **preds)

    except Exception as exc:
        logger.exception("Prediction error: %s", exc)
        return render_template("error.html", message=str(exc)), 400


@app.route("/health", methods=["GET"])
def health():
    model_file = Path(DEFAULT_MODEL_PATH)
    present = model_file.exists()

    loaded = False
    if present:
        try:
            _ = load_model()
            loaded = True
        except Exception:
            loaded = False

    return jsonify({
        "status": "ok",
        "model_present": present,
        "model_loaded": loaded,
    })


# ----------------------------------------------------------------------
# Startup
# ----------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5002"))
    debug = os.environ.get("FLASK_ENV", "").lower() == "development"

    logger.info(
        "Starting app on port %s (debug=%s). MODEL_PATH=%s",
        port,
        debug,
        DEFAULT_MODEL_PATH,
    )

    app.run(host="0.0.0.0", port=port, debug=debug)
