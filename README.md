# Wind Turbine Blade Design Optimization

## Overview
This project leverages machine learning to predict the performance of wind turbine blades based on material properties, geometry, and operating conditions. It builds on ANSYS simulation data for a blade made of Aluminium Alloy, extending the analysis to a broader range of conditions using a synthetic dataset. A Flask web app allows users to input design parameters and get predictions for deformation, stress, strain, factor of safety, fatigue life, and damage, enabling engineers to optimize blade designs without running time-intensive simulations.

The app is deployed at [insert Render URL here, e.g., https://wind-turbine-blade-optimization.onrender.com].

## Project Goals
- Predict wind turbine blade performance metrics (deformation, stress, strain, factor of safety, fatigue life, and damage) using machine learning.
- Enable optimization of blade design by exploring different materials, geometries, and operating conditions.
- Deploy a user-friendly web app for interactive predictions, making the tool accessible to engineers and researchers.

## Tech Stack
- **Programming Language**: Python 3.10.17
- **Libraries**:
  - `pandas`: Data manipulation and synthetic dataset generation.
  - `scikit-learn`: Random Forest Regressor for multi-output prediction.
  - `joblib`: Saving and loading the trained model.
  - `numpy`: Numerical operations for data generation and processing.
  - `flask`: Web app framework for building the interactive interface.
  - `gunicorn`: WSGI server for deployment on Render.
- **Development Environment**: Local machine with zsh shell (macOS/Linux).
- **Version Control**: Git and GitHub for repository management.
- **Deployment Platform**: Render (free tier).
- **Hardware**: Standard laptop (no GPU required).

## Methodology
1. **Data Generation**:
   - Used simulation results from ANSYS Workbench (Transient Structural, Modal, Harmonic, and Fatigue analyses) as a baseline:
     - Material: Aluminium Alloy.
     - Deformation: 0.046712 mm.
     - Stress (Von-Mises): 1.385 MPa.
     - Strain: 7.73732e-6.
     - Factor of Safety: 15.
     - Fatigue Life: 1e6 cycles.
     - Damage: 1000.
   - Generated a synthetic dataset (`wind_turbine_blade_data.csv`) with 150 data points by varying:
     - Material Properties: Young’s Modulus (50–90 GPa), Density (2500–3000 kg/m³), Poisson’s Ratio (0.3–0.35).
     - Geometry: Blade Thickness (3–7 mm), Blade Length (0.8–1.2 m).
     - Operating Conditions: Pressure (80,000–120,000 Pa), Frequency (200–400 Hz).
   - Scaled the performance metrics (deformation, stress, strain, etc.) based on physical relationships (e.g., deformation scales inversely with Young’s Modulus).

2. **Modeling**:
   - Loaded the synthetic dataset and split it into 80% training and 20% testing sets (`random_state=42` for reproducibility).
   - Trained a Random Forest Regressor (`n_estimators=100`) to predict all six performance metrics simultaneously.
   - Evaluated the model:
     - Training R² Score: ~0.98 (indicating a good fit to the training data).
     - Testing R² Score: ~0.93 (indicating strong generalization to unseen data).
   - Saved the trained model as `rf_blade_model.pkl` for use in the web app.

3. **Web App Development**:
   - Built a Flask web app (`app.py`) to serve predictions:
     - `/` route: Displays an input form (`index.html`) for users to enter design parameters.
     - `/predict` route: Processes inputs, makes predictions using the Random Forest model, and displays results (`result.html`).
   - Designed user-friendly templates with basic CSS styling for a clean interface.
   - Configured the app to run on port 5002 locally to avoid conflicts with other projects.

4. **Deployment Preparation**:
   - Added a `requirements.txt` file listing all dependencies for reproducibility.
   - Included a `.gitignore` file to exclude unnecessary files (e.g., Python cache, virtual environments) while keeping the model file (`rf_blade_model.pkl`).
   - Pushed the project to GitHub (`https://github.com/thesoulseizure/WindTurbineBladeOptimization`) for deployment on Render.

## Files
- `generate_synthetic_data.py`: Script to generate the synthetic dataset based on ANSYS simulation results.
- `train_blade_model.py`: Script to train the Random Forest model and save it as `rf_blade_model.pkl`.
- `app.py`: Flask web app for serving predictions, running on port 5002 locally.
- `templates/index.html`: HTML form for user input of blade design parameters.
- `templates/result.html`: HTML page to display prediction results.
- `rf_blade_model.pkl`: Saved Random Forest model for predictions.
- `wind_turbine_blade_data.csv`: Synthetic dataset with 150 data points.
- `requirements.txt`: List of Python dependencies for the project.
- `.gitignore`: File to exclude unnecessary files from version control.
- `README.md`: Project documentation (this file).

## How to Run Locally
1. **Prerequisites**:
   - Python 3.10.17
   - Install required libraries:
     ```
     pip install -r requirements.txt
     ```
2. **Clone the Repository**:
   ```
   git clone https://github.com/thesoulseizure/WindTurbineBladeOptimization.git
   cd WindTurbineBladeOptimization
   ```
3. **Generate the Synthetic Dataset** (if not already present):
   ```
   python3 generate_synthetic_data.py
   ```
   This creates `wind_turbine_blade_data.csv`.
4. **Train the Model** (if not already done):
   ```
   python3 train_blade_model.py
   ```
   This creates `rf_blade_model.pkl`.
5. **Run the Web App**:
   ```
   python3 app.py
   ```
   - Open `http://127.0.0.1:5002` in your browser to use the app.
   - Enter blade design parameters (e.g., Young’s Modulus = 70 GPa, Density = 2700 kg/m³, Poisson’s Ratio = 0.33, Thickness = 5 mm, Length = 1 m, Pressure = 101325 Pa, Frequency = 300 Hz) to get predictions.

## Access the Deployed App
- The web app is deployed at [insert Render URL here, e.g., https://wind-turbine-blade-optimization.onrender.com].
- Enter blade design parameters to get performance predictions.
- If not yet deployed, follow the deployment instructions below.

## Deployment on Render
1. **Push to GitHub** (if not already done):
   ```
   git add .
   git commit -m "Finalized project for deployment"
   git push origin main
   ```
2. **Create a Web Service on Render**:
   - Go to `https://render.com` and sign in.
   - Create a new web service and connect your `WindTurbineBladeOptimization` repository.
   - Configure the service:
     - Name: `wind-turbine-blade-optimization`
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Click “Create Web Service” to deploy.
3. **Update the README**:
   - After deployment, update this README with the Render URL provided (e.g., `https://wind-turbine-blade-optimization.onrender.com`).

## Future Improvements
- **Real-World Data Integration**: Incorporate experimental or additional simulation data to improve model accuracy beyond synthetic data.
- **Visualizations**: Add plots (e.g., predicted vs. actual metrics, feature importance) to the web app for better insights.
- **Optimization Algorithms**: Implement optimization techniques (e.g., genetic algorithms) to suggest the best design parameters for desired performance.
- **Input Validation**: Add checks to ensure user inputs are within realistic ranges (e.g., Young’s Modulus between 50–90 GPa).

## Acknowledgments
- Based on ANSYS simulation data from the mini project *"Analysis of Wind Turbine Blade"* .

