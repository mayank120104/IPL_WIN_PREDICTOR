import streamlit as st
import pickle
import pandas as pd
import time

# Set page configuration
st.set_page_config(page_title="IPL Victory Predictor", layout="wide")

# Session state to track if the intro was shown
if "intro_played" not in st.session_state:
    st.session_state.intro_played = False

# Show intro video if not played
if not st.session_state.intro_played:
    st.video("intro_clip.mp4")  # Ensure this file is in the correct location

    # JavaScript to automatically redirect after video ends (6 sec delay)
    st.markdown(
        """
        <script>
        setTimeout(function() {
            window.location.href = "?skip_intro=true";
        }, 6000);
        </script>
        """,
        unsafe_allow_html=True
    )

    # Button to skip intro
    if st.button("Skip Intro"):
        st.session_state.intro_played = True
        st.rerun()

    st.stop()  # Stop execution here so main content doesn't load yet

# Load the trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define Teams & Cities
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# Main Heading
st.markdown("<h1 style='text-align: center;'>IPL Victory Predictor</h1>", unsafe_allow_html=True)

# Image Path Handling for Top Image
st.image("images/ipl_players.jpeg", use_container_width=True)

# Title
st.markdown("<h2 style='text-align: left;'>IPL VICTORY PREDICTOR</h2>", unsafe_allow_html=True)

# Layout: Left - Input Fields | Right - IPL Trophy Image
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))
    selected_city = st.selectbox('Select the host city', sorted(cities))
    target = st.number_input('Target', min_value=1)
    score = st.number_input('Score', min_value=0)
    overs = st.number_input('Overs completed', min_value=0.0, max_value=20.0, step=0.1)
    wickets = st.number_input('Wickets fallen', min_value=0, max_value=10)

with col2:
    st.image("images/ipl_trophy.jpeg", use_container_width=True)

# Predict Button
if st.button('Predict'):
    if overs == 0:
        st.warning("Overs completed cannot be zero!")
    else:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        remaining_wickets = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        # Create Input DataFrame
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [remaining_wickets],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Predict using Model
        result = pipe.predict_proba(input_df)
        loss_prob = result[0][0]
        win_prob = result[0][1]

        # Display Results
        st.markdown(f"<h2 style='text-align: left; color: #FF4500;'>{batting_team} - {round(win_prob * 100)}%</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: left; color: #FF4500;'>{bowling_team} - {round(loss_prob * 100)}%</h2>", unsafe_allow_html=True)
