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
