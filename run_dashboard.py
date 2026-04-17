import streamlit as st
import pandas as pd
import altair as alt
from babel import Locale
from sqlalchemy import text
from src.database import engine

st.set_page_config(page_title="Movies Dashboard", layout="wide")
st.title("Movies Dashboard")


@st.cache_data(ttl=60)
def load_movies():
    """Carrega filmes do banco e adiciona colunas auxiliares (year, display_title)."""
    query = text("""
        SELECT id, title, original_title, original_language,
               popularity, release_date, vote_average, vote_count
        FROM movies
        WHERE release_date IS NOT NULL
        ORDER BY popularity DESC
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    df["year"] = pd.to_datetime(df["release_date"]).dt.year
    df["display_title"] = "[" + df["original_language"].str.upper() + "] - " + df["title"]
    return df


df = load_movies()

if df.empty:
    st.warning("Nenhum filme encontrado na base de dados.")
    st.stop()

# --- 1. Top 10 Popularidade ---
st.header("Top 10 Filmes por Popularidade")

top10 = df.nlargest(10, "popularity")[["display_title", "popularity", "vote_average", "year"]].reset_index(drop=True)
top10.index = top10.index + 1
top10.columns = ["Filme", "Popularidade", "Nota Média", "Ano"]

col1, col2 = st.columns([1, 1])
with col1:
    st.dataframe(top10, use_container_width=True)
with col2:
    bars_top10 = alt.Chart(top10).mark_bar().encode(
        x=alt.X("Filme:N", sort="-y", title="Filme"),
        y=alt.Y("Popularidade:Q"),
        tooltip=["Filme", "Popularidade", "Nota Média", "Ano"],
    ).properties(height=400)
    st.altair_chart(bars_top10, use_container_width=True)

# --- 2. Filme mais popular por ano ---
st.header("Filme Mais Popular por Ano")

idx_max = df.groupby("year")["popularity"].idxmax()
top_by_year = df.loc[idx_max, ["year", "display_title", "popularity", "vote_average"]].sort_values("year", ascending=False)
top_by_year.columns = ["Ano", "Filme", "Popularidade", "Nota Média"]
top_by_year = top_by_year.reset_index(drop=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.dataframe(top_by_year, use_container_width=True)
with col2:
    chart_data = top_by_year.set_index("Ano")[["Popularidade"]]
    st.line_chart(chart_data)

# --- 3. Rank interno por língua original ---
st.header("Ranking por Língua Original")

lang_counts = df["original_language"].value_counts().reset_index()
lang_counts.columns = ["code", "total"]


LANG_ALIASES = {
    "cn": "zh",
}


def _resolve_lang_name(code):
    try:
        resolved = LANG_ALIASES.get(code, code)
        return Locale(resolved).get_language_name("pt_BR") or code
    except Exception:
        return code


def lang_label(code, total):
    name = _resolve_lang_name(code)
    return f"[{code.upper()}] - {name.title()} ({total})"


lang_options = [lang_label(row["code"], row["total"]) for _, row in lang_counts.iterrows()]
lang_codes = lang_counts["code"].tolist()

selected_option = st.selectbox("Selecione a língua:", lang_options)
selected_lang = lang_codes[lang_options.index(selected_option)]

lang_df = df[df["original_language"] == selected_lang].copy()
lang_df = lang_df.sort_values("popularity", ascending=False).reset_index(drop=True)
lang_df.index = lang_df.index + 1
lang_display = lang_df[["display_title", "popularity", "vote_average", "year"]]
lang_display.columns = ["Filme", "Popularidade", "Nota Média", "Ano"]

col1, col2 = st.columns([1, 1])
with col1:
    st.dataframe(lang_display.head(20), use_container_width=True)
with col2:
    chart_lang = lang_display.head(20).reset_index(drop=True)
    bars = alt.Chart(chart_lang).mark_bar().encode(
        x=alt.X("Ano:O", sort="ascending", title="Ano"),
        y=alt.Y("Popularidade:Q"),
        tooltip=["Filme", "Popularidade", "Nota Média", "Ano"],
    ).properties(height=400)
    st.altair_chart(bars, use_container_width=True)

st.caption(f"Total de filmes: {len(lang_df)}")

# --- 4. Média de popularidade por língua ---
st.header("Comparativo de Popularidade Média por Língua")

avg_by_lang = (
    df.groupby("original_language")["popularity"]
    .agg(["mean", "count"])
    .reset_index()
)
avg_by_lang.columns = ["code", "Popularidade Média", "Qtd Filmes"]
avg_by_lang["Língua"] = avg_by_lang["code"].apply(
    lambda c: f"[{c.upper()}] - {_resolve_lang_name(c).title()}"
)
avg_by_lang = avg_by_lang.drop(columns=["code"])
avg_by_lang = avg_by_lang[["Língua", "Qtd Filmes", "Popularidade Média"]]

min_films = st.slider("Mínimo de filmes por língua:", 1, int(avg_by_lang["Qtd Filmes"].max()), 3)
avg_filtered = avg_by_lang[avg_by_lang["Qtd Filmes"] >= min_films].sort_values("Popularidade Média", ascending=False)
avg_filtered = avg_filtered.reset_index(drop=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.dataframe(avg_filtered, use_container_width=True)
with col2:
    bars_avg = alt.Chart(avg_filtered).mark_bar().encode(
        x=alt.X("Língua:N", sort="-y", title="Língua"),
        y=alt.Y("Popularidade Média:Q"),
        tooltip=["Língua", "Qtd Filmes", "Popularidade Média"],
    ).properties(height=400)
    st.altair_chart(bars_avg, use_container_width=True)
