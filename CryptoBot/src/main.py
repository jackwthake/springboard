import binance as binance

if __name__ == '__main__':
  api_keys = binance.setup('../secret/secret.json')

  df = binance.download_data('ETHUSDT', 1000)
  df = binance.format_dataframe(df)

  print(df.head(20))
  print(api_keys)
  print(binance.get_live_price('ETHUSDT'))