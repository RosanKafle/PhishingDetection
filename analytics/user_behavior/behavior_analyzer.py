import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class BehaviorAnalyzer:
    # ... your existing code ...
    
    def simulate_campaign_effectiveness_over_time(self, weeks=8, campaigns_per_week=3):
        """Simulating phishing campaign effectiveness trends over time"""
        
        # Generate date range
        start_date = datetime.now() - timedelta(weeks=weeks)
        dates = [start_date + timedelta(days=i) for i in range(weeks * 7)]
        
        campaign_data = []
        campaign_id = 1
        
        for week in range(weeks):
            for campaign in range(campaigns_per_week):
                # Campaign date
                campaign_date = start_date + timedelta(weeks=week, days=np.random.randint(0, 7))
                
                # Simulate different campaign types
                campaign_types = ['email_phishing', 'social_media', 'smishing', 'vishing', 'spear_phishing']
                campaign_type = np.random.choice(campaign_types)
                
                # Simulate effectiveness (declining over time as users get trained)
                base_success_rate = 0.15  # 15% base success rate
                time_decay = week * 0.01  # 1% improvement per week due to training
                type_modifier = {
                    'email_phishing': 0.05,
                    'social_media': 0.08, 
                    'smishing': 0.04,
                    'vishing': 0.06,
                    'spear_phishing': 0.12
                }.get(campaign_type, 0.05)
                
                success_rate = max(0.02, base_success_rate + type_modifier - time_decay)
                
                # Simulate targets and responses
                targets = np.random.randint(50, 200)
                successful_clicks = int(targets * success_rate)
                reported_as_phishing = int(successful_clicks * np.random.uniform(0.1, 0.3))
                
                campaign_data.append({
                    'campaign_id': campaign_id,
                    'date': campaign_date,
                    'week': week + 1,
                    'campaign_type': campaign_type,
                    'targets': targets,
                    'successful_clicks': successful_clicks,
                    'click_rate': success_rate,
                    'reported_count': reported_as_phishing,
                    'reporting_rate': reported_as_phishing / max(1, successful_clicks)
                })
                
                campaign_id += 1
        
        return pd.DataFrame(campaign_data)
    
    def analyze_department_improvement_trends(self, weeks=8):
        """Analyzing how departments improve over time"""
        
        departments = ['Finance', 'HR', 'IT', 'Marketing', 'Operations']
        trend_data = []
        
        for week in range(1, weeks + 1):
            for dept in departments:
                # Simulate improvement over time
                base_risk = {
                    'Finance': 0.092, 'HR': 0.076, 'IT': 0.095, 
                    'Marketing': 0.089, 'Operations': 0.087
                }[dept]
                
                # Weekly improvement (1-2% reduction per week)
                improvement = week * np.random.uniform(0.01, 0.02)
                current_risk = max(0.02, base_risk - improvement)
                
                # Training completion improvement
                base_training = np.random.uniform(0.6, 0.8)
                training_improvement = week * 0.05  # 5% more training completion per week
                current_training = min(1.0, base_training + training_improvement)
                
                # Security awareness improvement
                base_awareness = np.random.uniform(70, 80)
                awareness_improvement = week * 2  # 2 points improvement per week
                current_awareness = min(100, base_awareness + awareness_improvement)
                
                trend_data.append({
                    'week': week,
                    'department': dept,
                    'click_through_rate': current_risk,
                    'training_completed': current_training,
                    'security_awareness_score': current_awareness,
                    'improvement_rate': (base_risk - current_risk) / base_risk if base_risk > 0 else 0
                })
        
        return pd.DataFrame(trend_data)
    
    def measure_training_effectiveness(self, weeks=8):
        """Measuring training program effectiveness over time"""
        
        training_data = []
        
        for week in range(1, weeks + 1):
            # Simulate training sessions
            sessions_held = np.random.randint(2, 6)
            
            for session in range(sessions_held):
                attendees = np.random.randint(15, 40)
                completion_rate = min(1.0, 0.7 + (week * 0.03))  # Improving completion
                
                # Pre/post training click rates
                pre_training_rate = np.random.uniform(0.12, 0.18)
                improvement = week * 0.01 + np.random.uniform(0.02, 0.05)
                post_training_rate = max(0.02, pre_training_rate - improvement)
                
                training_data.append({
                    'week': week,
                    'session_id': f"W{week}S{session+1}",
                    'attendees': attendees,
                    'completion_rate': completion_rate,
                    'pre_training_click_rate': pre_training_rate,
                    'post_training_click_rate': post_training_rate,
                    'effectiveness': (pre_training_rate - post_training_rate) / pre_training_rate
                })
        
        return pd.DataFrame(training_data)
