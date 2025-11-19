
# Wind Turbine Blade Optimization – Technical Report

## 1. Introduction

This technical report presents the development of a **machine‑learning–based predictive framework** for wind turbine blade performance analysis.  
The project integrates:

- **Finite Element Analysis (FEA)** concepts (geometry, meshing, load cases)
- **Synthetic scientific data generation**
- **Multi‑output regression modeling**
- **Interactive predictor web application (Flask)**
- **Visualization and evaluation pipelines**

The objective is to emulate real‑world engineering workflows used in **digital twins**, **design optimization**, and **predictive maintenance** while maintaining research‑grade rigor.

---

## 2. Problem Statement

Wind turbine blades operate under:

- aerodynamic forces  
- centrifugal loads  
- material fatigue  
- structural vibrations  

Evaluating their performance typically requires **computationally expensive simulations** or **laboratory experiments**.

The goal of this project is to:

> **Build a fast surrogate model** capable of predicting key structural responses using input parameters such as material properties, blade geometry, and operating conditions.

This enables:

- rapid design iteration  
- real‑time evaluation  
- stress–strain insight  
- fatigue and life estimation  

---

## 3. Methodology Overview

The full workflow includes:

1. **Data Generation**
   - Synthetic dataset generation using physics‑informed relationships.
   - Noise injection to simulate real world variability.
2. **Feature Engineering**
   - 7 input features  
   - 6 output performance metrics  
3. **Training Pipeline**
   - Multi‑output Random Forest Regression  
   - Train/test split & evaluation
4. **Model Deployment**
   - Flask web interface  
   - REST API endpoints  
5. **Visualization**
   - Correlation heatmap  
   - Feature importance  
   - Prediction diagnostics  
6. **Documentation & Reproducibility**
   - Jupyter notebooks  
   - Automated plots  
   - Technical diagrams  

---

## 4. Dataset Description

### **Input Features**
| Feature | Description |
|--------|-------------|
| Young’s Modulus (GPa) | Material stiffness |
| Density (kg/m³) | Material density |
| Poisson's Ratio | Material lateral contraction ratio |
| Thickness (mm) | Blade shell thickness |
| Length (m) | Blade length |
| Pressure (Pa) | Aerodynamic surface pressure |
| Frequency (Hz) | Vibration / operating frequency |

### **Predicted Outputs**
| Metric | Meaning |
|--------|---------|
| Deformation (mm) | Tip displacement |
| Stress (MPa) | Von Mises stress |
| Strain | Unit deformation |
| Factor of Safety | Strength utilization |
| Fatigue Life (cycles) | Expected operational cycles |
| Damage | Energy-based damage index |

---

## 5. Data Generation Model

Synthetic data follows physically meaningful relationships.

Example deformation model:

\[
\delta \propto rac{PL^3}{EI}
\]

Simplified synthetic form:

\[
\delta = rac{L^3 \cdot P}{E \cdot t} + noise
\]

Stress model:

\[
\sigma \propto rac{P}{t}
\]

Fatigue life:

\[
N_f \propto rac{1}{\sigma^m}
\]

Noise and random perturbations are added to emulate simulation‑based datasets.

---

## 6. Model Architecture

### **Algorithm:**  
**Random Forest Regressor (Multi‑Output)**  
- Handles nonlinear interactions  
- Provides feature importance  
- Robust under noisy physics‑derived data  

### **Training Metrics**
- R² (train and test)
- Residual analysis
- Error distribution plots  

---

## 7. Visualization Outputs

Figures included in `/reports/figures`:

- **Input feature distributions**  
- **Correlation heatmap**  
- **Feature importance rank**  
- **Actual vs Predicted plots**  
- **Residual histograms**  
- Engineering‑style plots: deformation vs length, stress vs pressure, etc.

---

## 8. Engineering Diagrams from Project Assets

Figures extracted from FEA study:

Figures extracted from the FEA study:

### Blade geometry
![Geometry](../assets/geometry.png)

### Mesh diagram
![Mesh diagram](../assets/mesh-diagram.png)

### Mesh details
![Mesh details](../assets/mesh-details.png)

---

### Case 1 — FEA study outputs

#### Input conditions
![Case 1 input](../assets/case1-input.png)

#### Deformation (transient/modal)
![Case 1 deformation](../assets/case1-deformation.png)

#### Stress (von-Mises)
![Case 1 stress](../assets/case1-stress.png)

#### Strain
![Case 1 strain](../assets/case1-strain.png)

#### Factor of Safety
![Case 1 factor of safety](../assets/case1-safety%20factor.png)

---

### Case 2 — Harmonic / Frequency response
![Case 2 output](../assets/case2-output.png)

---

### Case 3 — Fatigue analysis

#### Damage map
![Case 3 damage](../assets/case3-damage.png)

#### Fatigue life
![Case 3 life](../assets/case3-life.png)

---

### Summary / Combined results
![Results overview](../assets/results.png)

---

## 9. Web Application

The predictor app supports:

- Form‑based input  
- Real‑time prediction  
- JSON API endpoints  
- Fully containerized structure (`src/windturbine/app.py`)  

Outputs displayed cleanly with engineering units.

---

## 10. Results Summary

- Model captures general physical trends:
  - Longer blades deform more  
  - Higher pressure → higher stress  
  - Higher stress → reduced fatigue life  
- Surrogate model provides **rapid millisecond‑level inference**  
- Good baseline accuracy for digital twin prototyping  

---

## 11. Repository Architecture

```
WindTurbineBladeOptimization/
│
├── assets/                   # PPT screenshots, engineering diagrams
├── reports/figures/          # Auto‑generated plots
├── data/                     # Synthetic datasets
├── models/                   # Trained ML models
├── src/
│   └── windturbine/
│       ├── generate.py       # Synthetic data generator
│       ├── train.py          # ML training pipeline
│       ├── visualization.py  # Plot generator
│       └── app.py            # Flask web app
├── tests/                    # Unit tests (pytest)
└── TECHNICAL_REPORT.md       # This document
```

---

## 12. Conclusion

This project showcases:

- Modern engineering workflow  
- ML surrogate modeling  
- FEA-inspired simulation logic  
- Deployment-ready prediction interface  
- Research‑grade documentation  

It serves as a foundation for:

- Digital twin pipelines  
- Optimization studies  
- Structural health monitoring  
- Material and geometry research  

---

## 13. Future Scope

- Integrate real FEA datasets (ANSYS/Abaqus)
- Neural network surrogate models (PINNs, DeepONet)
- Reinforcement learning for design optimization
- Full digital‑twin dashboard
- Time‑series fatigue modeling

---

## 14. References

- Wind turbine structural mechanics literature  
- Random Forest Regression – Breiman (2001)  
- Fatigue life estimation methods (Basquin equation)  
- Digital twin engineering frameworks  

---

*End of Report*
