import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, r2_score

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('df.csv')

# Features: Selecting relevant columns for prediction
X = df[['month', 'day_of_week', 'product_category_name']]
y_sales = df['daily_sales_count']

# One-hot encode product_category_name if needed
X = pd.get_dummies(X, columns=['product_category_name'])

# Print input shapes
print("Shape of X before train-test split:", X.shape)
print("Shape of y_sales:", y_sales.shape)

# Split the data into training and test sets
X_train_sales, X_test_sales, y_train_sales, y_test_sales = train_test_split(X, y_sales, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_sales_scaled = scaler.fit_transform(X_train_sales)
X_test_sales_scaled = scaler.transform(X_test_sales)

# Print scaled data shapes
print("Shape of X_train_sales_scaled:", X_train_sales_scaled.shape)
print("Shape of X_test_sales_scaled:", X_test_sales_scaled.shape)
print("Shape of y_train_sales:", y_train_sales.shape)
print("Shape of y_test_sales:", y_test_sales.shape)

# Define a function to build the model
def build_model(input_shape):
    model = Sequential([
        Dense(64, activation='relu', input_shape=input_shape),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)  # Output layer for regression, no activation function
    ])
    return model

# Build the model
model_sales = build_model(input_shape=(X_train_sales_scaled.shape[1],))

# Compile the model
model_sales.compile(optimizer=Adam(), loss='mean_squared_error')

# Define early stopping criteria
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history_sales = model_sales.fit(X_train_sales_scaled, y_train_sales, epochs=20, batch_size=32, validation_data=(X_test_sales_scaled, y_test_sales), callbacks=[early_stopping])

# Predict on test set
y_pred_sales = model_sales.predict(X_test_sales_scaled).flatten()

# Evaluate model
mse_sales = mean_squared_error(y_test_sales, y_pred_sales)
r2_sales = r2_score(y_test_sales, y_pred_sales)

print("Daily Sales Count Model - Mean Squared Error:", mse_sales)
print("Daily Sales Count Model - R-squared:", r2_sales)

# Save the model
model_sales.save('daily_sales_count_model.h5')
print("Model saved as 'daily_sales_count_model.h5'")
