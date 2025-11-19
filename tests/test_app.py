import joblib
import numpy as np
import pytest

FEATURE_ORDER = [
    "youngs_modulus",
    "density",
    "poissons_ratio",
    "thickness",
    "length",
    "pressure",
    "frequency",
]


class DummyModel:
    def predict(self, X):
        n = X.shape[0]
        out = np.zeros((n, 6))
        s = X.sum(axis=1).to_numpy()
        for i in range(6):
            out[:, i] = s * (i + 1) * 0.001 + (i + 1) * 0.1
        return out


@pytest.fixture
def client(tmp_path, monkeypatch):
    model_path = tmp_path / "models"
    model_path.mkdir()
    dummy = DummyModel()
    mfile = model_path / "rf_blade_model.pkl"
    joblib.dump(dummy, mfile)

    monkeypatch.setenv("MODEL_PATH", str(mfile))

    import importlib
    import src.windturbine.app as appmod

    importlib.reload(appmod)
    client_obj = appmod.app.test_client()
    return client_obj


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
