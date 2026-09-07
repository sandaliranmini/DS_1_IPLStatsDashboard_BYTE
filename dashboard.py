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

# 2 charts of Top Batsman and Bowlers
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Run-Scorers")
    batsmen = deliveries[deliveries['match_id'].isin(filtered['match_id'])]
    top_bats = batsmen.groupby('striker')['batsman_runs'].sum().reset_index()
    top_bats.columns = ['Player', 'Runs']
    top_bats = top_bats.sort_values('Runs', ascending=False).head(10)
    
    fig2 = px.bar(top_bats, x='Runs', y='Player', orientation='h', 
                  title="Top Run-Scorers", color='Runs',
                  color_continuous_scale='Viridis')
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Top 10 Wicket-Takers")
    wickets = deliveries[(deliveries['match_id'].isin(filtered['match_id'])) & 
                         (deliveries['is_wicket'] == 1)]
    top_wkts = wickets.groupby('bowler').size().reset_index(name='Wickets')
    top_wkts = top_wkts.sort_values('Wickets', ascending=False).head(10)
    
    fig3 = px.bar(top_wkts, x='Wickets', y='bowler', orientation='h',
                  title="Top Wicket-Takers", color='Wickets',
                  color_continuous_scale='Reds')
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

# Team Win Percentage chart
st.subheader("Team Win Percentages")

wins = filtered['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']

# Count total matches per team
total = pd.concat([filtered['team1'], filtered['team2']]).value_counts().reset_index()
total.columns = ['Team', 'Total']

win_pct = total.merge(wins, on='Team', how='left')
win_pct['Wins'] = win_pct['Wins'].fillna(0)
win_pct['Win%'] = (win_pct['Wins'] / win_pct['Total'] * 100).round(2)
win_pct = win_pct.sort_values('Win%', ascending=False)

fig4 = px.bar(win_pct, x='Team', y='Win%', title="Win Percentage by Team",
              text='Win%',
              color='Win%',
              color_continuous_scale='Blues')
fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig4.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig4, use_container_width=True)

#Insight
st.markdown("---")
st.subheader("Key Insights")
st.write("• Dashboard shows IPL statistics from multiple seasons")
st.write("• Use filters in sidebar to explore specific seasons/teams")
st.write("• All charts update automatically based on filters") 
