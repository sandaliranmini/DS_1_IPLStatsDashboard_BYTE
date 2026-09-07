import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

st.set_page_config(page_title="IPL Dashboard", layout="wide")

#export function
def download_chart_button(fig, filename, button_text):
    """Convert plotly figure to PNG and provide download button"""
    try:
        img_bytes = fig.to_image(format="png", width=800, height=500)
        b64 = base64.b64encode(img_bytes).decode()
        
        button_html = f'''
            <a href="data:image/png;base64,{b64}" download="{filename}.png" target="_blank">
                <button style="
                    background-color: #1a237e;
                    color: white;
                    padding: 8px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                ">
                    {button_text}
                </button>
            </a>
        '''
        return button_html
    except Exception as e:
        return f"Export error: {e}"


# Data Source
st.sidebar.markdown("### Data Source")
st.sidebar.info(
    "**Source:** Kaggle IPL Dataset\n"
    "**URL:** https://www.kaggle.com/datasets/meruvakodandasuraj/ipl-complete-dataset-2008-2025\n"
    f"**Extraction Date:**2026-09-05"
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
runs = deliveries[deliveries['match_id'].isin(filtered['match_id'])].groupby('match_id')['total_runs'].sum().reset_index()
runs = runs.merge(matches[['match_id', 'date']], on='match_id').sort_values('date')
fig1 = px.line(runs, x='date', y='total_runs', title="Runs Per Match")
if 'first_innings_score' in filtered.columns:
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    # Export button for Runs per match Chart
    st.markdown(download_chart_button(fig1, "runs_per_match", "Download Chart as PNG"), unsafe_allow_html=True)
else:
    st.warning("⚠️ 'first_innings_score' column not found. Showing matches per season instead.")
    alt_data = filtered.groupby('season').size().reset_index(name='matches')
    fig1 = px.bar(alt_data, x='season', y='matches', title="Matches Per Season",
                  color_discrete_sequence=['#1a237e'])
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Export button for Chart Runs per match alternative
    st.markdown(download_chart_button(fig1, "matches_per_season", "Download Chart as PNG"), unsafe_allow_html=True)
    

st.markdown("---")

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

    # Export button for chart of Top Batsmans
    st.markdown(download_chart_button(fig2, "top_run_scorers", "Download Chart as PNG"), unsafe_allow_html=True)

with col2:
    st.subheader("Top 10 Wicket-Takers")
    wickets = wickets[~wickets['dismissal_type'].isin(['run out', 'retired hurt', 'obstructing the field'])]
    top_wkts = wickets.groupby('bowler').size().reset_index(name='Wickets')
    top_wkts = top_wkts.sort_values('Wickets', ascending=False).head(10)
    
    fig3 = px.bar(top_wkts, x='Wickets', y='bowler', orientation='h',
                  title="Top Wicket-Takers", color='Wickets',
                  color_continuous_scale='Reds')
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

    # Export button for chart of top bowlers
    st.markdown(download_chart_button(fig3, "top_wicket_takers", "Download Chart as PNG"), unsafe_allow_html=True)

st.markdown("---")

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

# Export button for Chart of team win percentage
st.markdown(download_chart_button(fig4, "team_win_percentages", "Download Chart as PNG"), unsafe_allow_html=True)

#Insight
st.markdown("---")
st.subheader("Key Insights")
st.write("• Dashboard shows IPL statistics from multiple seasons")
st.write("• Use filters in sidebar to explore specific seasons/teams")
st.write("• All charts update automatically based on filters") 

# footer
st.markdown("---")
st.markdown("""
    <div style="display: flex; justify-content: space-between; color: #888; font-size: 12px; padding: 5px;">
        <span>IPL Dashboard • AVIP 2026</span>
        <span>Data: Kaggle IPL Dataset 2008-2025</span>
        <span>Generated: {datetime}</span>
    </div>
""".format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)