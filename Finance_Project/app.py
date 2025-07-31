from flask import Flask, render_template, request, redirect, url_for
import numpy as np

import joblib

# Load the model with joblib
model = joblib.load('model.joblib')  

app = Flask(__name__)

# In-memory storage for history (for production, use a database)
history = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/history')
def history_page():
    return render_template('history.html', history=history)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form (you could email/store it)
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"New contact: {name} | {email} | {message}")
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        age = int(request.form['age'])
        sex = 1 if request.form['sex'].lower() == 'male' else 0
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = 1 if request.form['smoker'].lower() == 'yes' else 0
        region = request.form['region'].lower()

        # Simplified encoding for region (single integer, not one-hot)
        region_map = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}
        region_encoded = region_map.get(region, -1)  # fallback to -1 if not found
        
        # Combine features (now only 6 features)
        features = np.array([age, sex, bmi, children, smoker, region_encoded]).reshape(1, -1)


        # Predict
        charges = round(model.predict(features)[0], 2)

        # Save to history
        history.append({
            'age': age,
            'sex': request.form['sex'],
            'bmi': bmi,
            'children': children,
            'smoker': request.form['smoker'],
            'region': region,
            'charges': charges
        })

        return render_template('predict_form.html', prediction=charges)

    return render_template('predict_form.html')  # a form page you should create

if __name__ == '__main__':
    app.run(debug=True)
