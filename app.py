from flask import Flask, render_template, request, abort, jsonify
import joblib
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app. Templates must live in ./templates relative to this file.
app = Flask(__name__, template_folder='templates')

# Model path (relative to this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rf_blade_model.pkl")

# Try to load the model and log errors clearly
rf_model = None
try:
    logger.info("Loading model from %s", MODEL_PATH)
    rf_model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.exception("Failed to load model. Predictions will not work until the model is available: %s", e)
    rf_model = None

@app.route("/")
def index():
    # Render input form
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if rf_model is None:
        logger.error("Prediction requested but model is not loaded.")
        return render_template("error.html", message="Model not loaded on server. Check logs."), 500

    try:
        # Parse and validate incoming form values
        def get_float(key):
            v = request.form.get(key)
            if v is None or v == "":
                raise ValueError(f"Missing form value: {key}")
            return float(v)

        features = {
            "youngs_modulus": get_float("youngs_modulus"),
            "density": get_float("density"),
            "poissons_ratio": get_float("poissons_ratio"),
            "thickness": get_float("thickness"),
            "length": get_float("length"),
            "pressure": get_float("pressure"),
            "frequency": get_float("frequency"),
        }

        input_df = pd.DataFrame([features])

        # Predict
        preds = rf_model.predict(input_df)

        # If model returns shape (n_samples, n_targets) where n_targets=6
        if hasattr(preds, "__len__") and len(preds) > 0:
            row = preds[0]
        else:
            row = preds

        # Defensive: ensure we have at least 6 outputs
        if len(row) < 6:
            logger.error("Model returned unexpected output shape: %s", row)
            return render_template("error.html", message="Model returned unexpected output shape."), 500

        results = {
            "deformation": float(row[0]),
            "stress": float(row[1]),
            "strain": float(row[2]),
            "factor_of_safety": float(row[3]),
            "fatigue_life": float(row[4]),
            "damage": float(row[5]),
        }

        return render_template("result.html", **results)
    except Exception as e:
        logger.exception("Error during prediction: %s", e)
        return render_template("error.html", message=str(e)), 400

@app.route("/health")
def health():
    # Simple health endpoint to quickly check app status
    status = {"status": "ok", "model_loaded": rf_model is not None}
    return jsonify(status)

if __name__ == "__main__":
    # When run locally, debug True is okay for development; Render will use gunicorn.
    app.run(host="0.0.0.0", port=5002, debug=True)
