from google.cloud import bigquery
import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Liam\Documents\_Python\steam-BQ-key\steaminsights-466700-b053db8508f6.json"

client = bigquery.Client(project='steaminsights-466700')

avg_by_genre_query = """
  SELECT 
  `genre`,
  avg(CAST(`average_forever` AS FLOAT64)) as avg_forever,
  avg(CAST(`average_2weeks` AS FLOAT64)) as avg_2week,
  avg(CAST(`positive` AS FLOAT64)) as avg_positive,
  avg(CAST(`negative` AS FLOAT64)) as avg_negative,
  count(`appid`) as genre_count

  FROM(
    SELECT
      `genre`,
      `positive`,
      `negative`,
      `average_forever`,
      `average_2weeks`,
      `appid`
    FROM `steaminsights-466700.steam_data.indie_games`
    UNPIVOT(
      has_genre FOR genre IN(
            `Action` as 'action',
            `Adventure` as 'adventure',
            `RPG` as 'rpg',
            `Massively Multiplayer` as 'mmo',
            `Violent` as 'violent',
            `Gore` as 'gore',
            `Strategy` as 'strat',
            `Racing` as 'racing',
            `Simulation` as 'simulation',
            `Casual` as 'casual',
            `Early Access` as 'early',
            `Free To Play` as 'free',
            `Sports` as 'sport'          
      )
    )
    WHERE has_genre = 1
  )
  GROUP BY genre;
  """
avg_by_genre_df = client.query(avg_by_genre_query).to_dataframe()
os.makedirs("steam-insights/src/data", exist_ok=True)
avg_by_genre_df.to_json("steam-insights/src/data/avg_by_genre.json", index=False, orient='records')
print("Average by genre data fetched and saved.")

#Creating a condensed version of the indie games DataFrame for TopGamesChart.js. Stored here for now, before automatic pulls.
#df_indie = pd.read_json('steam-insights/src/data/df_indie.json', orient='records', lines=True)
#df_indie_simple = df_indie[['appid', 'name', 'genres_list', 'average_forever', 'average_2weeks', 
#                            'positive', 'negative', 'owners_lower']].copy()

df_indie_simple_query = """
SELECT
  `appid`,
  `name`,
  `genres_list`,
  `average_forever`,
  `average_2weeks`,
  `positive`,
  `negative`,
  `owners`,
  `owners_lower`,
  `publisher`,
  `developer`
FROM `steaminsights-466700.steam_data.indie_games`
WHERE EXISTS (
  SELECT 1
  FROM UNNEST(`genres_list`) AS genre
  WHERE genre IN ('Action', 'Adventure', 'RPG', 'Massively Multiplayer', 'Violent', 'Gore', 
                  'Strategy', 'Racing', 'Simulation', 'Casual', 'Early Access', 
                  'Free To Play', 'Sports')
);
"""
df_indie_simple = client.query(df_indie_simple_query).to_dataframe()
df_indie_simple.to_json('steam-insights/src/data/df_indie_simple.json', index=False, orient='records')
print("Condensed indie games data fetched and saved.")