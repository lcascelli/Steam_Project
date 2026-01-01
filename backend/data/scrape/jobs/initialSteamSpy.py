import requests
import time
import pandas as pd
from google.cloud import bigquery

project_id = 'steaminsights-466700'
dataset_id = 'steam_data'
#Pulling into clean games which includes all of the games pulled from steamspy.
main_table = 'clean_games'
temp_table = 'new_appids_staging'


#TOTAL TIME FOR THIS SCRIPT IS 2667m 30.3s


#This script scrapes data from the SteamSpy API and the Steam Storefront API.
#will take 85 minutes to run. 
#iterating through the API to get all games

def main():
    print("Starting SteamSpy data pull")
    bq= bigquery.Client()
    #Pull data from SteamSpy API
    raw_df = steamspy_pull()
    #Normalize and clean data
    clean_df = normalize_steamspy(raw_df)
    #Load existing appids from BigQuery
    existing_appids= load_existing_appids(bq)
    #Upsert data to BigQuery
    upsert_to_bigquery(clean_df, bq)
    #Write new appids to staging table for next pull to get the genres
    write_new_appids(clean_df, existing_appids, bq)


def steamspy_pull():
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
        if len(df) <800:
            break
        page += 1
        time.sleep(60)

    steamspy_df = pd.concat(all_data, ignore_index=True)
    steamspy_df = steamspy_df.drop_duplicates(subset=['appid'])
    print("total games in SteamSpy:", len(steamspy_df))
    return steamspy_df

def normalize_steamspy(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize columns for BigQuery"""
    expected_columns = ["appid", "name", "developer", "publisher", "score_rank",
                        "positive", "negative", "userscore", "average_forever", 
                        "average_2weeks", "ccu", "owners", "median_forever",
                        "median_2weeks", "price", "initialprice", "discount"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    numeric_cols = ["positive", "negative", "userscore", "average_forever",
                    "average_2weeks", "ccu", "median_forever",
                    "median_2weeks", "price", "initialprice"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    #SPLITTING OWNERS INTO LOWER AND UPPER BOUNDS. SHOWS UP AS A RANGE I.E. "10000...20000" 
    df["owners_lower"] = df["owners"].str.split("...").str[0].astype(float)
    df["owners_upper"] = df["owners"].str.split("...").str[1].astype(float)

    normalized = df[expected_columns + ["owners_lower", "owners_upper"]]
    return normalized

"""BIGQUERY UPSERT LOGIC"""

def load_existing_appids(bq):
    query = f"""
    SELECT appid 
    FROM `{project_id}.{dataset_id}.{main_table}`
    """
    existing = bq.query(query).to_dataframe()
    return set(existing['appid'].astype(int))

def upsert_to_bigquery(df, bq):
    temp_table = f"{project_id}.{dataset_id}._steamspy_temp"

    load_job = bq.load_table_from_dataframe(
        df,
        temp_table,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    load_job.result()

    print("Loaded temp SteamSpy table.")

    merge_query = f"""
    MERGE `{project_id}.{dataset_id}.{main_table}` T
    USING `{temp_table}` S
    ON T.appid = S.appid
    WHEN MATCHED THEN UPDATE SET
        T.name = S.name,
        T.developer = S.developer,
        T.publisher = S.publisher,
        T.score_rank = S.score_rank,
        T.positive = S.positive,
        T.negative = S.negative,
        T.userscore = S.userscore,
        T.average_forever = S.average_forever,
        T.average_2weeks = S.average_2weeks,
        T.ccu = S.ccu,
        T.owners = S.owners,
        T.median_forever = S.median_forever,
        T.median_2weeks = S.median_2weeks,
        T.price = S.price,
        T.initialprice = S.initialprice,
        T.discount = S.discount,
        T.owners_lower = S.owners_lower,
        T.owners_upper = S.owners_upper
        WHEN NOT MATCHED THEN
        INSERT ROW;
        """
    
    bq.query(merge_query).resul()
    print("Merge completed. Data in main table is up to date.")

    bq.delete_table(temp_table, not_found_ok=True)


"""STAGING NEW APPIDS FOR SECOND QUERY TO FIND THEIR GENRES"""

def write_new_appids(df, existing_appids, bq):
    new_df = df[~df["appid"].isin(existing_appids)][["appid"]]

    if new_df.empty:
        print("No new appids to process.")
        return
    staging_table = f"{project_id}.{dataset_id}.{temp_table}"

    bq.load_table_from_dataframe(
        new_df,
        staging_table,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    ).result()

    print(f"Wrote {len(new_df)} new appids to staging table.")


if __name__ == "__main__":
    main()
