import requests
import pandas as pd
from datetime import datetime
import time
from io import BytesIO
import zipfile

OPENPHISH_URL = "https://openphish.com/feed.txt"
URLHAUS_ZIP_URL = "https://urlhaus.abuse.ch/downloads/csv/"

def collect_openphish():
    print("Debug: Starting collect_openphish()")
    try:
        response = requests.get(OPENPHISH_URL)
        response.raise_for_status()
        urls = response.text.strip().splitlines()
        df = pd.DataFrame(urls, columns=['url'])
        df['source'] = 'openphish'
        print(f"OpenPhish: Retrieved {len(df)} URLs")
        return df
    except Exception as e:
        print(f"Error fetching OpenPhish data: {e}")
        return pd.DataFrame(columns=['url', 'source'])

def collect_urlhaus():
    print("Debug: Starting collect_urlhaus()")
    try:
        response = requests.get(URLHAUS_ZIP_URL)
        response.raise_for_status()
        zip_file_bytes = BytesIO(response.content)
        with zipfile.ZipFile(zip_file_bytes) as z:
            csv_filenames = z.namelist()
            print(f"URLHaus ZIP contains files: {csv_filenames}")
            with z.open(csv_filenames[0]) as csvfile:
                col_names = ['id', 'dateadded', 'url', 'status', 'modified',
                             'threat', 'tags', 'urlhaus_link', 'reporter']
                df = pd.read_csv(csvfile, comment='#', header=None, names=col_names)
        print(f"URLHaus columns: {list(df.columns)}")
        urls_df = df[['url']].copy()
        urls_df['source'] = 'urlhaus'
        print(f"URLHaus: Extracted {len(urls_df)} URLs")
        return urls_df
    except Exception as e:
        print(f"Error fetching URLHaus data: {e}")
        return pd.DataFrame(columns=['url', 'source'])

def combine_feeds(df1, df2):
    print("Debug: Combining feeds")
    combined = pd.concat([df1, df2], ignore_index=True)
    before = len(combined)
    combined.drop_duplicates(subset=['url'], inplace=True)
    after = len(combined)
    print(f"Combined feeds: {before} URLs before deduplication, {after} after deduplication")
    combined['date_collected'] = datetime.utcnow().isoformat()
    return combined

def collect_all():
    print("Debug: Starting collect_all()")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    openphish_df = collect_openphish()
    urlhaus_df = collect_urlhaus()
    all_threats = combine_feeds(openphish_df, urlhaus_df)
    filename = f"realtime_threats_{timestamp}.csv"
    all_threats.to_csv(filename, index=False)
    print(f"Saved combined threats to {filename}")
    all_threats.to_csv('combined_threats.csv', index=False)
    print("Saved combined threats to combined_threats.csv")
    return all_threats

def run_automated_collection():
    while True:
        print(f"\nStarting threat collection at {datetime.utcnow().isoformat()} UTC")
        threats = collect_all()
        print(f"Collected a total of {len(threats)} unique threat URLs")
        print("Sleeping for 1 hour...\n")
        time.sleep(3600)

if __name__ == "__main__":
    print("Debug: Entered main execution block")
    collect_all()
