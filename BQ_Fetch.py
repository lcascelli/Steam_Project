from google.cloud import bigquery
import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = #enter key here

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
