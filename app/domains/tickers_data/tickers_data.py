import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from app.config.settings import Settings
from app.domains.graphs.max_min_plot import max_min_plot
from app.domains.graphs.candle_plot import candle_plot

dolar = 4.97


class TickersData:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol

    def _fetch_history(self, period, interval):
        ticker = yf.Ticker(self.ticker_symbol)
        return ticker.history(period=period, interval=interval)

    def _convert_to_currency(self, dataframe, currency):
        if currency == "BRL":
            dataframe[["Open", "High", "Low", "Close"]] *= dolar

    def get_general_data(self, time, currency):
        period_map = {"Diário": "1d", "Semanal": "5d", "Mensal": "30d"}
        interval_map = {"Diário": "15m", "Semanal": "15m", "Mensal": "15m"}

        period = period_map.get(time)
        interval = interval_map.get(time)

        df_history = self._fetch_history(period, interval)
        self._convert_to_currency(df_history, currency)

        latest_data = df_history.iloc[-1]
        general_data = Settings(
            symbol=self.ticker_symbol,
            open=round(float(latest_data["Open"]), 2),
            higher=round(float(latest_data["High"]), 2),
            lower=round(float(latest_data["Low"]), 2),
            closed=round(float(latest_data["Close"]), 2),
            volume=latest_data["Volume"],
        )

        return general_data, df_history

    def get_download(self, time, currency):
        _, dataframe = self.get_general_data(time, currency)
        dataframe = dataframe.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        return dataframe.sort_values("Datetime", ascending=False)

    def plot_max_min(self, time, currency):
        _, dataframe = self.get_general_data(time, currency)
        dataframe = dataframe.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        return max_min_plot(
            dataframe["Datetime"],
            dataframe["Low"],
            dataframe["High"],
            dataframe["Open"].mean(),
            time,
            self.ticker_symbol,
            currency,
        )

    def plot_candle(self, time, currency):
        _, dataframe = self.get_general_data(time, currency)
        dataframe = dataframe.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        return candle_plot(dataframe, self.ticker_symbol, currency, time)
