from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model and encoders once at startup
model = joblib.load('AQI_Model.joblib')
country_encoder = joblib.load('country_encoder.joblib')
city_encoder = joblib.load('city_encoder.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        country = request.form['country'].strip()
        city = request.form['city'].strip()
        aqi_value = int(request.form['aqi_value'])
        co_value = int(request.form['co_value'])
        ozone_value = int(request.form['ozone_value'])
        no2_value = int(request.form['no2_value'])
        pm25_value = int(request.form['pm25_value'])

        # Check if values are in known encoder classes
        if country not in country_encoder.classes_:
            return f"Error: Country '{country}' not recognized."

        if city not in city_encoder.classes_:
            return f"Error: City '{city}' not recognized."

        # Encode using LabelEncoder
        country_encoded = country_encoder.transform([country])[0]
        city_encoded = city_encoder.transform([city])[0]

        # Feature vector
        features = np.array([[country_encoded, city_encoded, aqi_value, co_value, ozone_value, no2_value, pm25_value]])

        # Make prediction
        prediction = model.predict(features)[0]

        # Display result
        return render_template('index.html', prediction=prediction, range=range)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
