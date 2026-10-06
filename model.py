import pandas as pd
from sklearn.linear_model import LinearRegression

# Load dataset
data = pd.read_csv("data/energy_data.csv")

# Input features
X = data[[
    "hours",
    "appliances",
    "temperature",
    "previous_usage"
]]

# Target value
y = data["current_usage"]

# Create and train model
model = LinearRegression()
model.fit(X, y)

# Prediction function
def predict_energy(hours, appliances, temperature, previous_usage):
    prediction = model.predict([[
        hours,
        appliances,
        temperature,
        previous_usage
    ]])

    return round(prediction[0], 2)