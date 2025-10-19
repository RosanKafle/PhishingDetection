#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

def generate_user_behavior_data():
    # Generate campaign effectiveness data
    weeks = 8
    campaign_data = []
    
    for week in range(1, weeks + 1):
        for campaign in range(3):  # 3 campaigns per week
            base_success = 0.15 - (week * 0.01)  # Improving over time
            success_rate = max(0.03, base_success + np.random.uniform(-0.02, 0.02))
            
            targets = np.random.randint(50, 200)
            clicks = int(targets * success_rate)
            
            campaign_data.append({
                'week': week,
                'campaign_type': np.random.choice(['email', 'social', 'sms']),
                'targets': targets,
                'clicks': clicks,
                'success_rate': success_rate * 100
            })
    
    # Generate department improvement data
    departments = ['Finance', 'HR', 'IT', 'Marketing', 'Operations']
    dept_data = []
    
    for week in range(1, weeks + 1):
        for dept in departments:
            base_risk = {'Finance': 9.2, 'HR': 7.6, 'IT': 9.5, 'Marketing': 8.9, 'Operations': 8.7}[dept]
            improvement = week * 0.8  # 0.8% improvement per week
            current_risk = max(2.0, base_risk - improvement)
            
            dept_data.append({
                'week': week,
                'department': dept,
                'risk_score': current_risk,
                'training_completion': min(100, 60 + week * 5)
            })
    
    # Create visualizations
    plt.style.use('dark_background')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10), facecolor='#1a1a1a')
    
    # 1. Campaign effectiveness over time
    campaign_df = pd.DataFrame(campaign_data)
    weekly_avg = campaign_df.groupby('week')['success_rate'].mean()
    ax1.plot(weekly_avg.index, weekly_avg.values, marker='o', color='#00d4aa', linewidth=2)
    ax1.set_title('Campaign Success Rate Over Time', color='white', fontsize=14)
    ax1.set_xlabel('Week', color='white')
    ax1.set_ylabel('Success Rate (%)', color='white')
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#1a1a1a')
    
    # 2. Department risk scores
    dept_df = pd.DataFrame(dept_data)
    latest_week = dept_df[dept_df['week'] == weeks]
    ax2.bar(latest_week['department'], latest_week['risk_score'], color='#f59e0b', alpha=0.8)
    ax2.set_title('Current Department Risk Scores', color='white', fontsize=14)
    ax2.set_ylabel('Risk Score (%)', color='white')
    ax2.tick_params(axis='x', rotation=45, colors='white')
    ax2.set_facecolor('#1a1a1a')
    
    # 3. Training completion trends
    for dept in departments:
        dept_subset = dept_df[dept_df['department'] == dept]
        ax3.plot(dept_subset['week'], dept_subset['training_completion'], 
                marker='o', label=dept, linewidth=2)
    ax3.set_title('Training Completion by Department', color='white', fontsize=14)
    ax3.set_xlabel('Week', color='white')
    ax3.set_ylabel('Completion Rate (%)', color='white')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_facecolor('#1a1a1a')
    
    # 4. Campaign type effectiveness
    type_avg = campaign_df.groupby('campaign_type')['success_rate'].mean()
    colors = ['#ec4899', '#0ea5e9', '#10b981']
    ax4.pie(type_avg.values, labels=type_avg.index, autopct='%1.1f%%', 
           colors=colors, startangle=90)
    ax4.set_title('Campaign Type Effectiveness', color='white', fontsize=14)
    
    plt.tight_layout()
    plt.savefig('user_behavior_dashboard.png', facecolor='#1a1a1a', dpi=150)
    plt.close()
    
    # Generate summary statistics
    summary = {
        'total_campaigns': len(campaign_data),
        'avg_success_rate': f"{campaign_df['success_rate'].mean():.1f}%",
        'improvement_trend': f"{(weekly_avg.iloc[0] - weekly_avg.iloc[-1]):.1f}% reduction",
        'best_department': latest_week.loc[latest_week['risk_score'].idxmin(), 'department'],
        'worst_department': latest_week.loc[latest_week['risk_score'].idxmax(), 'department'],
        'avg_training_completion': f"{dept_df[dept_df['week'] == weeks]['training_completion'].mean():.1f}%"
    }
    
    print("User Behavior Analytics Results:")
    print(f"Total Campaigns Analyzed: {summary['total_campaigns']}")
    print(f"Average Success Rate: {summary['avg_success_rate']}")
    print(f"Improvement Trend: {summary['improvement_trend']}")
    print(f"Best Performing Department: {summary['best_department']}")
    print(f"Needs Attention: {summary['worst_department']}")
    print(f"Average Training Completion: {summary['avg_training_completion']}")
    print("\nDashboard saved as 'user_behavior_dashboard.png'")
    
    return json.dumps(summary)

if __name__ == "__main__":
    generate_user_behavior_data()