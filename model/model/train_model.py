import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import joblib

def train_and_save_best_model(data_path, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Load Dataset
    df = pd.read_csv(data_path)
    
    # Normalize column names to lowercase
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Feature Engineering: Extract the Brand/Company from the Car Name string
    df['brand'] = df['car_name'].apply(lambda x: str(x).split()[0])
    
    # Separate Features and Target
    X = df.drop(columns=['selling_price', 'car_name'])
    y = df['selling_price']
    
    # Identify feature pipelines
    numerical_cols = ['year', 'present_price', 'kms_driven', 'owner']
    categorical_cols = ['brand', 'fuel_type', 'seller_type', 'transmission']
    
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define Regressors
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(random_state=42, n_estimators=100),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }
    
    best_r2 = -float('inf')
    best_pipeline = None
    best_model_name = ""
    performance_metrics = {}

    print("--- Evaluating Machine Learning Regression Models ---")
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
        pipeline.fit(X_train, y_train)
        
        preds = pipeline.predict(X_test)
        r2 = r2_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)
        
        performance_metrics[name] = {'R2': r2, 'MAE': mae, 'RMSE': rmse}
        print(f"{name} -> R² Score: {r2:.4f} | MAE: {mae:.4f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_pipeline = pipeline
            best_model_name = name

    print(f"\n🏆 Chosen Model: {best_model_name} (R²: {best_r2:.4f})")
    
    model_payload = {
        'pipeline': best_pipeline,
        'metrics': performance_metrics[best_model_name],
        'model_name': best_model_name
    }
    
    model_save_path = os.path.join(save_dir, 'car_price_model.pkl')
    joblib.dump(model_payload, model_save_path)
    print(f"Artifact successfully saved to: {model_save_path}")

if __name__ == '__main__':
    train_and_save_best_model('dataset.csv', 'model')