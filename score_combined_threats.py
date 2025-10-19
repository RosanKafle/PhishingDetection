import pandas as pd
from threat_scoring import calculate_threat_score, classify_threat_level

def main():
    """Load combined threats and add threat scores"""
    try:
        print("Debug: Starting main()")
        df = pd.read_csv('combined_threats.csv')
        print(f"Loaded {len(df)} URLs from combined_threats.csv")
        
        # Add threat score for each URL
        df['threat_score'] = df['url'].apply(calculate_threat_score)
        df['threat_level'] = df['threat_score'].apply(classify_threat_level)
        
        # Save enhanced dataset
        df.to_csv('combined_threats_scored.csv', index=False)
        print(f"Processed {len(df)} URLs with threat scores.")
        print("Saved updated dataset as combined_threats_scored.csv")
        
        # Show sample results
        print("\nSample scored threats:")
        print(df[['url', 'source', 'threat_score', 'threat_level']].head())

    except FileNotFoundError:
        print("Error: combined_threats.csv not found. Please run automated_threat_collector.py first.")
    except Exception as e:
        print(f"Error processing threats: {e}")

if __name__ == "__main__":
    print("Debug: Entered main execution block")
    main()
