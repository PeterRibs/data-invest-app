import streamlit as st
from app.domains.tickers_data.tickers_data import TickersData
from app.domains.tickers_data.ticker_list import ticker_list
from app.domains.database.database_functions import Database

database = Database("datainvest_database.db")
database.create_table()

time_list = ["Diário", "Semanal", "Mensal"]
currency_list = ["USD", "BRL"]

# Sidebar
st.set_page_config(layout="wide")
st.sidebar.image("app/assets/datainvest.png")
selected_ticker = st.sidebar.selectbox("Ação:", sorted(ticker_list))
time = st.sidebar.selectbox("Período analisado:", time_list)
currency = st.sidebar.selectbox("Moeda:", currency_list)

# Header
col00, col01, col02, col03, col04 = st.columns(5)

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
col04.write(f"""Número de negociações: {ticker_general_data.volume}""")

# Tabs
charts, tables, notes, compare = st.tabs(
    ["Gráficos", "Tabela", "Anotações", "Comparativo"]
)

with charts:
    col10, col11 = st.columns(2)
    col10.plotly_chart(ticker_data.plot_candle(time, currency))
    col11.plotly_chart(ticker_data.plot_max_min(time, currency))

    note = st.text_area("Adicione uma anotação:", key="note_individual")
    if st.button("Salvar", key="save_individual"):
        database.insert_note(time, "individual", selected_ticker, note)
        st.success("Salvo com sucesso!")
        note = ""

with tables:
    st.write(ticker_dataframe)

with notes:
    ticker_notes = database.get_notes_as_dataframe(selected_ticker)
    ticker_notes = ticker_notes.drop("id", axis=1)
    ticker_notes.columns = ["Data", "Período", "Área", "Ação", "Anotação"]
    st.write(ticker_notes)

with compare:
    col10, col11, col12, col13, col14 = st.columns(5)
    col20, col21 = st.columns(2)
    col30, col31 = st.columns(2)

    selected_ticker_second = col13.selectbox("Segunda Ação:", ticker_list)
    ticker_data_second = TickersData(ticker_symbol=selected_ticker_second)

    col20.plotly_chart(ticker_data.plot_candle(time, currency))
    col21.plotly_chart(ticker_data_second.plot_candle(time, currency))
    col30.plotly_chart(ticker_data.plot_max_min(time, currency))
    col31.plotly_chart(ticker_data_second.plot_max_min(time, currency))

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
