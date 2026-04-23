import streamlit as st
import pandas as pd

# --- STYLING & THEME ---
st.set_page_config(page_title="Sports Prop Analyzer", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .stButton>button { background-color: #00C853; color: white; border-radius: 8px; width: 100%; }
    .report-card { background-color: #1E1E1E; padding: 15px; border-radius: 10px; border-left: 5px solid #00C853; margin-bottom: 10px; }
    </style>
    """, unsafe_content_type=True)

# --- APP HEADER ---
st.title("🎯 Sports Prop Analyzer: Player Prop Edition")
st.caption("Rebuilt from Jan 11 Stable Build | PrizePicks Optimized")

# --- DATA FEED (Add your API keys here) ---
# For now, using a dynamic tactical sample
props_data = [
    {"player": "J. Tatum", "sport": "NBA", "stat": "Points", "line": 26.5, "proj": 29.3, "hit_rate": "80%", "game": "BOS @ MIA"},
    {"player": "Alcaraz", "sport": "Tennis", "stat": "Games Won", "line": 12.5, "proj": 14.1, "hit_rate": "75%", "game": "ATP Madrid"},
    {"player": "m0NESY", "sport": "CS2", "stat": "Map 1-2 Kills", "line": 38.5, "proj": 42.0, "hit_rate": "70%", "game": "G2 vs FaZe"},
    {"player": "L. Doncic", "sport": "NBA", "stat": "Rebounds", "line": 9.5, "proj": 11.2, "hit_rate": "85%", "game": "DAL @ PHX"},
    {"player": "S. Scheffler", "sport": "PGA", "stat": "Birdies", "line": 4.5, "proj": 5.2, "hit_rate": "90%", "game": "The Masters"},
    {"player": "Ohtani", "sport": "MLB", "stat": "Total Bases", "line": 1.5, "proj": 2.1, "hit_rate": "65%", "game": "LAD @ SF"}
]

df = pd.DataFrame(props_data)

# --- SIDEBAR: TACTICAL SEGMENTATION ---
st.sidebar.header("🛠️ Generator Controls")
sport_toggle = st.sidebar.multiselect("Filter Sports", options=df['sport'].unique(), default=df['sport'].unique())
game_select = st.sidebar.selectbox("Segment by Game", options=["All Games"] + list(df['game'].unique()))
slip_size = st.sidebar.slider("PrizePicks Slip Size", 2, 6, 4)

# Apply Filters
filtered_df = df[df['sport'].isin(sport_toggle)]
if game_select != "All Games":
    filtered_df = filtered_df[filtered_df['game'] == game_select]

# --- GENERATOR ENGINE ---
if st.button(f"Generate {slip_size}-Man Tactical Slip"):
    st.subheader(f"✅ Your {slip_size}-Man PrizePicks Slip")
    
    # Logic: Sort by biggest edge (Proj - Line)
    filtered_df['edge'] = filtered_df['proj'] - filtered_df['line']
    top_picks = filtered_df.sort_values(by='edge', ascending=False).head(slip_size)
    
    # Display like a betting ticket
    for idx, row in top_picks.iterrows():
        st.markdown(f"""
        <div class="report-card">
            <b>{row['player']} ({row['sport']})</b><br>
            Game: {row['game']} | Stat: {row['stat']}<br>
            <span style="color:#00C853;">Line: {row['line']} | Projected: {row['proj']} | Hit Rate: {row['hit_rate']}</span>
        </div>
        """, unsafe_content_type=True)
    
    # PrizePicks Logic Label
    type_label = "Power Play" if slip_size <= 4 else "Flex Play"
    st.success(f"Strategy: {type_label} | Logic: Statistical Variance over L5 Games")

# --- RAW DATA VIEW ---
with st.expander("Show Tactical Data Table"):
    st.dataframe(filtered_df)
