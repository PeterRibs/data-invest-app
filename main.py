import streamlit as st
from app.domains.tickers_data.tickers_data import TickersData
from app.domains.tickers_data.ticker_list import ticker_list
from app.domains.database.database_functions import Database

database = Database("datainvest_database.db")
database.create_table()

st.set_page_config(layout="wide")

col000, col001, col002, col003, col004 = st.columns(5)
col00, col01, col02, col03, col05 = st.columns(5)

col000.image("app/assets/datainvest.png", width=200)

selected_ticker = col001.selectbox("Ação:", sorted(ticker_list))

time_list = ["Diário", "Semanal", "Mensal"]

time = col002.selectbox("Período analisado:", time_list)

currency_list = ["USD", "BRL"]

currency = col003.selectbox("Moeda:", currency_list)

ticker_data = TickersData(ticker_symbol=selected_ticker)
ticker_dataframe = ticker_data.get_download(time, currency)

ticker_dataframe.columns = [
    "Data - Hora",
    "Abertura",
    "Máximo",
    "Mímino",
    "Fechamento",
    "Qtd trades",
]


ticker_general_data = ticker_data.get_general_data(time, currency)[0]

ticker_data_open_mean = round(
    ticker_data.get_general_data(time, currency)[1]["Open"].mean(), 2
)
ticker_data_close_mean = round(
    ticker_data.get_general_data(time, currency)[1]["Close"].mean(), 2
)
col00.title(
    f"""{selected_ticker} 
{currency} - {time}"""
)
col01.write(f"""Abertura: {ticker_general_data.open}""")
col01.metric(
    label="Fechamento:",
    value=float(ticker_general_data.closed),
    delta=round(float(ticker_general_data.closed) - float(ticker_general_data.open), 2),
)
col02.write(f"""Máximo: {ticker_general_data.higher}""")
col02.metric(
    label="Mínimo:",
    value=float(ticker_general_data.lower),
    delta=round(
        float(ticker_general_data.lower) - float(ticker_general_data.higher), 2
    ),
)
col03.write(f"""Média de abertura: {ticker_data_open_mean}""")
col03.metric(
    label="Média de fechamento:",
    value=float(ticker_data_close_mean),
    delta=round(float(ticker_data_close_mean) - float(ticker_data_open_mean), 2),
)
col05.write(f"""Número de negociações: {ticker_general_data.volume}""")

charts, tables, compare, notes = st.tabs(
    ["Gráficos", "Tabela", "Comparativo", "Anotações"]
)

with charts:
    col16, col17 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time, currency))
    col17.plotly_chart(ticker_data.plot_max_min(time, currency))

    note = st.text_area("Adicione uma anotação:", key="note_individual")
    if st.button("Salvar", key="save_individual"):
        database.insert_note(time, "individual", selected_ticker, note)
        st.success("Salvo com sucesso!")
        note = ""

with tables:
    st.write(ticker_dataframe)

with compare:

    col_compare_0, col_compare_1, col_compare_2, col_compare_3, col_compare_4 = (
        st.columns(5)
    )
    selected_ticker_second = col_compare_3.selectbox("Segunda Ação:", ticker_list)
    ticker_data_second = TickersData(ticker_symbol=selected_ticker_second)

    col16, col17 = st.columns(2)
    col26, col27 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time, currency))
    col17.plotly_chart(ticker_data_second.plot_candle(time, currency))
    col16.plotly_chart(ticker_data.plot_max_min(time, currency))
    col17.plotly_chart(ticker_data_second.plot_max_min(time, currency))

    note = st.text_area("Adicione um anotação:", key="note_compare")
    if st.button("Salvar", key="save_compare"):
        database.insert_note(
            time,
            "comparação",
            f"{selected_ticker} - {selected_ticker_second}",
            note,
        )
        st.success("Salvo com sucesso!")
        note = ""

with notes:
    ticker_notes = database.get_notes_as_dataframe(selected_ticker)
    ticker_notes = ticker_notes.drop("id", axis=1)
    ticker_notes.columns = ["Data", "Período", "Área", "Ação", "Anotação"]
    st.write(ticker_notes)
