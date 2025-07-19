

import pandas as pd
import numpy as np
import ast
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import classification_report
import joblib

#importing data from csv files
steamspy_df = pd.read_csv('steamspy_all_games.csv')
storefront_df_raw = pd.read_csv('storefront_data.csv')

#the json is stringified, so we need to convert it to a real list before we can use it
storefront_df_raw['genres_parsed'] = storefront_df_raw['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
storefront_df = storefront_df_raw.drop(columns=['genres', 'release_date', 'genres_parsed'])

#for debugging
#print("columns in storefront_df:", storefront_df.columns)
#print("columns in steamspy_df:", steamspy_df.columns)

#genres_df = df['genres_list'].str.join('|').str.get_dummies()

storefront_df['genres_list_id'] = storefront_df_raw['genres_parsed'].apply(lambda x: [g['id'] for g in x if 'id' in g] if isinstance(x, list) else [])
genres_df_id = storefront_df['genres_list_id'].str.join('|').str.get_dummies()

#for debugging
#print("Storefront duplicates previous to remove:", storefront_df['appid'].duplicated().sum(), "Length pre-duplicates:", len(storefront_df))
#print("Steamspy duplicates previous to remove:", steamspy_df['appid'].duplicated().sum(), "Length pre-duplicates:", len(steamspy_df))

storefront_df = storefront_df.drop_duplicates(subset='appid')
steamspy_df = steamspy_df.drop_duplicates(subset='appid')

#for debugging
#print("Storefront duplicates after drop:", storefront_df['appid'].duplicated().sum(), "Length post-duplicates:", len(storefront_df))
#print("Steamspy duplicates after drop:", steamspy_df['appid'].duplicated().sum(), "Length post-duplicates:", len(steamspy_df))


df = pd.merge(storefront_df, steamspy_df, left_on='appid', right_on='appid', how='inner')
#for debugging
#print("Merged duplicates after drop:", df['appid'].duplicated().sum(), "Length post-duplicates:", len(df))
#if len(df) > len(storefront_df) and len(df) > len(steamspy_df):
#    print("There are still more rows in the merged dataframe than in the individual dataframes. There may be some mismatched appids in the two dataframes.")
#else:
#    print("The merged dataframe has the same number or fewer rows as the individual dataframes. There are no mismatched appids.")
#df = df.drop(columns='genres_list')

#for debugging
#print("length of df after merge:", len(df))

#Creating a dictionary to map the ids to the EN descriptions so results are interpretable
#ASSUMPTION: English descriptions will be in the front. This method takes the first description for each id to map them together, if there is an error will have to manually change.
all_genres = storefront_df_raw['genres_parsed'].dropna().explode()
genre_dicts = [g for g in all_genres if isinstance(g, dict) and 'id' in g and 'description' in g]
genre_map = {}
for g in genre_dicts:
    genre_map[g['id']] = genre_map.get(g['id'], g['description'])
#for debugging
#print(genre_map.values())
if len(genre_map.keys()) == len(genres_df_id.columns):
    print("No Flags")
else:
    print("ERROR")


df['genres_list'] = df['genres_list_id'].apply(
    lambda id_list: [genre_map.get(i, f"Unknown-{i}") for i in id_list]
)

#for debugging
#print("length of df before dropping na",len(df))

df = df.drop(columns=['genres_list_id', 'score_rank'])
df = df.dropna()

#for debugging
#print("length of df after dropping na",len(df))
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(df['genres_list'])


genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_, index=df.index)
df_encoded = pd.concat([df, genres_df], axis=1)

#for debugging
#print(df_encoded.columns)

df_indie = df_encoded[(df_encoded['Indie'] == 1) & (df_encoded['type'] == 'game')].copy()

df_indie.loc[:, 'owners_lower'] = df_indie['owners'].str.split(" ..").str[0].str.replace(',','').astype(int)

df_indie.loc[:, "same_dev_pub"] = (
    df_indie['developer'].str.strip() ==
    df_indie['publisher'].str.strip()
).astype(int)

df_final = df_indie.drop(columns=['genres_list', 'price', 'initialprice', 'discount', 'owners','publisher', 'developer', 'type','name', 'appid', 'Indie'])

expected_columns = ['Action', 'Casual', 'Adventure', 'Simulation', 'Strategy', 'RPG',
                    'Early Access', 'Free To Play', 'Sports', 'Racing', 'Massively Multiplayer',
                    'Violent', 'Gore','positive', 'negative','average_forever','median_forever',
                    'ccu', 'same_dev_pub']

#for debugging
#missing = [col for col in expected_columns if col not in df_final.columns]
#print("Missing columns:", missing)

df_final['owners_binned'] = pd.cut(df_final['owners_lower'], bins=[-1, 100000, 500000, 1000000, 5000000, 10000000, np.inf], labels=[1, 2, 3, 4, 5, 6]).astype(int)

X = df_final[['Action', 'Casual', 'Adventure', 'Simulation', 'Strategy', 'RPG', 'Early Access', 'Free To Play', 'Sports', 'Racing', 'Massively Multiplayer',
              'Violent', 'Gore','positive', 'negative','average_forever','median_forever','ccu', 'same_dev_pub']]
y = df_final['owners_binned'] 


pipe_binned = Pipeline([
    ('powertransformer', PowerTransformer(method='yeo-johnson', standardize=True)),
    ('classifier', RandomForestClassifier(random_state=7, n_estimators=200, max_depth=10, min_samples_split=10))
])
pipe_binned.fit(X, y)

bin_map = {
    1: '0-100,000',
    2: '100,001-500,000',
    3: '500,001-1,000,000',
    4: '1,000,001-5,000,000',
    5: '5,000,001-10,000,000',
    6: '10,000,001+'
    }

joblib.dump(pipe_binned, 'rf_model.pkl')

y_pred = pipe_binned.predict(X)
print(classification_report(y, y_pred))

print("success")