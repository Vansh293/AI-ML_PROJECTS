import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your training dataset (replace with correct file name)
df = pd.read_csv('your_training_data.csv')

# Create encoders
country_encoder = LabelEncoder()
city_encoder = LabelEncoder()

# Fit the encoders on original text columns
country_encoder.fit(df['country'])
city_encoder.fit(df['city'])

# Save the encoders
joblib.dump(country_encoder, 'country_encoder.joblib')
joblib.dump(city_encoder, 'city_encoder.joblib')

print("Encoders saved successfully!")
