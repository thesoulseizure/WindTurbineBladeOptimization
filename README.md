# Wind Turbine Blade Optimization Using Machine Learning

<h1 align="center">🌬️ Wind Turbine Blade Optimization</h1>
<p align="center">
  Machine Learning + Flask Web App for predicting and optimizing wind turbine blade performance.  
</p>
<p align="center">
  <img alt="project-logo" src="https://img.shields.io/badge/Wind%20Turbine%20Blade%20Optimization-Project-blueviolet?style=for-the-badge">
</p>

<p align="center">
  <!-- Status -->
  <a href="https://windturbinebladeoptimization.onrender.com">
    <img alt="deployment" src="https://img.shields.io/badge/Live%20App-Online-success?style=flat-square">
  </a>

  <!-- Python -->
  <img alt="python" src="https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python">

  <!-- License -->
  <a href="./LICENSE">
    <img alt="license" src="https://img.shields.io/badge/License-MIT-green?style=flat-square">
  </a>

  <!-- Build (GitHub Actions) -->
  <a href="https://github.com/TheComputationalCore/WindTurbineBladeOptimization/actions">
    <img alt="build" src="https://img.shields.io/github/actions/workflow/status/TheComputationalCore/WindTurbineBladeOptimization/python-app.yml?style=flat-square&label=CI%20Build">
  </a>

  <!-- Code Style -->
  <img alt="code-style" src="https://img.shields.io/badge/Code%20Style-black-black?style=flat-square">

  <!-- Model -->
  <img alt="model" src="https://img.shields.io/badge/Model-RandomForestRegressor-orange?style=flat-square">

  <!-- Issues -->
  <a href="https://github.com/TheComputationalCore/WindTurbineBladeOptimization/issues">
    <img alt="issues" src="https://img.shields.io/github/issues/TheComputationalCore/WindTurbineBladeOptimization?style=flat-square">
  </a>

  <!-- Stars -->
  <img alt="stars" src="https://img.shields.io/github/stars/TheComputationalCore/WindTurbineBladeOptimization?style=flat-square">
</p>


## 🌬️ Overview
This project presents a complete machine-learning–driven pipeline for **wind turbine blade structural behavior prediction and optimization**.  
It combines **synthetic dataset generation**, **Random Forest regression modeling**, **interactive Flask-based prediction dashboard**, and **comprehensive visualization reports**.  

The goal is to help researchers, engineers, and digital twin developers simulate how turbine blade materials and geometry respond to load, pressure, vibration, and fatigue.

---

## 🚀 Features

### ✔ End-to-end ML pipeline
- Synthetic dataset generation
- Data preprocessing
- Model training and evaluation
- Model serialization using `joblib`

### ✔ Flask web application
- Interactive input form  
- Real-time predictions for:
  - Deformation  
  - Stress  
  - Strain  
  - Factor of safety  
  - Fatigue life  
  - Damage index  

### ✔ Scientific Visualization Suite
- Input distribution plots  
- Correlation heatmaps  
- Scatter relationships  
- Model feature importance (Tree-based)  
- Actual vs Predicted curves  
- Residual analysis  
- Engineering relationship plots  

All charts saved under `/reports/figures`.

### ✔ Fully Modular Architecture
- `src/windturbine/data` → dataset generation  
- `src/windturbine/model` → ML model training  
- `src/windturbine/app` → web app  
- `src/windturbine/visualization` → plotting suite  
- `docs/` → reports & documentation  
- `assets/` → screenshots, extracted images  

---

## 🧰 Tech Stack

| Layer | Technology |
|------|------------|
| **Backend** | Python 3, Flask |
| **Machine Learning** | Scikit-Learn, NumPy, Pandas |
| **Visualization** | Matplotlib, Seaborn |
| **Deployment** | Render.com |
| **Packaging** | `joblib`, modular Python architecture |
| **Version Control** | Git + GitHub |

---

## 🌐 Live Deployment

The full web application is deployed at:

👉 **https://windturbinebladeoptimization.onrender.com**

---

## 📁 Project Structure

```
WindTurbineBladeOptimization/
│
├── assets/                     # screenshots & extracted PPT images
├── docs/
│   └── TECHNICAL_REPORT.md     # full engineering & ML report
│
├── reports/
│   └── figures/                # generated plots
│
├── src/
│   └── windturbine/
│       ├── data_generation.py
│       ├── train.py
│       ├── app.py
│       └── visualization.py
│
├── tests/                      # full CI test suite
│
├── synthetic_data/             # generated datasets
├── models/                     # saved ML models
├── README.md
└── LICENSE
```

---

## 📸 Screenshots

### 🏠 Dashboard  
![Dashboard](screenshots/dashboard.png)

### 🔢 Input Form  
![Form](screenshots/enter_input.png)

### 📊 Prediction Output  
![Results](screenshots/result.png)

---

## 📊 Example Generated Plots

Plots are auto-generated under `/reports/figures`.  
Include:

### Input distributions  
![Input distributions](reports/figures/input_distributions.png)

### Scatter relationships  
![Scatter relationships](reports/figures/scatter_relations.png)

### Correlation heatmap  
![Correlation heatmap](reports/figures/correlation_heatmap.png)

### Feature importance  
![Feature importance](reports/figures/feature_importance.png)

### Actual vs Predicted  
![Actual vs Predicted](reports/figures/actual_vs_predicted.png)

### Residual histograms  
![Residual histograms](reports/figures/residual_histograms.png)
---

## 🧪 Running Locally

### 1️⃣ Create & activate virtual env
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Generate synthetic dataset
```bash
python -m src.windturbine.data_generation --n 5000 --seed 42
```

### 4️⃣ Train the model
```bash
python -m src.windturbine.train
```

### 5️⃣ Run visualization suite
```bash
python -m src.windturbine.visualization
```

### 6️⃣ Start the web app
```bash
python -m src.windturbine.app
```

---

## 🧪 Tests (CI-friendly)

```bash
pytest -q
```

---

## 👤 Author

**Dinesh Chandra — TheComputationalCore**

- GitHub: https://github.com/TheComputationalCore  
- YouTube: https://www.youtube.com/@TheComputationalCore  
- Passion: AI × Simulation × Digital Twins × Computational Engineering  

---

## 📜 License

This project is open-source under the **MIT License**.

---

## ⭐ Acknowledgements

This work is inspired by real-world engineering analysis, structural mechanics, and data-driven digital twin methodologies.

If you like this project, consider ⭐ starring the repo!

