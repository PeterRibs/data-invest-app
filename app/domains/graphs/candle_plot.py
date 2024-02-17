import plotly.graph_objects as go


def candle_plot(
    df,
    ticker_symbol,
    currency,
    height_size=400,
    width_size=550,
):
    candle = go.Figure(
        data=[
            go.Candlestick(
                x=df["Datetime"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )

    candle.update_layout(
        title=f"Variação da ação: {ticker_symbol}",
        xaxis_title="Data - Hora",
        yaxis_title=f"Valor ({currency})",
        xaxis_rangeslider_visible=False,
        height=height_size,
        width=width_size,
    )
    return candle
