import streamlit as st
import pickle
import pandas as pd
import time

# Step 1: Set up session state for splash video
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False

# Step 2: Splash screen logic
if not st.session_state.show_main_app:
    st.set_page_config(page_title="IPL Victory Predictor", layout="wide")
    st.markdown("""
        <style>
        .video-container {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 9999;
            background-color: black;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        </style>
        <div class="video-container">
            <video id="introVideo" autoplay muted>
                <source src="/static/intro_clip.mp4" type="video/mp4">
            </video>
        </div>
        <script>
            const video = document.getElementById("introVideo");
            video.onended = function() {
                window.location.reload();
            }
        </script>
    """, unsafe_allow_html=True)

    time.sleep(7)  # Adjust based on video length
    st.session_state.show_main_app = True
    st.experimental_rerun()
    st.stop()

# Step 3: Main App Logic Starts Here

# Set page configuration
st.set_page_config(page_title="IPL Victory Predictor", layout="wide")

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

# Custom Styling
st.markdown(
    """
    <style>
    body {
        background-color: black;
    }
    .big-text {
        font-size: 70px !important;
        font-weight: bold;
        text-align: center;
        color: white;
        margin-top: 20px;
    }
    .small-text {
        font-size: 24px;
        text-align: center;
        color: white;
    }
    .title-text {
        font-size: 60px !important;
        font-weight: bold;
        text-align: left;
        color: white;
        margin-top: 50px;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4500;
        color: white;
        font-size: 20px;
        padding: 10px;
        border-radius: 8px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D84315;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Heading
st.markdown("<p class='big-text'>Can't Tell a Yorker from a Googly? We Got Your IPL Predictions Covered</p>", unsafe_allow_html=True)
st.markdown("<p class='small-text'>Dominate your fantasy league and win big with our winning strategies</p>", unsafe_allow_html=True)

# Image Path Handling for Top Image
top_image_path = "images/ipl_players.jpeg" 
st.image(top_image_path, use_container_width=True)

# Add a Large Gap for Scrolling Effect
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Title
st.markdown("<p class='title-text'>IPL VICTORY PREDICTOR</p>", unsafe_allow_html=True)

# Layout: Left - Input Fields | Right - IPL Trophy Image
col1, col2 = st.columns(2)  

with col1:  
    batting_team = st.selectbox('Select the batting team', sorted(teams), key="batting_team")
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), key="bowling_team")
    selected_city = st.selectbox('Select the host city', sorted(cities), key="city")
    target = st.number_input('Target', min_value=1, key="target")
    score = st.number_input('Score', min_value=0, key="score")
    overs = st.number_input('Overs completed', min_value=0.0, max_value=20.0, step=0.1, key="overs")
    wickets = st.number_input('Wickets fallen', min_value=0, max_value=10, key="wickets")

# Right Side: IPL Trophy Image
with col2:
    trophy_image_path = "images/ipl_trophy.jpeg"
    st.image(trophy_image_path, use_container_width=True)

# Predict Button - Aligned and Styled
with col1:
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
