import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import random

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

# Sidebar controls
st.sidebar.title("Dashboard Controls")
refresh_rate = st.sidebar.slider("Auto-refresh rate (seconds)", 5, 60, 30)
show_goals = st.sidebar.checkbox("Show Goal Statistics", value=True)
show_form = st.sidebar.checkbox("Show Recent Form", value=True)

# Function to generate realistic team data with updates
def fetch_team_stats():
    """
    Simulates fetching live Champions League data
    In production, replace this with actual API calls or web scraping
    """
    teams_data = {
        'Team': [
            'Real Madrid', 'Bayern Munich', 'Manchester City', 'PSG',
            'Arsenal', 'Inter Milan', 'Barcelona', 'Liverpool',
            'Atletico Madrid', 'Borussia Dortmund', 'AC Milan', 'Chelsea',
            'Juventus', 'Benfica', 'Porto', 'Ajax'
        ],
        'Played': [6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5],
        'Wins': [5, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1],
        'Draws': [1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 0],
        'Losses': [0, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 3, 4],
        'Goals_For': [18, 16, 15, 12, 14, 11, 13, 12, 8, 9, 7, 8, 6, 5, 4, 3],
        'Goals_Against': [4, 6, 5, 7, 8, 9, 10, 11, 6, 8, 9, 10, 9, 8, 11, 15],
        'Recent_Form': ['W-W-W-D-W', 'W-W-L-W-W', 'W-W-W-L-D', 'D-W-L-W-D',
                       'W-D-W-L-W', 'W-L-W-D-W', 'D-W-W-L-L', 'W-L-W-L-D',
                       'W-D-L-W-D', 'L-W-W-L-D', 'D-W-L-L-W', 'L-W-D-L-W',
                       'W-L-D-W-L', 'D-L-D-W-L', 'L-L-W-D-L', 'L-L-L-L-W']
    }
    
    df = pd.DataFrame(teams_data)
    
    # Calculate additional statistics
    df['Points'] = df['Wins'] * 3 + df['Draws']
    df['Goal_Difference'] = df['Goals_For'] - df['Goals_Against']
    
    # Add small random variations to simulate live updates
    if 'last_update' in st.session_state:
        for idx in range(len(df)):
            if random.random() < 0.1:  # 10% chance of goal update
                df.loc[idx, 'Goals_For'] += random.choice([0, 1])
    
    # Sort by points, then goal difference
    df = df.sort_values(['Points', 'Goal_Difference', 'Goals_For'], ascending=[False, False, False])
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    
    return df

# Fetch the data
df = fetch_team_stats()

# Last update time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.info(f"Last updated: {current_time}")

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Teams", len(df), delta=None)
with col2:
    st.metric("Total Goals", int(df['Goals_For'].sum()), delta=None)
with col3:
    st.metric("Matches Played", int(df['Played'].sum()), delta=None)
with col4:
    avg_goals = df['Goals_For'].sum() / df['Played'].sum()
    st.metric("Avg Goals/Match", f"{avg_goals:.2f}", delta=None)

st.markdown("---")

# Standings Table
st.subheader("📊 Group Stage Standings")

# Format the dataframe for display
display_df = df[['Team', 'Played', 'Wins', 'Draws', 'Losses', 'Goals_For', 'Goals_Against', 'Goal_Difference', 'Points']]
display_df.columns = ['Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']

# Color code the top teams
def highlight_top_teams(row):
    if row.name <= 8:
        return ['background-color: #d4edda'] * len(row)
    elif row.name <= 12:
        return ['background-color: #fff3cd'] * len(row)
    else:
        return ['background-color: #f8d7da'] * len(row)

styled_df = display_df.style.apply(highlight_top_teams, axis=1)
st.dataframe(styled_df, use_container_width=True, height=600)

st.caption("🟢 Green: Qualified for Round of 16 | 🟡 Yellow: Playoff Round | 🔴 Red: Eliminated")

st.markdown("---")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Points Comparison")
    fig_points = px.bar(
        df.head(10),
        x='Team',
        y='Points',
        color='Points',
        color_continuous_scale='Blues',
        title='Top 10 Teams by Points'
    )
    fig_points.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_points, use_container_width=True)

with col2:
    st.subheader("⚽ Goal Difference")
    fig_gd = px.bar(
        df.head(10),
        x='Team',
        y='Goal_Difference',
        color='Goal_Difference',
        color_continuous_scale='RdYlGn',
        title='Top 10 Teams by Goal Difference'
    )
    fig_gd.update_layout(xaxis_tickangle=-45, showlegend=False)
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
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

if show_form:
    st.markdown("---")
    st.subheader("📈 Recent Form (Last 5 Matches)")
    
    form_col1, form_col2 = st.columns([2, 1])
    
    with form_col1:
        form_df = df[['Team', 'Recent_Form']].head(10)
        st.dataframe(form_df, use_container_width=True, height=400)
    
    with form_col2:
        st.info("""
        **Form Guide:**
        - W: Win
        - D: Draw
        - L: Loss
        
        Showing the last 5 matches for each team from left to right (oldest to newest).
        """)

# Auto-refresh
st.session_state.last_update = current_time
time.sleep(refresh_rate)
st.rerun()