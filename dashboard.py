import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IPL Dashboard", layout="wide")

# Data Source
st.sidebar.markdown("### Data Source")
st.sidebar.info(
    "**Source:** Kaggle IPL Dataset\n"
    "**URL:** https://www.kaggle.com/datasets/meruvakodandasuraj/ipl-complete-dataset-2008-2025\n"
    f"**Extraction Date:** {datetime.now().strftime('%Y-%m-%d')}"
)
st.sidebar.image("IPL_logo.jpg", use_container_width=True)

# Read data
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
    
# Clean data
matches['season'] = matches['season'].astype(str)

# Sidebar title
st.sidebar.title("IPL Dashboard")
# Side bar divider(horizontal line)
st.sidebar.markdown("---")

#Get the user input for season
season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + sorted(matches['season'].unique(), reverse=True)
)

# Get the User input for teams
all_teams = sorted(set(matches['team1'].unique()) | set(matches['team2'].unique()))
team = st.sidebar.selectbox("Select Team", ["All"] + all_teams)

#filters
filtered = matches.copy()
if season != "All":
    filtered = filtered[filtered['season'] == season]
if team != "All":
    filtered = filtered[(filtered['team1'] == team) | (filtered['team2'] == team)]



st.title("IPL Cricket Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(filtered))
col2.metric("Seasons", len(filtered['season'].unique()))
col3.metric("Teams", len(set(filtered['team1'].unique()) | set(filtered['team2'].unique())))

st.markdown("---")

# Runs Per Match
st.subheader(" Runs Per Match Over Seasons")
if 'first_innings_score' in filtered.columns:
    runs_data = filtered.groupby('season').agg({
        'match_id': 'count',
        'first_innings_score': 'sum'
    }).reset_index()
    runs_data['avg_runs'] = runs_data['first_innings_score'] / runs_data['match_id']
    
    fig1 = px.line(runs_data, x='season', y='avg_runs', title="Average Runs Per Match")
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
else:
    alt_data = filtered.groupby('season').size().reset_index(name='matches')
    fig1 = px.bar(alt_data, x='season', y='matches', title="Matches Per Season")
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)


