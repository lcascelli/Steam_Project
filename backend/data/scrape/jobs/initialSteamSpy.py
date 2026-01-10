import requests
import time
import pandas as pd
from google.cloud import bigquery


"""
UPDATES DOCKER IMAGE and UPDATES THE CLOUD RUN JOB:
cd .\backend\data\scrape\
docker build -t steamspy-job .
docker tag steamspy-job:latest us-docker.pkg.dev/steaminsights-466700/steamspy/steamspy-job:latest
docker push us-docker.pkg.dev/steaminsights-466700/steamspy/steamspy-job:latest


gcloud run jobs update steamspy-job `
  --image us-docker.pkg.dev/steaminsights-466700/steamspy/steamspy-job:latest `
  --region us-west1

"""

project_id = 'steaminsights-466700'
dataset_id = 'steam_data'
#Pulling into clean games which includes all of the games pulled from steamspy.
main_table = 'raw_data'
temp_table = 'new_appids_staging'


#TOTAL TIME FOR THIS SCRIPT IS 2667m 30.3s


#This script scrapes data from the SteamSpy API and the Steam Storefront API.
#will take 85 minutes to run. 
#iterating through the API to get all games

def main():
    print("Starting SteamSpy data pull", flush=True)
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
        if page >0:
            print("Sleeping for 65 seconds to avoid rate limiting...", flush=True)
            time.sleep(65)
        print(f"Fetching page {page} from SteamSpy API...", flush=True)
        response = requests.get(f"https://steamspy.com/api.php?request=all&page={page}", headers=headers, timeout=60)

        if response.status_code != 200:
            print(f"Error fetching data from SteamSpy API: {response.status_code} on page {page}", flush=True)
            break

        if not response.text.strip():
            print(f"No data returned from SteamSpy API on page {page}", flush=True)
            break

        try:
            data = response.json()

        except ValueError as e:
            print(f"Error parsing JSON from SteamSpy API on page {page}: {e}", flush=True)
            break

        if not data:
            print("No data returned, stopping", flush=True)
            break
        df = pd.DataFrame.from_dict(data, orient='index')
        print(f"Page {page} returned {len(df)} games", flush=True)

        all_data.append(df)

        if len(df) <900:
            print("Last page reached, stopping", flush=True)
            break
        page += 1

    steamspy_df = pd.concat(all_data, ignore_index=True)
    steamspy_df = steamspy_df.drop_duplicates(subset=['appid'])
    print("total games in SteamSpy:", len(steamspy_df), flush=True)
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
    
    string_cols = ["name", "developer", "publisher", "score_rank","owners","discount"]
    for col in string_cols:
        df[col] = df[col].astype(str).replace({"nan": None})

    #SPLITTING OWNERS INTO LOWER AND UPPER BOUNDS. SHOWS UP AS A RANGE I.E. "10000...20000" 
    df["owners"] = (
        df["owners"]
        .astype(str)
        .str.strip()
        .replace({"":None, "nan":None})
    )
    owners_split = df["owners"].str.split(" .. ", expand=True)  # Split the range into two parts
    df["owners_lower"] = (owners_split[0]
                          .str.replace(",","",regex=False)
                          .astype("Int64"))  # Convert lower bound to int

    normalized = df[expected_columns + ["owners_lower"]]
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

    print("Loaded temp SteamSpy table.", flush=True)

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
        T.owners_lower = S.owners_lower
        WHEN NOT MATCHED THEN
        INSERT (
        appid, name, developer, publisher, score_rank, positive, negative, userscore,
        average_forever, average_2weeks, ccu, owners, median_forever, median_2weeks,
        price, initialprice, discount, owners_lower)
        VALUES (
        S.appid, S.name, S.developer, S.publisher, S.score_rank, S.positive, S.negative, S.userscore,
        S.average_forever, S.average_2weeks, S.ccu, S.owners, S.median_forever, S.median_2weeks,
        S.price, S.initialprice, S.discount, S.owners_lower);
        """
    
    bq.query(merge_query).result()
    print("Merge completed. Data in main table is up to date.", flush=True)

    bq.delete_table(temp_table, not_found_ok=True)


"""STAGING NEW APPIDS FOR SECOND QUERY TO FIND THEIR GENRES"""

def write_new_appids(df, existing_appids, bq):
    new_df = df[~df["appid"].isin(existing_appids)][["appid"]]

    if new_df.empty:
        print("No new appids to process.", flush=True)
        return
    staging_table = f"{project_id}.{dataset_id}.{temp_table}"

    bq.load_table_from_dataframe(
        new_df,
        staging_table,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    ).result()

    print(f"Wrote {len(new_df)} new appids to staging table.", flush=True)


if __name__ == "__main__":
    main()
