import streamlit as st
from app.domains.tickers_data.tickers_data import TickersData
from app.domains.tickers_data.ticker_list import ticker_list

st.set_page_config(layout="wide")

st.sidebar.image("app/assets/datainvest.png")

selected_ticker = st.sidebar.selectbox("Ação:", sorted(ticker_list))

time_list = ["Diário", "Semanal", "Mensal"]

time = st.sidebar.selectbox("Período analisado:", time_list)

col01, col02, col03, col04, col05 = st.columns(5)

ticker_data = TickersData(ticker_symbol=selected_ticker)
ticker_dataframe = ticker_data.get_download(time)

ticker_dataframe.columns = [
    "Data - Hora",
    "Abertura",
    "Máximo",
    "MÍmino",
    "Fechamento",
    "Qtd trades",
]

ticker_general_data = ticker_data.get_general_data(time)[0]

dolar = 4.97
open_value_brl = round((float(ticker_general_data.open) * dolar), 2)
higher_value_brl = round((float(ticker_general_data.higher) * dolar), 2)
lower_value_brl = round((float(ticker_general_data.lower) * dolar), 2)
closed_value_brl = round((float(ticker_general_data.closed) * dolar), 2)

col01.write(
    f"""\n
    Abertura: \n
    {ticker_general_data.open} USD \n
    {open_value_brl} BRL"""
)
col02.write(
    f"""\n
    Fechamento: \n
    {ticker_general_data.closed} USD \n
    {closed_value_brl} BRL"""
)
col03.write(
    f"""\n
    Máximo: \n
    {ticker_general_data.higher} USD \n
    {higher_value_brl} BRL"""
)
col04.write(
    f"""\n
    Mínimo: \n
    {ticker_general_data.lower} USD \n
    {lower_value_brl} BRL"""
)

col05.write(
    f"""\n
    Número de negociações: \n
    {ticker_general_data.volume}"""
)

charts, tables, compare, observations = st.tabs(
    ["Gráficos", "Tabela", "Comparativo", "Observações"]
)

with charts:
    col16, col17 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time))
    col17.plotly_chart(ticker_data.plot_close(time))

with tables:
    st.title(f"Tabela - {selected_ticker}")
    st.write(ticker_dataframe)

with compare:
    selected_ticker_second = st.selectbox("Segunda Ação:", ticker_list)
    ticker_data_second = TickersData(ticker_symbol=selected_ticker_second)

    col16, col17 = st.columns(2)
    col26, col27 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time))
    col17.plotly_chart(ticker_data_second.plot_candle(time))
    col16.plotly_chart(ticker_data.plot_close(time))
    col17.plotly_chart(ticker_data_second.plot_close(time))

with observations:
    st.title("Observações")
