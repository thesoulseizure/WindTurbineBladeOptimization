import os
import joblib
import tempfile
from pathlib import Path
import numpy as np

import pytest

from app import app, FEATURE_ORDER

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create a trivial model that echoes input to 6 outputs for testing
    class DummyModel:
        def predict(self, X):
            n = X.shape[0]
            # Return deterministic 6-value outputs based on X sum
            out = np.zeros((n, 6))
            s = X.sum(axis=1).to_numpy()
            for i in range(6):
                out[:, i] = s * (i + 1) * 0.001 + (i + 1) * 0.1
            return out

    model_path = tmp_path / "models"
    model_path.mkdir()
    dummy = DummyModel()
    mfile = model_path / "rf_blade_model.pkl"
    joblib.dump(dummy, mfile)
    # monkeypatch MODEL_PATH in app module to point to this model
    monkeypatch.setenv("MODEL_PATH", str(mfile))
    # reload app module to load model (import side-effect)
    # Note: this test assumes app loads model at import; alternatively you can import reload
    from importlib import reload
    import app as appmod
    reload(appmod)
    client = appmod.app.test_client()
    yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    j = res.get_json()
    assert "model_loaded" in j

def test_predict_form(client):
    data = {k: 1.0 for k in FEATURE_ORDER}
    res = client.post("/predict", data=data)
    assert res.status_code == 200
    assert b"Prediction Results" in res.data or b"Deformation" in res.data
