import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd

# Ensure page config is set
st.set_page_config(page_title="IPL Victory Predictor", layout="wide")

# ---- SESSION STATE TO HANDLE INTRO ---- #
if 'intro_done' not in st.session_state:
    st.session_state.intro_done = False

# ---- INTRO PAGE ---- #
if not st.session_state.intro_done:
    st.markdown("<style>body { background-color: black; }</style>", unsafe_allow_html=True)

    # HTML: Video with Skip button + JS
    html_code = """
    <video id="introVideo" width="100%" autoplay>
      <source src="/static/intro_clip.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <br><br>
    <div style="text-align:center;">
      <button onclick="skipIntro()" style="padding: 12px 24px; font-size: 18px; background-color: #FF4500; color: white; border: none; border-radius: 8px; cursor: pointer;">
        Skip Intro
      </button>
    </div>

    <script>
      var video = document.getElementById('introVideo');
      video.onended = function() {
          window.parent.postMessage("intro_done", "*");
      };

      function skipIntro() {
          window.parent.postMessage("intro_done", "*");
      }
    </script>
    """
    components.html(html_code, height=400)

    # JS Listener to set session state
    st.markdown("""
    <script>
    window.addEventListener("message", (event) => {
        if (event.data === "intro_done") {
            document.cookie = "intro=done";
            parent.window.location.reload();
        }
    });
    </script>
    """, unsafe_allow_html=True)

    st.stop()

# ---- MAIN APP AFTER INTRO ---- #
st.session_state.intro_done = True

# Load model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define teams and cities
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

# Headings and Image
st.markdown("<p class='big-text'>Can't Tell a Yorker from a Googly? We Got Your IPL Predictions Covered</p>", unsafe_allow_html=True)
st.markdown("<p class='small-text'>Dominate your fantasy league and win big with our winning strategies</p>", unsafe_allow_html=True)
st.image("images/ipl_players.jpeg", use_container_width=True)
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("<p class='title-text'>IPL VICTORY PREDICTOR</p>", unsafe_allow_html=True)

# Input Form
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), key="batting_team")
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), key="bowling_team")
    selected_city = st.selectbox('Select the host city', sorted(cities), key="city")
    target = st.number_input('Target', min_value=1, key="target")
    score = st.number_input('Score', min_value=0, key="score")
    overs = st.number_input('Overs completed', min_value=0.0, max_value=20.0, step=0.1, key="overs")
    wickets = st.number_input('Wickets fallen', min_value=0, max_value=10, key="wickets")

with col2:
    st.image("images/ipl_trophy.jpeg", use_container_width=True)

# Prediction Logic
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

            result = pipe.predict_proba(input_df)
            loss_prob = result[0][0]
            win_prob = result[0][1]

            st.markdown(f"<h2 style='text-align: left; color: #FF4500;'>{batting_team} - {round(win_prob * 100)}%</h2>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: left; color: #FF4500;'>{bowling_team} - {round(loss_prob * 100)}%</h2>", unsafe_allow_html=True)
