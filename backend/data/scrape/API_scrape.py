import requests
import time
import pandas as pd
import google.cloud as bigquery

project_id = 'steaminsights-466700'
dataset_id = 'steam_data'
main_table = 'indie_games'
staging_table = 'indie_games_staging'


#TOTAL TIME FOR THIS SCRIPT IS 2667m 30.3s


#This script scrapes data from the SteamSpy API and the Steam Storefront API.
#will take 85 minutes to run. 
#iterating through the API to get all games
all_data = []
page = 0
headers = {
    'User-Agent': 'Mozilla/5.0'}
while True:
    response = requests.get(f"https://steamspy.com/api.php?request=all&page={page}", headers=headers)
    data = response.json()
    if not data:
        break
    all_data.append(pd.DataFrame.from_dict(data, orient='index'))
    df = pd.DataFrame.from_dict(data, orient='index')
    print(f"Page {page} returned {len(df)} games")
    if len(df) <1000:
        break
    page += 1
    time.sleep(60)

steamspy_df = pd.concat(all_data, ignore_index=True)
steamspy_df = steamspy_df.drop_duplicates(subset=['appid'])
print("total games in SteamSpy:", len(steamspy_df))


#TAKES 2582m 30.3s TO RUN. ONLY RUN WHEN NECESSARY!
#pull game IDs to iterate over
appids = steamspy_df['appid'].tolist()
storefront_data = []
#iterate over appids and request data from storefront API
for id in appids:
    url = "https://store.steampowered.com/api/appdetails?appids=" + str(id)
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        data = r.json()
        if data[str(id)]['success'] == True:
            game_data = data[str(id)]['data']
            storefront_data.append({
                'appid': id,
                'genres': game_data.get('genres'),
                'type': game_data.get('type'),
                'release_date': game_data.get('release_date')
            })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for appid {id}: {e}")
    #Rate limit of 100,000 requests per day, 200 requests per 5 minutes
    time.sleep(1.6)  # Sleep to avoid hitting rate limits

storefront_df = pd.DataFrame(storefront_data)
#storefront_df.to_csv('storefront_data.csv', index=False)

merged_df = steamspy_df.merge(storefront_df, on='appid', how='left')

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

table_id = f"{project_id}.{dataset_id}.{staging_table}"
load_job = client.load_table_from_dataframe(
    merged_df,
    table_id,
    job_config=job_config
)

load_job.result()  # Waits for the job to complete.
print(f"Loaded {load_job.output_rows} rows into {table_id}... Uploaded to staging table.")

merge_query = f"""
MERGE `{project_id}.{dataset_id}.{main_table}` T
USING `{project_id}.{dataset_id}.{staging_table}` S
ON T.appid = S.appid

WHEN MATCHED THEN
  UPDATE SET
    T.name = S.name,
    T.score_rank = S.score_rank,
    T.positive = S.positive,
    T.negative = S.negative,
    T.average_forever = S.average_forever,
    T.average_2weeks = S.average_2weeks,
    T.ccu = S.ccu,
    T.owners = S.owners,
    T.players_forever = S.players_forever,
    T.players_2weeks = S.players_2weeks,
    T.genres = S.genres,
    T.type = S.type
WHEN NOT MATCHED THEN
    INSERT *
    """

merge_job = client.query(merge_query)
merge_job.result()

print("Merge completed. Data in main table is up to date.")