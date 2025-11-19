import pandas as pd
from src.windturbine.train import train
from sklearn.ensemble import RandomForestRegressor


def test_train_smoke():
    df = pd.DataFrame(
        {
            "youngs_modulus": [70, 75, 65, 80],
            "density": [2700, 2750, 2650, 2800],
            "poissons_ratio": [0.33, 0.34, 0.32, 0.33],
            "thickness": [5, 5.5, 4.5, 6],
            "length": [1, 1.1, 0.9, 1.05],
            "pressure": [101325, 100000, 110000, 105000],
            "frequency": [300, 310, 290, 305],
            "deformation": [0.04, 0.045, 0.05, 0.042],
            "stress": [1.3, 1.4, 1.2, 1.35],
            "strain": [7e-6, 8e-6, 7.5e-6, 7.8e-6],
            "factor_of_safety": [15, 14, 16, 15],
            "fatigue_life": [1e6, 9e5, 1.1e6, 1.05e6],
            "damage": [1000, 1050, 980, 1020],
        }
    )

    X = df[
        [
            "youngs_modulus",
            "density",
            "poissons_ratio",
            "thickness",
            "length",
            "pressure",
            "frequency",
        ]
    ]
    y = df[
        [
            "deformation",
            "stress",
            "strain",
            "factor_of_safety",
            "fatigue_life",
            "damage",
        ]
    ]

    model = train(X, y, n_estimators=10, random_state=0)
    assert isinstance(model, RandomForestRegressor)
