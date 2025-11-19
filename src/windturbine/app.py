#!/usr/bin/env python3
from __future__ import annotations
"""
Flask app for Wind Turbine Blade Predictor.

This app locates templates either inside the package (src/windturbine/templates)
or at the repo root (templates/). It loads a joblib model (path configurable via
MODEL_PATH env var) and exposes:
  - GET  /        -> input form
  - POST /predict -> render prediction result page
  - GET  /health  -> JSON health info

Run locally:
  MODEL_PATH=models/rf_blade_model.pkl python -m src.windturbine.app
"""
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, render_template, request, jsonify

import joblib
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("windturbine.app")

# Determine sensible template folder location:
# prefer package-local templates (src/windturbine/templates),
# fall back to repo-root templates/ for compatibility with earlier layout.
PACKAGE_TEMPLATES = Path(__file__).resolve().parent / "templates"
# repo root is three parents up: src/windturbine -> src -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
REPO_TEMPLATES = REPO_ROOT / "templates"

if PACKAGE_TEMPLATES.exists():
    TEMPLATE_FOLDER = PACKAGE_TEMPLATES
    logger.info("Using package templates: %s", PACKAGE_TEMPLATES)
elif REPO_TEMPLATES.exists():
    TEMPLATE_FOLDER = REPO_TEMPLATES
    logger.info("Using repo-root templates: %s", REPO_TEMPLATES)
else:
    # default to package templates path (will raise TemplateNotFound later if missing)
    TEMPLATE_FOLDER = PACKAGE_TEMPLATES
    logger.warning("No templates directory found in package or repo root; expected at one of: %s or %s", PACKAGE_TEMPLATES, REPO_TEMPLATES)

app = Flask(__name__, template_folder=str(TEMPLATE_FOLDER))

# Feature order used by model.predict
FEATURE_ORDER = [
    "youngs_modulus",
    "density",
    "poissons_ratio",
    "thickness",
    "length",
    "pressure",
    "frequency",
]

# Default model path (can be overridden via env var)
DEFAULT_MODEL_PATH = os.environ.get("MODEL_PATH", "models/rf_blade_model.pkl")


def load_model(path: Optional[str] = None):
    """
    Load the model from disk. Returns the loaded model or raises FileNotFoundError.
    This function caches the loaded model on the module to avoid repeated loads.
    """
    if path is None:
        path = DEFAULT_MODEL_PATH

    # simple module-level cache
    if hasattr(load_model, "_cache") and load_model._cache is not None:
        return load_model._cache

    p = Path(path)
    if not p.exists():
        logger.warning("Model file not found at %s", p)
        raise FileNotFoundError(f"Model not found at {p}")

    try:
        logger.info("Loading model from %s", p)
        mdl = joblib.load(p)
        load_model._cache = mdl  # type: ignore[attr-defined]
        logger.info("Model loaded successfully.")
        return mdl
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Failed to load model: %s", exc)
        raise


def safe_predict(model, values: Dict[str, Any]) -> Dict[str, float]:
    """
    Given a fitted model and dictionary of feature values, return predictions mapped to names.
    Raises ValueError if inputs are invalid or model returns unexpected shape.
    """
    # Ensure feature order & types are floats
    try:
        row = [float(values[k]) for k in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e}") from e
    except Exception as e:
        raise ValueError(f"Invalid feature value: {e}") from e

    df = pd.DataFrame([row], columns=FEATURE_ORDER)
    preds = model.predict(df)

    # preds could be array-like with shape (1, n_targets) or (n_targets,)
    if hasattr(preds, "__len__") and getattr(preds, "ndim", 1) == 2:
        out = preds[0]
    else:
        out = preds

    if len(out) < 6:
        raise ValueError("Model returned unexpected number of outputs (expected >=6).")

    return {
        "deformation": float(out[0]),
        "stress": float(out[1]),
        "strain": float(out[2]),
        "factor_of_safety": float(out[3]),
        "fatigue_life": float(out[4]),
        "damage": float(out[5]),
    }


@app.route("/", methods=["GET"])
def index():
    """
    Render input form. If templates are missing this will raise TemplateNotFound
    and Flask will show a helpful traceback in debug mode.
    """
    return render_template("index.html")


def _parse_form(req) -> Dict[str, float]:
    """Parse required features from Flask request.form and return floats."""
    parsed: Dict[str, float] = {}
    for key in FEATURE_ORDER:
        v = req.form.get(key)
        if v is None or v.strip() == "":
            raise ValueError(f"Missing form value: {key}")
        try:
            parsed[key] = float(v)
        except ValueError as e:
            raise ValueError(f"Invalid numeric value for {key}: {v}") from e
    return parsed


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle predict form submission. Attempts to load the model (if not already loaded).
    Returns result.html with named predictions or error.html on failures.
    """
    try:
        model = None
        try:
            model = load_model()  # may raise FileNotFoundError
        except FileNotFoundError:
            logger.error("Model not loaded - cannot perform prediction.")
            return render_template("error.html", message="Model not loaded on server. Train the model or set MODEL_PATH."), 500

        data = _parse_form(request)
        preds = safe_predict(model, data)
        return render_template("result.html", **preds)
    except Exception as exc:
        logger.exception("Error during prediction: %s", exc)
        # Render a friendly error page with the exception message
        return render_template("error.html", message=str(exc)), 400


@app.route("/health", methods=["GET"])
def health():
    """
    Simple health endpoint: returns whether model file is available and whether model loads successfully.
    """
    model_present = Path(DEFAULT_MODEL_PATH).exists()
    model_loaded = False
    try:
        if model_present:
            # try loading without overwriting cached model if already loaded
            try:
                _ = load_model()
                model_loaded = True
            except Exception:
                model_loaded = False
    except Exception:
        model_loaded = False

    return jsonify({"status": "ok", "model_present": model_present, "model_loaded": model_loaded})


if __name__ == "__main__":
    # When running directly, use the default model path (can override via env var).
    port = int(os.environ.get("PORT", "5002"))
    # Enable flask debug only if FLASK_ENV=development is set by the user
    debug = os.environ.get("FLASK_ENV", "").lower() == "development"
    logger.info("Starting app on port %s (debug=%s). MODEL_PATH=%s", port, debug, os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH))
    app.run(host="0.0.0.0", port=port, debug=debug)
