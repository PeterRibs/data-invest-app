import yfinance as yf
from decimal import Decimal
from app.config.settings import Settings
from app.domains.graphs.max_min_plot import max_min_plot
from app.domains.graphs.candle_plot import candle_plot

dolar = 4.97


class TickersData:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol

    def _fetch_history(self, period, interval):
        ticker = yf.Ticker(self.ticker_symbol)
        print(ticker.earnings_dates)
        print(ticker.news)
        return ticker.history(period=period, interval=interval)

    def _convert_to_currency(self, dataframe, currency):
        if currency == "BRL":
            dataframe[["Open", "High", "Low", "Close"]] *= dolar

    def get_general_data(self, time, currency):
        period_map = {"Diário": "1d", "Semanal": "5d", "Mensal": "30d"}
        interval_map = {"Diário": "15m", "Semanal": "60m", "Mensal": "90m"}

        period = period_map.get(time)
        interval = interval_map.get(time)

        df_history = self._fetch_history(period, interval)
        self._convert_to_currency(df_history, currency)

        latest_data = df_history.iloc[-1]
        general_data = Settings(
            symbol=self.ticker_symbol,
            open=round(Decimal(latest_data["Open"]), 2),
            higher=round(Decimal(latest_data["High"]), 2),
            lower=round(Decimal(latest_data["Low"]), 2),
            closed=round(Decimal(latest_data["Close"]), 2),
            volume=latest_data["Volume"],
        )

        return general_data, df_history

    def get_download(self, time, currency):
        _, dataframe = self.get_general_data(time, currency)
        dataframe = dataframe.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        self._convert_to_currency(dataframe, currency)
        return dataframe.sort_values("Datetime", ascending=False)

    def plot_max_min(self, time, currency):
        _, dataframe = self.get_general_data(time, currency)
        dataframe = dataframe.reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        self._convert_to_currency(dataframe, currency)
        return max_min_plot(
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
        self._convert_to_currency(dataframe, currency)
        return candle_plot(dataframe, self.ticker_symbol, currency)


import yfinance as yf
from decimal import Decimal

from app.config.settings import Settings
from app.domains.graphs.max_min_plot import max_min_plot
from app.domains.graphs.candle_plot import candle_plot

dolar = 4.97


class TickersData:
    def __init__(self, ticker_symbol):
        self.ticker_symbol: str = ticker_symbol

    def get_general_data(self, time, currency):
        ticker = yf.Ticker(self.ticker_symbol)

        if time == "Diário":
            df_history = ticker.history(period="1d", interval="15m")
        elif time == "Semanal":
            df_history = ticker.history(period="5d", interval="60m")
        elif time == "Mensal":
            df_history = ticker.history(period="30d", interval="90m")

        history = ticker.history(period="1d", interval="5m")

        if currency == "BRL":
            df_history[["Open", "High", "Low", "Close"]] = (
                df_history[["Open", "High", "Low", "Close"]] * dolar
            )

        if currency == "BRL":
            history[["Open", "High", "Low", "Close"]] = (
                history[["Open", "High", "Low", "Close"]] * dolar
            )

        latest_data = history.iloc[-1]
        general_data = Settings(
            symbol=self.ticker_symbol,
            open=round(Decimal(latest_data["Open"]), 2),
            higher=round(Decimal(latest_data["High"]), 2),
            lower=round(Decimal(latest_data["Low"]), 2),
            closed=round(Decimal(latest_data["Close"]), 2),
            volume=latest_data["Volume"],
        )

        return general_data, df_history

    def get_download(self, time, currency):
        dataframe = self.get_general_data(time, currency)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        if currency == "BRL":
            dataframe[["Open", "High", "Low", "Close"]] = (
                dataframe[["Open", "High", "Low", "Close"]] * dolar
            )
        dataframe = dataframe.sort_values("Datetime", ascending=False)
        return dataframe

    def plot_max_min(self, time, currency):
        dataframe = self.get_general_data(time, currency)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]

        if currency == "BRL":
            dataframe[["Open", "High", "Low", "Close"]] = (
                dataframe[["Open", "High", "Low", "Close"]] * dolar
            )

        fig_max_min = max_min_plot(
            dataframe["Low"],
            dataframe["High"],
            dataframe["Open"].mean(),
            time,
            self.ticker_symbol,
            currency,
        )

        return fig_max_min

    def plot_candle(self, time, currency):
        dataframe = self.get_general_data(time, currency)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]

        if currency == "BRL":
            dataframe[["Open", "High", "Low", "Close"]] = (
                dataframe[["Open", "High", "Low", "Close"]] * dolar
            )

        fig_candle = candle_plot(dataframe, self.ticker_symbol, currency)

        return fig_candle
