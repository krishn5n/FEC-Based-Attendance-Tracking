import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the data from CSV
data = pd.read_csv('data3.csv')

# Convert string values to float using iloc
data.iloc[:, 2] = data.iloc[:, 2].str.replace(r'\D', '', regex=True).astype(float)  # 'Previous Attendance'
data.iloc[:, 3] = data.iloc[:, 3].str.replace(r'\D', '', regex=True).astype(float)  # 'Future Attendance'

# Extract features and target using iloc
X = data.iloc[:, 2:3]  # 'Previous Attendance' column
y = data.iloc[:, 3]    # 'Future Attendance' column

# Initialize the Linear Regression model
lr = LinearRegression()

# Train the model
lr.fit(X, y)

# Predict the future attendance
new_predictions = lr.predict(X)

# Print the predicted future attendance values
print("Predicted Future Attendance:")
print(new_predictions)

# Calculate the mean squared error
mse = mean_squared_error(y, new_predictions)

# Print the mean squared error
print("Mean Squared Error: ", mse)

# Calculate R-squared (coefficient of determination)
r_squared = r2_score(y, new_predictions)

# Print R-squared
print("R-Squared (Coefficient of Determination): ", r_squared)

# Define your API endpoint URL with Write API Key
api_url = 'https://api.thingspeak.com/update?api_key=CLXCP86IVHLI5CZC'

# Loop through each row and send data to ThingSpeak
for index, row in data.iterrows():
    uid = row.iloc[0]  # Assuming UID is in the first column
    total_attendance = row.iloc[1]  # Assuming Total Attendance is in the second column
    predicted_attendance = new_predictions[index]  # Predicted attendance for the current row

    # Prepare data to send to ThingSpeak
    data_to_send = {'field1': uid, 'field2': total_attendance, 'field3': predicted_attendance}

    # Send data to ThingSpeak
    response = requests.post(api_url, data=data_to_send)
    print(response.text)  # Print the response from ThingSpeak
