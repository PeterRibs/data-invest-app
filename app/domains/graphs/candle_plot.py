import plotly.graph_objects as go


def candle_plot(
    df,
    ticker_symbol,
    currency,
    time,
):
    candle = go.Figure(
        data=[
            go.Candlestick(
                x=df["Datetime"] if time == "Diário" else None,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )

    candle.update_layout(
        title=f"{ticker_symbol}",
        xaxis_title="Data - Hora",
        yaxis_title=f"Valor ({currency})",
        xaxis_rangeslider_visible=False,
    )
    return candle
