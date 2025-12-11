import requests
import time
import pandas as pd

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