import pandas as pd
import numpy as np
from datetime import datetime
import pickle
from sklearn.ensemble import RandomForestClassifier

class ModelOutputTracker:
    def __init__(self):
        self.predictions_log = []
        self.confidence_log = []
        self.timestamp_log = []
        
    def log_prediction(self, url_features, prediction, confidence_score):
        """Log model predictions with timestamp"""
        self.predictions_log.append({
            'timestamp': datetime.now(),
            'prediction': prediction,
            'confidence': confidence_score,
            'features_hash': hash(str(url_features))
        })
        
    def get_prediction_summary(self):
        """Generate summary statistics of predictions"""
        df = pd.DataFrame(self.predictions_log)
        if len(df) == 0:
            return "No predictions logged yet"
            
        summary = {
            'total_predictions': len(df),
            'phishing_detected': len(df[df['prediction'] == 1]),
            'avg_confidence': df['confidence'].mean(),
            'low_confidence_alerts': len(df[df['confidence'] < 0.7])
        }
        return summary
        
    def identify_edge_cases(self, threshold=0.6):
        """Identify predictions with low confidence scores"""
        df = pd.DataFrame(self.predictions_log)
        edge_cases = df[df['confidence'] < threshold]
        return edge_cases
        
# Initialize tracker
model_tracker = ModelOutputTracker()
