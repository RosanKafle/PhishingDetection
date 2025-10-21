import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_demo_visualizations():
    try:
        df = pd.read_csv('combined_threats_scored.csv')
        print(f"Creating dashboard for {len(df)} threat URLs...")
        
        # Create figure with multiple subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Threat sources pie chart
        source_counts = df['source'].value_counts()
        ax1.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Threat Sources Distribution')
        ax1.axis('equal')
        
        # 2. Threat scores histogram
        ax2.hist(df['threat_score'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        ax2.set_title('Threat Score Distribution')
        ax2.set_xlabel('Threat Score')
        ax2.set_ylabel('Count')
        ax2.grid(True, alpha=0.3)
        
        # 3. Threat levels bar chart
        level_counts = df['threat_level'].value_counts()
        colors = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'lightgreen', 'INFORMATIONAL': 'lightblue'}
        bar_colors = [colors.get(level, 'gray') for level in level_counts.index]
        ax3.bar(level_counts.index, level_counts.values, color=bar_colors, edgecolor='black')
        ax3.set_title('Threat Levels Distribution')
        ax3.set_xlabel('Threat Level')
        ax3.set_ylabel('Count')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Top 10 suspicious domains (if domain data is available)
        if 'domain' in df.columns:
            top_domains = df['domain'].value_counts().head(10)
            ax4.barh(range(len(top_domains)), top_domains.values, color='lightcoral')
            ax4.set_yticks(range(len(top_domains)))
            ax4.set_yticklabels([dom[:30] + '...' if len(dom) > 30 else dom for dom in top_domains.index])
            ax4.set_title('Top 10 Most Reported Domains')
            ax4.set_xlabel('Count')
        else:
            # Alternative: URL length vs score scatter
            ax4.scatter(df['url'].str.len(), df['threat_score'], alpha=0.5, color='purple')
            ax4.set_title('URL Length vs Threat Score')
            ax4.set_xlabel('URL Length')
            ax4.set_ylabel('Threat Score')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('threat_intelligence_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print summary statistics
        print("\n=== Threat Intelligence Summary ===")
        print(f"Total URLs analyzed: {len(df)}")
        print(f"Average threat score: {df['threat_score'].mean():.2f}")
        print(f"Highest threat score: {df['threat_score'].max()}")
        print("\nThreat Level Distribution:")
        for level, count in df['threat_level'].value_counts().items():
            print(f"  {level}: {count} ({count/len(df)*100:.1f}%)")
        
    except FileNotFoundError:
        print("Error: combined_threats_scored.csv not found. Please run the scoring pipeline first.")
    except Exception as e:
        print(f"Error creating dashboard: {e}")

if __name__ == "__main__":
    create_demo_visualizations()
