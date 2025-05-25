from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
rf_model = joblib.load('rf_blade_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    youngs_modulus = float(request.form['youngs_modulus'])
    density = float(request.form['density'])
    poissons_ratio = float(request.form['poissons_ratio'])
    thickness = float(request.form['thickness'])
    length = float(request.form['length'])
    pressure = float(request.form['pressure'])
    frequency = float(request.form['frequency'])

    # Prepare input data
    input_data = pd.DataFrame({
        'youngs_modulus': [youngs_modulus],
        'density': [density],
        'poissons_ratio': [poissons_ratio],
        'thickness': [thickness],
        'length': [length],
        'pressure': [pressure],
        'frequency': [frequency]
    })

    # Make predictions
    predictions = rf_model.predict(input_data)[0]
    results = {
        'deformation': predictions[0],
        'stress': predictions[1],
        'strain': predictions[2],
        'factor_of_safety': predictions[3],
        'fatigue_life': predictions[4],
        'damage': predictions[5]
    }

    return render_template('result.html', **results)

if __name__ == '__main__':
    app.run(port=5002, debug=True)