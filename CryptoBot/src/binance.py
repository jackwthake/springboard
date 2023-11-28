from attr import dataclass
import pandas as pd
from ta import add_all_ta_features
import requests
import json

from datetime import datetime

# constants
binance_uri = 'https://api.binance.us/api/v3/'
time_interval = '1m'

# stores the necessary api-keys
@dataclass
class Keys:
  public_key: str
  secret_key: str

# grabs keys and populates a dataclass for future use
def setup(key_path: str) -> Keys:
  return Keys(**json.load(open(key_path, 'r')))


# download candlestick data
def download_data(symbol: str, limit: int) -> pd.DataFrame:
  try: # try to download, catch any errors
    res = requests.get(binance_uri + 'klines?symbol=' + symbol + '&interval=' + time_interval + '&limit=' + str(limit))
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)
  
  return pd.read_json(res.text) # return imported data


# format candlestick data
def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  df.reset_index(drop=False, inplace=True)

  # first add column headers
  df = df.iloc[:, 1:]
  df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_trades', 'base', 'quote', 'unused']

  # we don't need the closetime since we know when the candle started and how long it should be
  df = df.iloc[:, :-3]
  df.drop(columns='close_time', inplace=True)

  # https://stackoverflow.com/questions/31548132/python-datetime-fromtimestamp-yielding-valueerror-year-out-of-range
  df['open_time'] = [datetime.fromtimestamp(x / 1000) for x in df['open_time']]

  # index based on open_time
  df.set_index('open_time', inplace=True)

  # add trade indicators
  df = add_all_ta_features(df, open='open', close='close', high='high', low='low', volume='quote_asset_volume')

  return df

# get live price
def get_live_price(symbol: str) -> float:
  try: # try to download, catch any errors
    res = requests.get(binance_uri + 'ticker/price?symbol=' + symbol)
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)
  
  return json.loads(res.text)['price']