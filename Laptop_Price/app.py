from flask import Flask, request, render_template
import numpy as np
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("LaptopPrice.joblib")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form data (all already numeric due to HTML value attributes)
        brand = int(request.form['brand'])
        processor_brand = int(request.form['processor_brand'])
        processor_name = int(request.form['processor_name'])
        processor_gnrtn = int(request.form['processor_gnrtn'])
        ram_gb = int(request.form['ram_gb'])
        ssd = int(request.form['ssd'])
        hdd = int(request.form['hdd'])
        os = int(request.form['os'])
        os_bit = int(request.form['os_bit'])
        graphic_card_gb = int(request.form['graphic_card_gb'])
        weight = float(request.form['weight'])
        warranty = int(request.form['warranty'])
        touchscreen = int(request.form['Touchscreen'])
        rating = int(request.form['rating'])
        num_ratings = int(request.form['Number of Ratings'])
        num_reviews = int(request.form['Number of Reviews'])

        # Form input array
        input_data = np.array([[brand, processor_brand, processor_name, processor_gnrtn,
                                ram_gb, ssd, hdd, os, os_bit, graphic_card_gb, weight,
                                warranty, touchscreen, rating, num_ratings, num_reviews]])

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        return render_template("index.html", prediction=round(predicted_price, 2))

    except Exception as e:
        return render_template("index.html", prediction=f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
