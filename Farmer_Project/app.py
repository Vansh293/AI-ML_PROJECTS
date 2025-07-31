from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('farmer.joblib')

# Label index to crop name mapping
label_dict = {
   1:'rice', 2:'maize', 3:'chickpea', 4:'kidneybeans', 5:'pigeonpeas',
       6:'mothbeans', 7:'mungbean', 8:'blackgram', 9:'lentil', 10:'pomegranate',
       11:'banana', 12:'mango', 13:'grapes', 14:'watermelon', 15:'muskmelon', 16:'apple',
       17:'orange', 18:'papaya', 19:'coconut', 20:'cotton', 21:'jute', 22:'coffee'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Make prediction
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)[0]
        predicted_crop = label_dict.get(prediction, "Unknown")

        return render_template('index.html', prediction_text=f"Recommended Crop: {predicted_crop.capitalize()}")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
