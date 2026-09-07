import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Load data
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
matches['season'] = matches['season'].astype(str)

print("📊 Generating HTML charts...")

# Chart 1: Runs Per Match
runs_data = matches.groupby('season').agg({
    'match_id': 'count',
    'first_innings_score': 'sum'
}).reset_index()
runs_data['avg_runs'] = runs_data['first_innings_score'] / runs_data['match_id']
fig1 = px.line(runs_data, x='season', y='avg_runs', title="Runs Per Match")
pio.write_html(fig1, "charts/runs_per_match.html")
print("✅ runs_per_match.html")

# Chart 2: Top Batsmen
top_bats = deliveries.groupby('striker')['batsman_runs'].sum().reset_index()
top_bats.columns = ['Player', 'Runs']
top_bats = top_bats.sort_values('Runs', ascending=False).head(10)
fig2 = px.bar(top_bats, x='Runs', y='Player', orientation='h', title="Top Run-Scorers")
fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
pio.write_html(fig2, "charts/top_run_scorers.html")
print("✅ top_run_scorers.html")

# Chart 3: Top Bowlers
wickets = deliveries[deliveries['is_wicket'] == 1]
top_wkts = wickets.groupby('bowler').size().reset_index(name='Wickets')
top_wkts = top_wkts.sort_values('Wickets', ascending=False).head(10)
fig3 = px.bar(top_wkts, x='Wickets', y='bowler', orientation='h', title="Top Wicket-Takers")
fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
pio.write_html(fig3, "charts/top_wicket_takers.html")
print("✅ top_wicket_takers.html")

# Chart 4: Team Win %
wins = matches['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']
total = pd.concat([matches['team1'], matches['team2']]).value_counts().reset_index()
total.columns = ['Team', 'Total']
win_pct = total.merge(wins, on='Team', how='left')
win_pct['Wins'] = win_pct['Wins'].fillna(0)
win_pct['Win%'] = (win_pct['Wins'] / win_pct['Total'] * 100).round(2)
fig4 = px.bar(win_pct, x='Team', y='Win%', title="Team Win %", text='Win%')
fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
pio.write_html(fig4, "charts/team_win_percentages.html")
print("✅ team_win_percentages.html")

print("\n🎉 All charts saved as HTML in /charts/ folder!")
print("\n📌 Next steps:")
print("   1. Open File Explorer")
print("   2. Go to the 'charts' folder")
print("   3. Double-click each .html file to open in browser")
print("   4. Take screenshots using Snipping Tool (Windows+Shift+S)")
print("   5. Save as PNG with the same names")