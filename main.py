import streamlit as st
from app.domains.tickers_data.tickers_data import TickersData
from app.domains.tickers_data.ticker_list import ticker_list
from app.domains.database.database_functions import Database

database = Database("datainvest_database.db")
database.create_table()

st.set_page_config(layout="wide")

# Header
col00, col01, col02, col03, col04 = st.columns(5)
col10, col11, col12, col13, col14, col15 = st.columns(6)

col00.image("app/assets/datainvest.png", width=200)

selected_ticker = col01.selectbox("Ação:", sorted(ticker_list))

time_list = ["Diário", "Semanal", "Mensal"]
time = col02.selectbox("Período analisado:", time_list)

currency_list = ["USD", "BRL"]
currency = col03.selectbox("Moeda:", currency_list)

ticker_data = TickersData(ticker_symbol=selected_ticker)
ticker_dataframe = ticker_data.get_download(time, currency)

tricker_get_general_data = ticker_data.get_general_data(time, currency)
ticker_general_data = tricker_get_general_data[0]
ticker_data_open_mean = round(tricker_get_general_data[1]["Open"].mean(), 2)
ticker_data_close_mean = round(tricker_get_general_data[1]["Close"].mean(), 2)
ticker_data_dividend = ticker_data.get_dividends_data(currency)

col10.title(
    f"""{selected_ticker} 
{currency} - {time}"""
)
col11.write(f"""Abertura: {ticker_general_data.open}""")
col11.metric(
    label="Fechamento:",
    value=float(ticker_general_data.closed),
    delta=round(float(ticker_general_data.closed) - float(ticker_general_data.open), 2),
)
col12.write(f"""Máximo: {ticker_general_data.higher}""")
col12.metric(
    label="Mínimo:",
    value=float(ticker_general_data.lower),
    delta=round(
        float(ticker_general_data.lower) - float(ticker_general_data.higher), 2
    ),
)
col13.write(f"""Média de abertura: {ticker_data_open_mean}""")
col13.metric(
    label="Média de fechamento:",
    value=float(ticker_data_close_mean),
    delta=round(float(ticker_data_close_mean) - float(ticker_data_open_mean), 2),
)
col14.write(f"""Dividendo anterior: {round(float(ticker_data_dividend[0][-2]),2)}""")
col14.metric(
    label="Dividendo:",
    value=round(float(ticker_data_dividend[0][-1]), 2),
    delta=round(
        float(ticker_data_dividend[0][-1]) - float(ticker_data_dividend[0][-2]),
        2,
    ),
)
col15.metric(
    label="Negociações:",
    value=round(int(tricker_get_general_data[0].volume), 2),
    delta=round(
        int(tricker_get_general_data[0].volume)
        - int(tricker_get_general_data[0].penultimate_data_volume),
        2,
    ),
)

# Tabs
charts, tables, notes, compare = st.tabs(
    ["Gráficos", "Tabela", "Anotações", "Comparativo"]
)

with charts:
    col20, col21 = st.columns(2)
    col20.plotly_chart(ticker_data.plot_candle(time, currency))
    col21.plotly_chart(ticker_data.plot_max_min(time, currency))

    note = st.text_area("Adicione uma anotação:", key="note_individual")
    if st.button("Salvar", key="save_individual"):
        database.insert_note(time, "individual", selected_ticker, note)
        st.success("Salvo com sucesso!")
        note = ""

with tables:
    ticker_dataframe.columns = [
        "Data - Hora",
        "Abertura",
        "Máximo",
        "Mímino",
        "Fechamento",
        "Qtd trades",
    ]
    st.write(ticker_dataframe)

with notes:
    ticker_notes = database.get_notes_as_dataframe(selected_ticker)
    ticker_notes = ticker_notes.drop("id", axis=1)
    ticker_notes.columns = ["Data", "Período", "Área", "Ação", "Anotação"]
    st.write(ticker_notes)

with compare:
    col20, col21, col22, col23, col24 = st.columns(5)
    col30, col31 = st.columns(2)
    col40, col41 = st.columns(2)
    col50, col51 = st.columns(2)

    selected_ticker_second = col23.selectbox("Segunda Ação:", ticker_list)
    ticker_data_second = TickersData(ticker_symbol=selected_ticker_second)

    col30.plotly_chart(ticker_data.plot_candle(time, currency))
    col31.plotly_chart(ticker_data_second.plot_candle(time, currency))
    col40.plotly_chart(ticker_data.plot_max_min(time, currency))
    col41.plotly_chart(ticker_data_second.plot_max_min(time, currency))
    col50.plotly_chart(ticker_data.plot_dividends(currency))
    col51.plotly_chart(ticker_data_second.plot_dividends(currency))

    note = st.text_area("Adicione uma anotação:", key="note_compare")
    if st.button("Salvar", key="save_compare"):
        database.insert_note(
            time,
            "comparação",
            f"{selected_ticker} - {selected_ticker_second}",
            note,
        )
        st.success("Salvo com sucesso!")
        note = ""
