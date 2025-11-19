from generate_synthetic_data import generate
def test_generate_basic():
    df = generate(n_samples=10, seed=0)
    assert len(df) == 10
    expected_cols = {'youngs_modulus','density','poissons_ratio','thickness','length','pressure','frequency',
                    'deformation','stress','strain','factor_of_safety','fatigue_life','damage'}
    assert expected_cols.issubset(set(df.columns))
