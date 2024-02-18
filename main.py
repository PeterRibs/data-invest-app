import streamlit as st
from app.domains.tickers_data.tickers_data import TickersData
from app.domains.tickers_data.ticker_list import ticker_list
from app.domains.database.database_functions import Database

database = Database("datainvest_database.db")
database.create_table()

st.set_page_config(layout="wide")

st.sidebar.image("app/assets/datainvest.png")

selected_ticker = st.sidebar.selectbox("Ação:", sorted(ticker_list))

time_list = ["Diário", "Semanal", "Mensal"]

time = st.sidebar.selectbox("Período analisado:", time_list)

currency_list = ["USD", "BRL"]

currency = st.sidebar.selectbox("Moeda:", currency_list)

col01, col02, col03, col05 = st.columns(4)

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

col01.write(f"""Abertura: {ticker_general_data.open} {currency}""")
col01.metric(
    label="Fechamento:",
    value=float(ticker_general_data.closed),
    delta=round(float(ticker_general_data.closed) - float(ticker_general_data.open), 2),
)
col02.write(f"""Máximo: {ticker_general_data.higher} {currency}""")
col02.metric(
    label="Mínimo:",
    value=float(ticker_general_data.lower),
    delta=round(
        float(ticker_general_data.lower) - float(ticker_general_data.higher), 2
    ),
)
col03.write(f"""Média de abertura: {ticker_data_open_mean} {currency}""")
col03.metric(
    label="Média de fechamento:",
    value=float(ticker_data_close_mean),
    delta=round(float(ticker_data_close_mean) - float(ticker_data_open_mean), 2),
)
col05.write(f"""Número de negociações: {ticker_general_data.volume}""")

charts, tables, compare, observations = st.tabs(
    ["Gráficos", "Tabela", "Comparativo", "Observações"]
)

with charts:
    col16, col17 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time, currency))
    col17.plotly_chart(ticker_data.plot_max_min(time, currency))

    comment = st.text_area("Adicione um comentário:", key="comment_individual")
    if st.button("Salvar", key="save_individual"):
        database.insert_comment(time, "individual", selected_ticker, comment)
        st.success("Salvo com sucesso!")
        comment = ""

with tables:
    st.title(f"Tabela - {selected_ticker}")
    st.write(ticker_dataframe)

with compare:
    selected_ticker_second = st.selectbox("Segunda Ação:", ticker_list)
    ticker_data_second = TickersData(ticker_symbol=selected_ticker_second)

    col16, col17 = st.columns(2)
    col26, col27 = st.columns(2)
    col16.plotly_chart(ticker_data.plot_candle(time, currency))
    col17.plotly_chart(ticker_data_second.plot_candle(time, currency))
    col16.plotly_chart(ticker_data.plot_max_min(time, currency))
    col17.plotly_chart(ticker_data_second.plot_max_min(time, currency))

    comment = st.text_area("Adicione um comentário:", key="comment_compare")
    if st.button("Salvar", key="save_compare"):
        database.insert_comment(
            time,
            "comparação",
            f"{selected_ticker} - {selected_ticker_second}",
            comment,
        )
        st.success("Salvo com sucesso!")
        comment = ""

with observations:
    st.title("Observações")
    ticker_comments = database.get_comments_as_dataframe(selected_ticker)
    ticker_comments = ticker_comments.drop("id", axis=1)
    ticker_comments.columns = ["Data", "Período", "Área", "Ação", "Comentário"]
    st.write(ticker_comments)
