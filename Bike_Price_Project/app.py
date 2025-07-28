from flask import Flask, render_template, request,url_for
import joblib
model = joblib.load('model.lb')
app = Flask(__name__)

prediction_history = []

# print(__name__) Magic Keyword
@app.route("/") # Here The / Represent The Root Path. 

# def home():
#     return "Hello Bhai Aaj Flask Pd Rahe Hai"
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/project', methods= ["POST", "GET"])
# def predict():
#     if request.method == 'POST':
#         # The Name Attribute Help To Select The Tag For Backend Processes (Link With Backend). 
#         brand_name = request.form['brand_name']
#         onwer = request.form['owner']
#         age = request.form['age']
#         power = request.form['power']
#         kms_driven = request.form['kms_driven']

#         brand_dict = {
#             'TVS': 1,
#             'Royal Enfield': 2,
#             'Triumph': 3,
#             'Yamaha': 4,
#             'Honda': 5,
#             'Hero': 6,
#             'Bajaj': 7,
#             'Suzuki': 8,
#             'Benelli': 9,
#             'KTM': 10,
#             'Mahindra': 11,
#             'Kawasaki': 12,
#             'Ducati': 13,
#             'Hyosung': 14,
#             'Harley-Davidson': 15,
#             'Jawa': 16,
#             'BMW': 17,
#             'Indian': 18,
#             'Rajdoot': 19,
#             'LML': 20,
#             'Yezdi': 21,
#             'MV': 22,
#             'Ideal': 23
#             }

#         brand_name = brand_dict[brand_name]

#         print("Received Data:- ",brand_name, age, power, kms_driven,onwer)

#         lst_2D = [[brand_name,onwer,age,power,kms_driven]]

#         pred = model.predict(lst_2D)
#         print("Prediction:- ",pred)


#         return render_template('project.html',prediction=int(pred))

@app.route('/project', methods=["POST", "GET"])
def predict():
    # The Name Attribute Help To Select The Tag For Backend Processes (Link With Backend). 
    # It Occur When The User Fill The Details In The Form Then Post Request Will Active. 
    if request.method == 'POST':
        brand_name = request.form['brand_name']
        owner = request.form['owner']
        age = request.form['age']
        power = request.form['power']
        kms_driven = request.form['kms_driven']
        name = brand_name
        owners  = owner
        brand_dict = {
            'TVS': 1, 'Royal Enfield': 2, 'Triumph': 3, 'Yamaha': 4,
            'Honda': 5, 'Hero': 6, 'Bajaj': 7, 'Suzuki': 8,
            'Benelli': 9, 'KTM': 10, 'Mahindra': 11, 'Kawasaki': 12,
            'Ducati': 13, 'Hyosung': 14, 'Harley-Davidson': 15,
            'Jawa': 16, 'BMW': 17, 'Indian': 18, 'Rajdoot': 19,
            'LML': 20, 'Yezdi': 21, 'MV': 22, 'Ideal': 23
        }
        owner_dict = {
            'First Owner':1,
            'Second Owner':2,
            'Third Owner':3,
            'Fourth Owner':4,
        }

        brand_name = brand_dict[brand_name]
        owner = owner_dict[owner]
        lst_2D = [[brand_name, owner, age, power, kms_driven]]

        print("Received Data:", name, age, power, kms_driven, owners)

        pred = model.predict(lst_2D)
        print("Prediction:", pred)

        # History Storing

        prediction_history.append((
            int(pred), owners, name, kms_driven, age, power
        ))
        return render_template('project.html', prediction=int(pred))
        
    # For GET requests: just show the form/page
    return render_template('project.html',prediction=0)

# On POST: it shows the prediction result.
# On GET: it loads the input form page.

@app.route('/history')
def history():
    return render_template('history.html', historical_data=prediction_history)


if __name__ == "__main__":
    app.run(debug=True) # Help To Change In Live (Instantly)




