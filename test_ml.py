import sys
import os
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_result_management.settings')
django.setup()

# Test the ML model
from ml_models.predictor import predictor

def test_ml_model():
    print("Testing ML Model Integration...")
    print("="*50)
    
    if __name__ == "__main__":
        test_ml_model()
    
    # Sample student data
    test_data = {
        'gender': 'Female',
        'race_ethnicity': 'group B',
        'parental_level_of_education': 'bachelor\'s degree',
        'lunch': 'standard',
        'test_preparation_course': 'completed',
        'study_hours_per_week': 25,
        'attendance_rate': 92.0,
        'previous_grade': 78.5
    }
    
    print("Input Data:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    # Make prediction
    predicted_grade, confidence = predictor.predict_grade(test_data)
    
    print(f"\nPrediction Results:")
    print(f"  Predicted Grade: {predicted_grade}%")
    print(f"  Confidence: {confidence}%")
    
    # Generate recommendations
    recommendations = predictor.generate_recommendations(test_data, predicted_grade)
    
    print(f"\nRecommendations ({len(recommendations)} total):")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. [{rec['category']}] {rec['suggestion']}")
        print(f"     Impact: {rec['impact']}, Priority: {rec['priority']}")
    
    print("="*50)
    print("✅ ML Model Test Completed Successfully!")

if __name__ == "__main__":
    test_ml_model()
