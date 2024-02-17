import plotly.express as px
import plotly.graph_objects as go


def max_min_plot(
    axis_y,
    axis_y_2,
    axis_y_3,
    time_title,
    ticker_symbol,
    currency,
    height_size=400,
    width_size=550,
):
    line_plot = px.line(
        y=axis_y,
        title=f"{ticker_symbol}  - {time_title}",
        markers=True,
        height=height_size,
        width=width_size,
    )
    line_plot.update_traces(
        line_color="#7092BE", line_width=3.6, name="Mínimo", showlegend=True
    )
    line_plot.update_xaxes(title_text="Data - Hora", showgrid=True, gridcolor="gray")
    line_plot.update_yaxes(
        title_text=f"Valor ({currency})", showgrid=True, gridcolor="gray"
    )

    if axis_y_2 is not None:
        line_plot.add_trace(
            go.Scatter(y=axis_y_2, name="Máximo", line=dict(color="blue"))
        )

    if axis_y_3 is not None:
        line_plot.add_hline(
            y=axis_y_3,
            name="Média",
            line_color="red",
            showlegend=True,
        )
    return line_plot
