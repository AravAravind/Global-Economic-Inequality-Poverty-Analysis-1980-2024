import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 Global Inequality & Poverty Dashboard")


df = pd.read_csv("archive/disuguaglianza-economica-globale-e-povert-1980-2024.csv")
df.columns = df.columns.str.strip()

df["gap"] = df["income_top10"] - df["income_bottom50"]


st.sidebar.header("Filters")

countries = df["country"].unique()
selected_country = st.sidebar.selectbox("Select Country", countries)

year = st.sidebar.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max())
)


country_df = df[df["country"] == selected_country]
year_df = df[df["year"] == year]



col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        country_df,
        x="year",
        y="gini_index",
        title=f"{selected_country} Inequality Trend"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(
        country_df,
        x="year",
        y="poverty_rate",
        title=f"{selected_country} Poverty Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)



col3, col4 = st.columns(2)

with col3:
    fig3 = px.line(
        country_df,
        x="year",
        y="gap",
        title="Income Gap (Top 10% vs Bottom 50%)"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.choropleth(
        year_df,
        locations="country",
        locationmode="country names",
        color="gini_index",
        title=f"Global Inequality Map ({year})"
    )
    st.plotly_chart(fig4, use_container_width=True)



st.subheader("🔥 Top Inequality Countries")

top = year_df.sort_values("gap", ascending=False).head(10)

fig5 = px.bar(
    top,
    x="gap",
    y="country",
    orientation="h",
    title="Top 10 Inequality Gap Countries"
)

st.plotly_chart(fig5, use_container_width=True)