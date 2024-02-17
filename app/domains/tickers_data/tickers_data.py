import yfinance as yf
from decimal import Decimal

from config.settings import Settings
from domains.graphs.close_plot import close_plot
from domains.graphs.candle_plot import candle_plot


class TickersData:
    def __init__(self, ticker_symbol):
        self.ticker_symbol: str = ticker_symbol

    def get_general_data(self, time):
        ticker = yf.Ticker(self.ticker_symbol)

        if time == "Diário":
            df_history = ticker.history(period="1d", interval="15m")
        elif time == "Semanal":
            df_history = ticker.history(period="5d", interval="60m")
        elif time == "Mensal":
            df_history = ticker.history(period="30d", interval="90m")

        history = ticker.history(period="1d", interval="5m")

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

    def get_download(self, time):
        dataframe = self.get_general_data(time)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]
        dataframe = dataframe.sort_values("Datetime", ascending=False)
        return dataframe

    def plot_close(self, time):
        dataframe = self.get_general_data(time)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]

        fig_close = close_plot(
            dataframe["Low"],
            dataframe["High"],
            dataframe["Open"].mean(),
            time,
            self.ticker_symbol,
        )

        return fig_close

    def plot_candle(self, time):
        dataframe = self.get_general_data(time)[1].reset_index()[
            ["Datetime", "Open", "High", "Low", "Close", "Volume"]
        ]

        fig_candle = candle_plot(
            dataframe,
            self.ticker_symbol,
        )

        return fig_candle
