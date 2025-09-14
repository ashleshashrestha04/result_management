import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def create_sample_data():
    """Create sample student performance data"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'race_ethnicity': np.random.choice(['group A', 'group B', 'group C', 'group D', 'group E'], n_samples),
        'parental_level_of_education': np.random.choice([
            'some high school', 'high school', 'some college', 
            'associate\'s degree', 'bachelor\'s degree', 'master\'s degree'
        ], n_samples),
        'lunch': np.random.choice(['standard', 'free/reduced'], n_samples),
        'test_preparation_course': np.random.choice(['none', 'completed'], n_samples),
        'study_hours_per_week': np.random.randint(5, 40, n_samples),
        'attendance_rate': np.random.uniform(70, 100, n_samples),
        'previous_grade': np.random.uniform(50, 95, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (math_score) based on features with some noise
    df['math_score'] = (
        df['study_hours_per_week'] * 1.2 +
        df['attendance_rate'] * 0.3 +
        df['previous_grade'] * 0.4 +
        (df['test_preparation_course'] == 'completed') * 5 +
        (df['lunch'] == 'standard') * 3 +
        np.random.normal(0, 5, n_samples)
    ).clip(0, 100)
    
    return df

def train_student_performance_model():
    """Train and save the student performance prediction model"""
    
    # Create or load your dataset
    df = create_sample_data()  # Replace with your actual dataset loading
    
    print("Dataset shape:", df.shape)
    print("Dataset columns:", df.columns.tolist())
    
    # Prepare features
    le_dict = {}
    categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
    
    # Encode categorical variables
    for col in categorical_columns:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col])
        le_dict[col] = le
    
    # Select features for the model
    feature_columns = [
        'gender_encoded', 'race_ethnicity_encoded', 'parental_level_of_education_encoded',
        'lunch_encoded', 'test_preparation_course_encoded', 'study_hours_per_week',
        'attendance_rate', 'previous_grade'
    ]
    
    X = df[feature_columns]
    y = df['math_score']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Performance:")
    print(f"MSE: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")
    
    # Save the model and preprocessors
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    joblib.dump(model, os.path.join(model_dir, 'student_performance_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(le_dict, os.path.join(model_dir, 'label_encoders.pkl'))
    joblib.dump(feature_columns, os.path.join(model_dir, 'feature_columns.pkl'))
    
    print("Model and preprocessors saved successfully!")
    
    return model, scaler, le_dict, feature_columns

if __name__ == "__main__":
    train_student_performance_model()
