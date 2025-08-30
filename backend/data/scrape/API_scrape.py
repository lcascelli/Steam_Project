import requests
import time
import pandas as pd


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
print("total games:", len(steamspy_df))
# Save the DataFrame to a CSV file
steamspy_df.to_csv('steamspy_all_games.csv', index=False)


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
storefront_df.to_csv('storefront_data.csv', index=False)