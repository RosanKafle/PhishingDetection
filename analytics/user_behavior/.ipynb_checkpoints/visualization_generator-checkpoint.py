import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class UserBehaviorVisualizer:
    def __init__(self):
        self.chart_style = 'seaborn-v0_8'
        
    def _ensure_directory_exists(self, path):
        """Create directory if it doesn't exist"""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
    def plot_department_risk_analysis(self, user_df, save_path="/home/lucifer/Desktop/Project/charts/"):
        """Create comprehensive department risk visualizations"""
        
        # Ensure the charts directory exists
        self._ensure_directory_exists(save_path)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Click-through rates by department
        dept_ctr = user_df.groupby('department')['click_through_rate'].mean()
        axes[0,0].bar(dept_ctr.index, dept_ctr.values, color='coral')
        axes[0,0].set_title('Phishing Click-Through Rate by Department')
        axes[0,0].set_ylabel('Click-Through Rate')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Training completion vs awareness score
        axes[0,1].scatter(user_df['training_completed'], 
                         user_df['security_awareness_score'],
                         alpha=0.6, c=user_df['click_through_rate'], 
                         cmap='RdYlBu_r')
        axes[0,1].set_xlabel('Training Completed (0=No, 1=Yes)')
        axes[0,1].set_ylabel('Security Awareness Score')
        axes[0,1].set_title('Training Impact on Security Awareness')
        
        # 3. Risk level distribution
        risk_dist = user_df['risk_level'].value_counts()
        axes[1,0].pie(risk_dist.values, labels=risk_dist.index, autopct='%1.1f%%')
        axes[1,0].set_title('User Risk Level Distribution')
        
        # 4. Department training effectiveness
        dept_training = user_df.groupby('department').agg({
            'training_completed': 'mean',
            'click_through_rate': 'mean'
        })
        
        x = dept_training['training_completed']
        y = dept_training['click_through_rate']
        axes[1,1].scatter(x, y, s=100, alpha=0.7)
        for i, dept in enumerate(dept_training.index):
            axes[1,1].annotate(dept, (x.iloc[i], y.iloc[i]))
        axes[1,1].set_xlabel('Training Completion Rate')
        axes[1,1].set_ylabel('Click-Through Rate')
        axes[1,1].set_title('Department Training Effectiveness')
        
        plt.tight_layout()
        
        # Save the figure
        output_path = os.path.join(save_path, 'user_behavior_dashboard.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return f"Dashboard saved to {output_path}"
    
    def create_model_monitoring_dashboard(self, model_tracker, perf_logger, save_path="/home/lucifer/Desktop/Project/charts/"):
        """Create model performance monitoring dashboard"""
        
        # Ensure the charts directory exists
        self._ensure_directory_exists(save_path)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Mock additional data for visualization
        predictions_over_time = np.random.choice([0, 1], size=50, p=[0.7, 0.3])
        confidence_scores = np.random.beta(8, 2, size=50)  # Higher confidence generally
        timestamps = pd.date_range('2025-08-01', periods=50, freq='H')
        
        # 1. Predictions over time
        df_pred = pd.DataFrame({
            'timestamp': timestamps,
            'prediction': predictions_over_time,
            'confidence': confidence_scores
        })
        
        daily_predictions = df_pred.groupby(df_pred['timestamp'].dt.date).agg({
            'prediction': ['count', 'sum']
        }).round(2)
        daily_predictions.columns = ['total', 'phishing_detected']
        
        axes[0,0].plot(daily_predictions.index, daily_predictions['total'], 
                      marker='o', label='Total Predictions')
        axes[0,0].plot(daily_predictions.index, daily_predictions['phishing_detected'], 
                      marker='s', label='Phishing Detected', color='red')
        axes[0,0].set_title('Daily Prediction Activity')
        axes[0,0].legend()
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Confidence score distribution
        axes[0,1].hist(confidence_scores, bins=20, alpha=0.7, color='skyblue')
        axes[0,1].axvline(0.7, color='red', linestyle='--', label='Low Confidence Threshold')
        axes[0,1].set_xlabel('Confidence Score')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].set_title('Model Confidence Distribution')
        axes[0,1].legend()
        
        # 3. Model performance metrics (mock data)
        metrics = {
            'Precision': [0.95, 0.93, 0.96, 0.94, 0.95],
            'Recall': [0.92, 0.94, 0.93, 0.95, 0.93],
            'F1-Score': [0.94, 0.94, 0.95, 0.95, 0.94]
        }
        
        for metric, values in metrics.items():
            axes[1,0].plot(range(1, 6), values, marker='o', label=metric)
        axes[1,0].set_xlabel('Week')
        axes[1,0].set_ylabel('Score')
        axes[1,0].set_title('Model Performance Trends')
        axes[1,0].legend()
        axes[1,0].set_ylim([0.9, 1.0])
        
        # 4. Alert summary
        alert_data = {
            'Low Confidence': len(confidence_scores[confidence_scores < 0.7]),
            'High Confidence': len(confidence_scores[confidence_scores >= 0.9]),
            'Medium Confidence': len(confidence_scores[(confidence_scores >= 0.7) & (confidence_scores < 0.9)])
        }
        
        axes[1,1].bar(alert_data.keys(), alert_data.values(), 
                     color=['red', 'green', 'orange'])
        axes[1,1].set_title('Confidence Level Distribution')
        axes[1,1].set_ylabel('Number of Predictions')
        
        plt.tight_layout()
        
        # Save the figure
        output_path = os.path.join(save_path, 'model_monitoring_dashboard.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return f"Model monitoring dashboard saved to {output_path}"

# Initialize visualizer
visualizer = UserBehaviorVisualizer()
