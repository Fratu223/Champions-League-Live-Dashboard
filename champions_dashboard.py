import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import requests

# Configure the page
st.set_page_config(
    page_title="Champions League Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">⚽ UEFA Champions League Dashboard</h1>', unsafe_allow_html=True)

# Sidebar - API Key Input
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("### API Configuration")
st.sidebar.info("""
Get your free API key from:
[football-data.org](https://www.football-data.org/client/register)

Free tier: 10 requests/minute
""")

if 'API_KEY' in st.secrets:
    api_key = st.secrets['API_KEY']
else:
    api_key = st.sidebar.text_input("Enter API Key", type="password")

if not api_key:
    st.warning("⚠️ Please enter your API key in the sidebar to fetch live Champions League data.")
    st.markdown("""
    ### How to Get Started:
    1. Visit [football-data.org](https://www.football-data.org/client/register)
    2. Register for a free account
    3. Copy your API key
    4. Paste it in the sidebar
    5. Start viewing live Champions League data!
    """)
    st.stop()

# Sidebar controls
refresh_rate = st.sidebar.slider("Auto-refresh rate (seconds)", 30, 300, 60)
show_goals = st.sidebar.checkbox("Show Goal Statistics", value=True)
show_matches = st.sidebar.checkbox("Show Recent Matches", value=True)

# Function to fetch real Champions League data
@st.cache_data(ttl=60)
def fetch_champions_league_data(api_key):
    """
    Fetches live Champions League standings from football-data.org API
    """
    headers = {'X-Auth-Token': api_key}
    
    # Champions League competition code is 'CL'
    url = "https://api.football-data.org/v4/competitions/CL/standings"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        teams_list = []
        
        # Extract standings from all groups
        for standing in data.get('standings', []):
            if standing['type'] == 'TOTAL':
                for team_data in standing['table']:
                    teams_list.append({
                        'Team': team_data['team']['name'],
                        'Played': team_data['playedGames'],
                        'Wins': team_data['won'],
                        'Draws': team_data['draw'],
                        'Losses': team_data['lost'],
                        'Goals_For': team_data['goalsFor'],
                        'Goals_Against': team_data['goalsAgainst'],
                        'Goal_Difference': team_data['goalDifference'],
                        'Points': team_data['points'],
                        'Position': team_data['position']
                    })
        
        if not teams_list:
            return None, "No standings data available. The competition may not have started yet."
        
        df = pd.DataFrame(teams_list)
        df = df.sort_values(['Points', 'Goal_Difference', 'Goals_For'], ascending=[False, False, False])
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        
        return df, None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            return None, "❌ Invalid API key. Please check your key and try again."
        elif e.response.status_code == 429:
            return None, "⚠️ Rate limit exceeded. Please wait a moment and refresh."
        else:
            return None, f"❌ HTTP Error: {e.response.status_code}"
    except Exception as e:
        return None, f"❌ Error fetching data: {str(e)}"

# Function to fetch recent matches
@st.cache_data(ttl=60)
def fetch_recent_matches(api_key):
    """
    Fetches recent Champions League matches
    """
    headers = {'X-Auth-Token': api_key}
    url = "https://api.football-data.org/v4/competitions/CL/matches?status=FINISHED"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        matches_list = []
        for match in data.get('matches', [])[-10:]:  # Last 10 matches
            matches_list.append({
                'Date': match['utcDate'][:10],
                'Home Team': match['homeTeam']['name'],
                'Score': f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}",
                'Away Team': match['awayTeam']['name'],
                'Matchday': match.get('matchday', 'N/A')
            })
        
        return pd.DataFrame(matches_list) if matches_list else None
        
    except Exception as e:
        return None

# Fetch the data
df, error = fetch_champions_league_data(api_key)

if error:
    st.error(error)
    st.stop()

if df is None or len(df) == 0:
    st.warning("No Champions League data available at the moment. The competition may not have started yet.")
    st.stop()

# Last update time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.success(f"✅ Connected to API")
st.sidebar.info(f"Last updated: {current_time}")

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Teams", len(df))
with col2:
    st.metric("Total Goals", int(df['Goals_For'].sum()))
with col3:
    st.metric("Matches Played", int(df['Played'].sum()))
with col4:
    if df['Played'].sum() > 0:
        avg_goals = df['Goals_For'].sum() / df['Played'].sum()
        st.metric("Avg Goals/Match", f"{avg_goals:.2f}")
    else:
        st.metric("Avg Goals/Match", "0.00")

st.markdown("---")

# Standings Table
st.subheader("📊 Champions League Standings")

# Format the dataframe for display
display_df = df[['Team', 'Played', 'Wins', 'Draws', 'Losses', 'Goals_For', 'Goals_Against', 'Goal_Difference', 'Points']].copy()
display_df.columns = ['Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']

# Color code the top teams (top 8 qualify directly, 9-24 go to playoffs in new format)
def highlight_teams(row):
    if row.name <= 8:
        return ['background-color: #d4edda'] * len(row)
    elif row.name <= 24:
        return ['background-color: #fff3cd'] * len(row)
    else:
        return ['background-color: #f8d7da'] * len(row)

styled_df = display_df.style.apply(highlight_teams, axis=1)
st.dataframe(styled_df, use_container_width=True, height=600)

st.caption("🟢 Green: Direct qualification to Round of 16 | 🟡 Yellow: Playoff qualification | 🔴 Red: Eliminated")

st.markdown("---")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Points Comparison")
    top_teams = df.head(16)
    fig_points = px.bar(
        top_teams,
        x='Team',
        y='Points',
        color='Points',
        color_continuous_scale='Blues',
        title='Top 16 Teams by Points'
    )
    fig_points.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
    st.plotly_chart(fig_points, use_container_width=True)

with col2:
    st.subheader("⚽ Goal Difference")
    fig_gd = px.bar(
        top_teams,
        x='Team',
        y='Goal_Difference',
        color='Goal_Difference',
        color_continuous_scale='RdYlGn',
        title='Top 16 Teams by Goal Difference'
    )
    fig_gd.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
    st.plotly_chart(fig_gd, use_container_width=True)

if show_goals:
    st.markdown("---")
    st.subheader("🎯 Attack vs Defense Analysis")
    
    fig_scatter = px.scatter(
        df,
        x='Goals_Against',
        y='Goals_For',
        size='Points',
        color='Points',
        hover_name='Team',
        title='Goals Scored vs Goals Conceded',
        labels={'Goals_For': 'Goals Scored', 'Goals_Against': 'Goals Conceded'},
        color_continuous_scale='Viridis',
        size_max=30
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

if show_matches:
    st.markdown("---")
    st.subheader("⚽ Recent Matches")
    
    matches_df = fetch_recent_matches(api_key)
    
    if matches_df is not None and len(matches_df) > 0:
        st.dataframe(matches_df, use_container_width=True, height=400)
    else:
        st.info("No recent match data available.")

# Statistics summary
st.markdown("---")
st.subheader("📈 Key Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔝 Highest Scoring Team**")
    top_scorer = df.loc[df['Goals_For'].idxmax()]
    st.write(f"{top_scorer['Team']}: {int(top_scorer['Goals_For'])} goals")

with col2:
    st.markdown("**🛡️ Best Defense**")
    best_defense = df.loc[df['Goals_Against'].idxmin()]
    st.write(f"{best_defense['Team']}: {int(best_defense['Goals_Against'])} goals conceded")

with col3:
    st.markdown("**⭐ Best Goal Difference**")
    best_gd = df.loc[df['Goal_Difference'].idxmax()]
    st.write(f"{best_gd['Team']}: +{int(best_gd['Goal_Difference'])}")

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()