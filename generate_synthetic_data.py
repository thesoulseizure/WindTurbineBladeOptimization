#!/usr/bin/env python3
"""
generate_synthetic_data.py

Generates a synthetic dataset for blade performance predictions.
Writes CSV into the `data/` directory by default.
"""

from __future__ import annotations

import argparse
import numpy as np
import pandas as pd
from pathlib import Path

BASELINE = {
    "youngs_modulus": 70,  # GPa
    "density": 2700,  # kg/m^3
    "poissons_ratio": 0.33,
    "thickness": 5,  # mm
    "length": 1,  # m
    "pressure": 101325,  # Pa
    "frequency": 300,  # Hz
    "deformation": 0.046712,  # mm
    "stress": 1.385,  # MPa
    "strain": 7.73732e-6,
    "factor_of_safety": 15,
    "fatigue_life": 1e6,  # cycles
    "damage": 1000,
}


def generate(n_samples: int = 150, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    data = {
        "youngs_modulus": np.random.uniform(50, 90, n_samples),
        "density": np.random.uniform(2500, 3000, n_samples),
        "poissons_ratio": np.random.uniform(0.3, 0.35, n_samples),
        "thickness": np.random.uniform(3, 7, n_samples),
        "length": np.random.uniform(0.8, 1.2, n_samples),
        "pressure": np.random.uniform(80000, 120000, n_samples),
        "frequency": np.random.uniform(200, 400, n_samples),
    }

    df = pd.DataFrame(data)

    # split complex formulas across lines for readability & flake8
    df["deformation"] = (
        BASELINE["deformation"]
        * (BASELINE["youngs_modulus"] / df["youngs_modulus"])
        * (df["length"] / BASELINE["length"]) ** 2
        * (df["pressure"] / BASELINE["pressure"])
    )

    df["stress"] = (
        BASELINE["stress"] * (df["pressure"] / BASELINE["pressure"]) * (BASELINE["thickness"] / df["thickness"])
    )

    df["strain"] = (
        BASELINE["strain"]
        * (df["stress"] / BASELINE["stress"])
        * (BASELINE["youngs_modulus"] / df["youngs_modulus"])
    )

    df["factor_of_safety"] = BASELINE["factor_of_safety"] * (BASELINE["stress"] / df["stress"])

    df["fatigue_life"] = BASELINE["fatigue_life"] * (BASELINE["stress"] / df["stress"]) ** 2

    df["damage"] = BASELINE["damage"] * (BASELINE["fatigue_life"] / df["fatigue_life"])

    return df


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic wind turbine blade dataset.")
    parser.add_argument("--n", type=int, default=150, help="Number of samples to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--out", type=str, default="data/wind_turbine_blade_data.csv", help="Output CSV path.")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate(n_samples=args.n, seed=args.seed)
    df.to_csv(out_path, index=False)
    print(f"Synthetic dataset generated and saved as '{out_path}' (n={args.n})")


if __name__ == "__main__":
    main()
