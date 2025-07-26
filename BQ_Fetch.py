from google.cloud import bigquery
import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = [#set your path to the service account key file here
    ]

client = bigquery.Client(project='steaminsights-466700')
count_by_genre_query = """
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
  `steaminsights-466700.steam_data.indie_games` 
  """
count_by_genre_query_df = client.query(count_by_genre_query).to_dataframe()
count_by_genre_query_df.to_json('steam-insights/src/data/genres_agg.json', index=False, orient='records', lines=True)

avg_by_genre_query = """
  SELECT 
  `genre`,
  avg(CAST(`average_forever` AS FLOAT64)) as avg_forever,
  avg(CAST(`average_2weeks` AS FLOAT64)) as avg_2week,
  avg(CAST(`positive` AS FLOAT64)) as avg_positive,
  avg(CAST(`negative` AS FLOAT64)) as avg_negative

  FROM(
    SELECT
      `genre`,
      `positive`,
      `negative`,
      `average_forever`,
      `average_2weeks`
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
            `Simulation` as 'sim',
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
avg_by_genre_df.to_json('steam-insights/src/data/avg_by_genre.json', index=False, orient='records', lines=True)
