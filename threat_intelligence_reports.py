from datetime import datetime, timedelta
import pandas as pd

def generate_executive_summary():
    """Generate executive-level threat intelligence report"""
    print("Debug: Loading combined_threats_scored.csv for report generation...")
    df = pd.read_csv('combined_threats_scored.csv')

    # Calculate key metrics
    total_threats = len(df)
    critical_threats = len(df[df['threat_level'] == 'CRITICAL'])
    avg_score = df['threat_score'].mean()

    # Recent trends (last 24 hours)
    df['date_collected'] = pd.to_datetime(df['date_collected'])
    recent_24h = df[df['date_collected'] >= datetime.now() - timedelta(hours=24)]

    print(f"Debug: Total threats: {total_threats}, Critical: {critical_threats}, Average Score: {avg_score:.2f}")
    print(f"Debug: New threats in last 24h: {len(recent_24h)}")

    report = f"""
# EXECUTIVE THREAT INTELLIGENCE SUMMARY
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## KEY FINDINGS
- **Total Active Threats**: {total_threats:,}
- **Critical Threats**: {critical_threats} ({critical_threats/total_threats*100:.1f}%)
- **Average Threat Score**: {avg_score:.1f}/100
- **New Threats (24h)**: {len(recent_24h)}

## THREAT LANDSCAPE OVERVIEW
{generate_threat_landscape_analysis(df)}

## RECOMMENDATIONS
{generate_recommendations(df)}
    """

    filename = f'threat_intelligence_report_{datetime.now().strftime("%Y%m%d")}.md'
    with open(filename, 'w') as f:
        f.write(report)

    print(f"Debug: Report saved to {filename}")

    return report

def generate_threat_landscape_analysis(df):
    """Analyze current threat landscape"""
    print("Debug: Generating threat landscape analysis...")

    # Top threat sources
    top_sources = df['source'].value_counts().head(5)

    # Threat distribution
    level_dist = df['threat_level'].value_counts()

    analysis = f"""
### Threat Source Analysis
- Primary Sources: {', '.join([f"{src} ({count:,})" for src, count in top_sources.items()])}

### Risk Distribution
- Critical: {level_dist.get('CRITICAL', 0)} threats
- High: {level_dist.get('HIGH', 0)} threats
- Medium: {level_dist.get('MEDIUM', 0)} threats
- Low: {level_dist.get('LOW', 0)} threats
- Informational: {level_dist.get('INFORMATIONAL', 0)} threats
    """

    print("Debug: Threat landscape analysis completed.")
    return analysis

def generate_recommendations(df):
    """Generate actionable recommendations"""
    print("Debug: Generating recommendations...")

    critical_count = len(df[df['threat_level'] == 'CRITICAL'])

    recommendations = []

    if critical_count > 100:
        recommendations.append("🚨 **IMMEDIATE ACTION**: Deploy additional monitoring for critical threats")

    if df['threat_score'].mean() > 60:
        recommendations.append("⚠️ **HIGH PRIORITY**: Review and strengthen security controls")

    recommendations.append("📊 **ONGOING**: Continue monitoring threat feeds and update signatures")

    print("Debug: Recommendations generated.")
    return '\n'.join(f"- {rec}" for rec in recommendations)

if __name__ == "__main__":
    report = generate_executive_summary()
    print("\nExecutive threat intelligence report generated successfully!\n")
    print("---------- Report Preview ----------\n")
    print(report)
    print("\n---------- End of Report ----------\n")
