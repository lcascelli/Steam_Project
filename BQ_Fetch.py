from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()
query = """
SELECT
  sum(`Action`) as sum_action,
  sum(`Adventure`) as sum_adventure,
  sum(`RPG`) as sum_rpg,
  sum(`Massively Multiplayer`) as sum_mmo,
  sum(`Violent`) as sum_violent,
  sum(`Gore`) as sum_gore,
  sum(`Strategy`) as sum_strat,
  sum(`Racing`) as sum_racing,
  sum(`Simulation`) as sum_sim,
  sum(`Casual`) as sum_casual,
  sum(`Early Access`) as sum_early,
  sum(`Free To Play`) as sum_free,
  sum(`Sports`) as sum_sport


  FROM
  `steaminsights-466700.steam_data.clean_games` 
  """
df = client.query(query).to_dataframe()
df.to_json('steam-insights\src\data\genres_agg.json', index=False, orient='records', lines=True)