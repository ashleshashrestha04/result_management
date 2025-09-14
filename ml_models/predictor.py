import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings

class StudentPerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and preprocessors"""
        try:
            model_dir = os.path.join(settings.BASE_DIR, 'ml_models')
            print(f"Loading model files from: {model_dir}")
            print(f"Model file: {os.path.join(model_dir, 'student_performance_model.pkl')}")
            print(f"Scaler file: {os.path.join(model_dir, 'scaler.pkl')}")
            print(f"Label encoders file: {os.path.join(model_dir, 'label_encoders.pkl')}")
            print(f"Feature columns file: {os.path.join(model_dir, 'feature_columns.pkl')}")

            self.model = joblib.load(os.path.join(model_dir, 'student_performance_model.pkl'))
            self.scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
            self.label_encoders = joblib.load(os.path.join(model_dir, 'label_encoders.pkl'))
            self.feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))
            print("ML model loaded successfully!")
        except Exception as e:
            print(f"Error loading ML model: {e}")
    
    def preprocess_input(self, student_data):
        """Preprocess input data for prediction"""
        try:
            # Create a DataFrame from input
            df = pd.DataFrame([student_data])
            
            # Encode categorical variables
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            
            for col in categorical_columns:
                if col in df.columns and col in self.label_encoders:
                    le = self.label_encoders[col]
                    # Handle unseen categories
                    df[col + '_encoded'] = df[col].apply(
                        lambda x: le.transform([x])[0] if x in le.classes_ else 0
                    )
                else:
                    df[col + '_encoded'] = 0
            
            # Select and order features according to training
            X = df[self.feature_columns].values
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            return X_scaled
        except Exception as e:
            print(f"Error preprocessing input: {e}")
            return None
    
    def predict_grade(self, student_data):
        """Predict student grade based on input features"""
        if self.model is None:
            return None, "Model not loaded"
        
        X_processed = self.preprocess_input(student_data)
        if X_processed is None:
            return None, "Error processing input data"
        
        try:
            prediction = self.model.predict(X_processed)[0]
            confidence = self.get_prediction_confidence(X_processed)
            return round(prediction, 2), confidence
        except Exception as e:
            return None, f"Error making prediction: {e}"
    
    def get_prediction_confidence(self, X_processed):
        """Calculate prediction confidence based on model uncertainty"""
        try:
            # For Random Forest, we can use the standard deviation of tree predictions
            tree_predictions = []
            for tree in self.model.estimators_:
                tree_pred = tree.predict(X_processed)
                tree_predictions.append(tree_pred[0])
            
            std_dev = np.std(tree_predictions)
            # Convert to confidence percentage (inverse relationship with std dev)
            confidence = max(0, min(100, 100 - (std_dev * 2)))
            return round(confidence, 1)
        except:
            return 85.0  # Default confidence
    
    def generate_recommendations(self, student_data, predicted_grade):
        """Generate improvement recommendations based on student data and prediction"""
        recommendations = []
        
        try:
            study_hours = student_data.get('study_hours_per_week', 0)
            attendance_rate = student_data.get('attendance_rate', 0)
            previous_grade = student_data.get('previous_grade', 0)
            test_prep = student_data.get('test_preparation_course', 'none')
            
            # Study hours recommendations
            if study_hours < 15:
                recommendations.append({
                    'category': 'Study Time',
                    'suggestion': f'Increase study hours from {study_hours} to at least 15-20 hours per week',
                    'impact': 'High',
                    'priority': 1
                })
            elif study_hours < 25:
                recommendations.append({
                    'category': 'Study Time',
                    'suggestion': f'Consider increasing study hours from {study_hours} to 25-30 hours per week for better results',
                    'impact': 'Medium',
                    'priority': 2
                })
            
            # Attendance recommendations
            if attendance_rate < 85:
                recommendations.append({
                    'category': 'Attendance',
                    'suggestion': f'Improve attendance from {attendance_rate:.1f}% to at least 90%',
                    'impact': 'High',
                    'priority': 1
                })
            elif attendance_rate < 95:
                recommendations.append({
                    'category': 'Attendance',
                    'suggestion': f'Maintain consistent attendance above 95% (currently {attendance_rate:.1f}%)',
                    'impact': 'Medium',
                    'priority': 2
                })
            
            # Test preparation recommendations
            if test_prep == 'none':
                recommendations.append({
                    'category': 'Test Preparation',
                    'suggestion': 'Enroll in test preparation courses to boost performance',
                    'impact': 'High',
                    'priority': 1
                })
            
            # Subject-specific recommendations based on predicted grade
            if predicted_grade < 60:
                recommendations.extend([
                    {
                        'category': 'Mathematics',
                        'suggestion': 'Focus on fundamental math concepts and practice daily',
                        'impact': 'High',
                        'priority': 1
                    },
                    {
                        'category': 'Study Strategy',
                        'suggestion': 'Consider getting a tutor or joining study groups',
                        'impact': 'High',
                        'priority': 1
                    }
                ])
            elif predicted_grade < 75:
                recommendations.extend([
                    {
                        'category': 'Mathematics',
                        'suggestion': 'Practice more challenging math problems and review weak areas',
                        'impact': 'Medium',
                        'priority': 2
                    },
                    {
                        'category': 'Study Strategy',
                        'suggestion': 'Create a structured study schedule and use active learning techniques',
                        'impact': 'Medium',
                        'priority': 2
                    }
                ])
            
            # Sort recommendations by priority
            recommendations.sort(key=lambda x: x['priority'])
            
            return recommendations
        
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return [{
                'category': 'General',
                'suggestion': 'Maintain consistent study habits and regular attendance',
                'impact': 'Medium',
                'priority': 1
            }]

# Global predictor instance
predictor = StudentPerformancePredictor()
