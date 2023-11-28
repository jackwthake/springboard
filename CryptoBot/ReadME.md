# Ethereuem Trading Bot
The goal of this project is to create a self sufficicent configurable cryptocurrency trading bot connected to the Binance US exchange.

Major Modules for this project:
- Interfacing with the exchange
  - Getting live price data
  - Placing orders
    - Handling any possible exceptions
  - viewing current orders (filled or not)
  - How often to poll data?
- Algo Module
  - When should we trade?
    - Are we already in a trade?
    - Integrate with Machine learning
      - What indicators are important? (EDA Phase)
    - How many trades should we have open at once?
