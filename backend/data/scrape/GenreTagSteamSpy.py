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

def upsert_game_details(appid: int):
    print(f"Fetching data for appid: {appid}")
    data = fetch_steamspy_data(appid)