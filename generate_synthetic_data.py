import numpy as np
import pandas as pd

# Baseline values from your simulation (Aluminium Alloy)
baseline = {
    'youngs_modulus': 70,  # GPa
    'density': 2700,  # kg/m^3
    'poissons_ratio': 0.33,
    'thickness': 5,  # mm
    'length': 1,  # m
    'pressure': 101325,  # Pa
    'frequency': 300,  # Hz
    'deformation': 0.046712,  # mm
    'stress': 1.385,  # MPa
    'strain': 7.73732e-6,
    'factor_of_safety': 15,
    'fatigue_life': 1e6,  # cycles
    'damage': 1000
}

# Number of synthetic data points
n_samples = 150

# Generate synthetic data by varying parameters
np.random.seed(42)
data = {
    'youngs_modulus': np.random.uniform(50, 90, n_samples),
    'density': np.random.uniform(2500, 3000, n_samples),
    'poissons_ratio': np.random.uniform(0.3, 0.35, n_samples),
    'thickness': np.random.uniform(3, 7, n_samples),
    'length': np.random.uniform(0.8, 1.2, n_samples),
    'pressure': np.random.uniform(80000, 120000, n_samples),
    'frequency': np.random.uniform(200, 400, n_samples)
}

# Calculate scaled outputs
df = pd.DataFrame(data)
df['deformation'] = baseline['deformation'] * (baseline['youngs_modulus'] / df['youngs_modulus']) * (df['length'] / baseline['length'])**2 * (df['pressure'] / baseline['pressure'])
df['stress'] = baseline['stress'] * (df['pressure'] / baseline['pressure']) * (baseline['thickness'] / df['thickness'])
df['strain'] = baseline['strain'] * (df['stress'] / baseline['stress']) * (baseline['youngs_modulus'] / df['youngs_modulus'])
df['factor_of_safety'] = baseline['factor_of_safety'] * (baseline['stress'] / df['stress'])
df['fatigue_life'] = baseline['fatigue_life'] * (baseline['stress'] / df['stress'])**2  # Simplified S-N curve
df['damage'] = baseline['damage'] * (baseline['fatigue_life'] / df['fatigue_life'])

# Save to CSV
df.to_csv('wind_turbine_blade_data.csv', index=False)
print("Synthetic dataset generated and saved as 'wind_turbine_blade_data.csv'")