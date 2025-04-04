import streamlit as st
import pickle
import pandas as pd
import base64
import os

# Set page configuration
st.set_page_config(page_title="IPL Victory Predictor", layout="wide")

# Function to play local MP4 splash screen
def autoplay_video(file_path):
    with open(file_path, "rb") as video_file:
        video_bytes = video_file.read()
        encoded = base64.b64encode(video_bytes).decode()
        video_html = f"""
        <style>
        .video-container {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 100vw;
            background-color: black;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        video {{
            height: 100%;
            width: 100%;
            object-fit: cover;
        }}
        </style>
        <div class="video-container">
            <video autoplay muted onended="parent.postMessage('video_done', '*')">
                <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
            </video>
        </div>
        <script>
        window.addEventListener('message', (event) => {{
            if (event.data === 'video_done') {{
                window.location.reload();
            }}
        }});
        </script>
        """
        st.markdown(video_html, unsafe_allow_html=True)

def main():
    # Splash screen logic
    if 'splash_shown' not in st.session_state:
        autoplay_video("videos/intro_clip.mp4")
        st.session_state.splash_shown = True
        st.stop()

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

    # Top Image
    top_image_path = "images/ipl_players.jpeg" 
    st.image(top_image_path, use_container_width=True)

    # Add vertical spacing
    st.markdown("<br>" * 14, unsafe_allow_html=True)

    # Title
    st.markdown("<p class='title-text'>IPL VICTORY PREDICTOR</p>", unsafe_allow_html=True)

    # Layout
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
        trophy_image_path = "images/ipl_trophy.jpeg"
        st.image(trophy_image_path, use_container_width=True)

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

if __name__ == "__main__":
    # Needed for Render to find and run the app
    port = int(os.environ.get("PORT", 8501))
    st._is_running_with_streamlit = True  # Workaround for streamlit CLI check
    main()
