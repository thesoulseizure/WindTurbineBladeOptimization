from src.windturbine.data import generate


def test_generate_basic():
    df = generate(n_samples=10, seed=0)
    assert len(df) == 10
    # basic columns present
    for c in ["deformation", "stress", "strain", "factor_of_safety", "fatigue_life", "damage"]:
        assert c in df.columns
