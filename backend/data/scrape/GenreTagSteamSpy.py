import requests
from google.cloud import bigquery
from datetime import datetime
from time import sleep

bq = bigquery.Client()
project_id = 'steaminsights-466700'
dataset_id = 'steam_data'
#Pulling into clean games which includes all of the games pulled from steamspy.
main_table = 'clean_games'
staging_table = 'new_appids_staging'
table_id = f"{project_id}.{dataset_id}.{main_table}"
staging_table_id = f"{project_id}.{dataset_id}.{staging_table}"

#mode introduced to allow for backfilling of data.
mode = 'backfill' #or 'staging'


def main():
    if mode == 'backfill':
        appids = fetch_appids_from_bq()
    elif mode == 'staging':
        appids = fetch_appids_from_staging()

        if not appids:
            print("No new appids found in staging table. Exiting.")
            return
    else:
        raise ValueError("Invalid mode. Use 'backfill' or 'staging'.")
    
    for idx, appid in enumerate(appids, start=1):
        process_appid(appid)
        sleep(1.1)  # Rate limiting to avoid hitting SteamSpy's rate limit

        if idx % 50 == 0:
            print(f"Progress: {idx}/{len(appids)} appids processed.")
    if mode == 'staging':
        delete_staging_rows()
    
    print("Processing complete.")



def fetch_appids_from_bq():
    """Currently this fetches all of the appids from the clean_games table. I need this to run once then only pull from the staging table."""
    query = f"""
    SELECT DISTINCT 'appid'
    FROM `{table_id}`
    WHERE 'appid' IS NOT NULL
    """
    results = bq.query(query).result()
    appids = [row['appid'] for row in results]
    print(f"found {len(appids)} appids in the main table.")
    return appids

def fetch_appids_from_staging():
    #Fetches all of the appids from the staging table to be used in the main table.
    query = f"""
    SELECT DISTINCT 'appid'
    FROM `{staging_table_id}`
    WHERE 'appid' IS NOT NULL
    """
    results = bq.query(query).result()
    appids = [row['appid'] for row in results]
    print(f"found {len(appids)} appids in the staging table.")
    return appids

def delete_staging_rows():
    #Clears the Staging table to allow for a new batch of data to be loaded.
    query = f"""
    DELETE FROM `{staging_table_id}`
    WHERE TRUE
    """
    results = bq.query(query).result()
    print(f"Deleted {results.total_rows} rows from staging table.")

def fetch_steamspy_data(appid: int):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching data for appid {appid}: {e}")
        return None

def normalize_genres(genre_string: str):
    if not genre_string:
        return []
    return [g.strip() for g in genre_string.split(',')]

def normalize_tags(tag_dict: dict):
    if not tag_dict:
        return []
    return [{"tag": k, "weight": int(v)} for k, v in tag_dict.items()]

def upsert_game_details(row: dict):
    errors = bq.insert_rows_json(main_table, [row])
    if errors:
        print(f"inserting row: {row['appid']}")
    else:
        print(f"inserted row: {row['appid']}")

def process_appid(appid: int):
    print(f"/n---Processing appid: {appid}--\n")
    data = fetch_steamspy_data(appid)
    if not data or 'appid' not in data:
        print(f"Skipping appid {appid} due to missing data.")
        return
    
    row = {
        "appid": appid,
        "genres": normalize_genres(data.get("genre", "")),
        "tags": normalize_tags(data.get("tags", {})),
        "last_updated": datetime.utcnow().isoformat(),
    }

    upsert_game_details(row)


if __name__ == "__main__":
    main()