import requests
from google.cloud import bigquery
from datetime import datetime
from time import sleep
import os

#--------
# INITIALIZING BQ AND TABLES
#-------- 

bq = bigquery.Client()
project_id = 'steaminsights-466700'
dataset_id = 'steam_data'
#Pulling into clean games which includes all of the games pulled from steamspy.
main_table = 'clean_games'
staging_table = 'new_appids_staging'
table_id = f"{project_id}.{dataset_id}.{main_table}"
staging_table_id = f"{project_id}.{dataset_id}.{staging_table}"
temp_table_id = f"{project_id}.{dataset_id}.temp_table"

#--------
# MODE SELECTION (backfill = updating previously pulled data, staging = updating new data from staging table)
#--------
MODE = os.getenv("MODE",'staging')
 

def main():
    if MODE == 'backfill':
        appids = fetch_appids_from_bq()
    elif MODE == 'staging':
        appids = fetch_appids_from_staging()

        if not appids:
            print("No new appids found in staging table. Exiting.")
            return
    else:
        raise ValueError("Invalid mode. Use 'backfill' or 'staging'.")
    
    rows = []
    
    for idx, appid in enumerate(appids, start=1):
        data = fetch_steamspy_data(appid)
        if not data or 'appid' not in data:
            print(f"Skipping appid {appid} due to missing data.")
            continue

        rows.append({
            "appid": appid,
            "genres": normalize_genres(data.get("genre", "")),
            "tags": normalize_tags(data.get("tags", {})),
            "last_updated": datetime.utcnow().isoformat(),
        })
        sleep(1.1)  # Rate limiting to avoid hitting SteamSpy's rate limit

        if idx % 50 == 0:
            print(f"Progress: {idx}/{len(appids)} appids processed.")

    load_rows_to_temp(rows)
    merge_into_main()
    if MODE == 'staging':
        delete_staging_rows(staging_table_id)
    
    print("Processing complete.")

#--------
# COLLECTING APPIDS FROM BQ
#--------

def fetch_appids_from_bq() -> list[int]:
    """Currently this fetches all of the appids from the clean_games table. I need this to run once then only pull from the staging table."""
    query = f"""
    SELECT DISTINCT appid
    FROM `{table_id}`
    WHERE appid IS NOT NULL
    """
    results = bq.query(query).result()
    appids = [row['appid'] for row in results]
    print(f"found {len(appids)} appids in the main table.")
    return appids

def fetch_appids_from_staging() -> list[int]:
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

#--------
# CLEANING STAGING TABLE
#--------

def delete_staging_rows(table: str):
    #Clears the Staging table to allow for a new batch of data to be loaded.
    query = f"""
    DELETE FROM `{table}`
    WHERE TRUE
    """
    results = bq.query(query).result()
    print(f"Deleted {results.total_rows} rows from staging table.")

#--------
# PROCESSING API PULLS
#--------

def fetch_steamspy_data(appid: int):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching data for appid {appid}: {e}")
        return None
    
#--------
# NORMALIZING DATA
#--------

def normalize_genres(genre_string: str):
    if not genre_string:
        return []
    return [g.strip() for g in genre_string.split(',')]

def normalize_tags(tag_dict: dict):
    if not tag_dict:
        return []
    return [{"tag": k, "weight": int(v)} for k, v in tag_dict.items()]

#--------
# INSERTING OR UPDATING DATA
#--------

def load_rows_to_temp(rows: list[dict]):
    if not rows:
        print("No rows to load.")
        return
    job = bq.load_table_from_json(rows, temp_table_id, job_config=bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE'))
    job.result()
    print(f"Loaded {len(rows)} rows into temp table.")

def merge_into_main():
    merge_sql = f"""
    MERGE `{table_id}` t
    USING `{temp_table_id}` s
    ON t.appid = s.appid
    WHEN MATCHED THEN
        UPDATE SET
            t.genres = s.genres,
            t.tags = s.tags,
            t.last_updated = s.last_updated
    """
    bq.query(merge_sql).result()
    print("Merged data into main table.")

def upsert_game_details(row: dict):
    if MODE == 'staging':
        errors = bq.insert_rows_json(table_id, [row])
        if errors:
            print(f"inserting row: {row['appid']}")
        else:
            print(f"inserted row: {row['appid']}")
    elif MODE == 'backfill':
        client = bigquery.Client(project=project_id)
        job_config = bigquery.LoadJobConfig(write_disposition='WRITE_APPEND')
        job = client.load_table_from_json([row], temp_table_id, job_config=job_config)
        job.result()
        query = f"""
        MERGE INTO `{table_id}` t
        USING `{temp_table_id}` s
        ON t.appid = s.appid
        WHEN MATCHED THEN
            UPDATE SET
                t.genres = s.genres,
                t.tags = s.tags,
                t.last_updated = s.last_updated
        """
        client.query(query).result()


if __name__ == "__main__":
    main()