import plotly.express as px


def dividend_plot(
    axis_x,
    axis_y,
    ticker_symbol,
    currency,
    height_size=400,
    width_size=560,
):
    line_plot = px.line(
        x=axis_x,
        y=axis_y,
        title=f"Últimos dividendos de {ticker_symbol}",
        markers=True,
        height=height_size,
        width=width_size,
    )
    line_plot.update_traces(line_color="#7092BE", line_width=3.6, name="Mínimo")
    line_plot.update_xaxes(title_text="Data", showgrid=True, gridcolor="gray")
    line_plot.update_yaxes(
        title_text=f"Valor ({currency})", showgrid=True, gridcolor="gray"
    )

    return line_plot
