import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class PerformanceLogger:
    def __init__(self):
        self.performance_metrics = []
        
    def log_performance(self, precision, recall, f1_score, roc_auc, timestamp=None):
        """Log model performance metrics"""
        if timestamp is None:
            timestamp = datetime.now()
            
        metrics = {
            'timestamp': timestamp,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'roc_auc': roc_auc
        }
        self.performance_metrics.append(metrics)
        
    def generate_performance_chart(self):
        """Create performance visualization"""
        if len(self.performance_metrics) == 0:
            return "No performance data to visualize"
            
        df = pd.DataFrame(self.performance_metrics)
        
        plt.figure(figsize=(12, 8))
        
        # Performance metrics over time
        plt.subplot(2, 2, 1)
        plt.plot(df.index, df['precision'], label='Precision', marker='o')
        plt.plot(df.index, df['recall'], label='Recall', marker='s')
        plt.plot(df.index, df['f1_score'], label='F1-Score', marker='^')
        plt.title('Model Performance Metrics Over Time')
        plt.legend()
        plt.ylabel('Score')
        
        # ROC-AUC trend
        plt.subplot(2, 2, 2)
        plt.plot(df.index, df['roc_auc'], color='red', marker='o')
        plt.title('ROC-AUC Score Trend')
        plt.ylabel('ROC-AUC Score')
        
        plt.tight_layout()
        plt.savefig('charts/model_performance_tracking.png', dpi=300)
        plt.show()
        
        return "Performance chart saved to charts/model_performance_tracking.png"

# Initialize logger
perf_logger = PerformanceLogger()