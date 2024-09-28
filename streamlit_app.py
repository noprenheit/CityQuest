import streamlit as st
import json
import random

# read and load the city data from the JSON file
with open('city.json', 'r', encoding='utf-8') as f:
    city_data = json.load(f)

# session state variables
if 'streak' not in st.session_state:
    st.session_state.streak = 0

if 'final_streak' not in st.session_state:
    st.session_state.final_streak = 0

if 'country' not in st.session_state:
    st.session_state.country = None

if 'cities' not in st.session_state:
    st.session_state.cities = None

if 'guessed_countries' not in st.session_state:
    st.session_state.guessed_countries = set()

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# New session state variables
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False

if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ''

if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ''

# Initialize the reset flag
if 'reset_user_answer' not in st.session_state:
    st.session_state.reset_user_answer = False

def new_country():
    remaining_countries = list(set(city_data.keys()) - st.session_state.guessed_countries)
    if not remaining_countries:
        st.write("🎉 Congratulations! You've guessed all the countries!")
        st.session_state.game_over = True
        return
    st.session_state.country = random.choice(remaining_countries)
    st.session_state.cities = city_data[st.session_state.country]
    st.session_state.guessed_countries.add(st.session_state.country)


# Start the game or pick a new country
if st.session_state.country is None and not st.session_state.game_over:
    new_country()

st.title("🌍 City Quest 🌍")
if not st.session_state.game_over:
    st.write(f"Cities: **{', '.join(st.session_state.cities)}**")
    st.write(f"Current Streak: **{st.session_state.streak}**")

    # Reset 'user_answer' before the text_input is instantiated
    if st.session_state.get('reset_user_answer', False):
        st.session_state.user_answer = ''
        st.session_state.reset_user_answer = False  # Reset the flag

    user_answer = st.text_input("Can you guess the country from these five cities?:", key='user_answer')

    if not st.session_state.answer_submitted:
        if st.button("Submit"):
            st.session_state.answer_submitted = True
            if user_answer.strip().lower() == st.session_state.country.strip().lower():
                st.session_state.feedback_message = "✅ Correct!"
                st.session_state.streak += 1
            else:
                st.session_state.final_streak = st.session_state.streak
                st.session_state.streak = 0
                st.session_state.game_over = True
                st.session_state.feedback_message = f"❌ Wrong! The correct answer was **{st.session_state.country}**."

            st.rerun()

    # After submitting, display feedback and Next Question button
    if st.session_state.answer_submitted and not st.session_state.game_over:
        # Display the feedback message
        if st.session_state.feedback_message:
            st.write(st.session_state.feedback_message)

        def reset_user_answer():
            st.session_state.reset_user_answer = True  # Set the flag instead of resetting directly

        if st.button("Next Question", on_click=reset_user_answer):
            # Prepare for the next round
            st.session_state.country = None
            st.session_state.answer_submitted = False
            st.session_state.feedback_message = ''
            st.rerun()

else:
    if st.session_state.feedback_message:
        st.write(st.session_state.feedback_message)
    st.write(f"Your final streak: **{st.session_state.final_streak}**")

# Add a reset button
if st.button("Reset Game"):
    st.session_state.streak = 0
    st.session_state.final_streak = 0
    st.session_state.country = None
    st.session_state.cities = None
    st.session_state.guessed_countries = set()
    st.session_state.game_over = False
    st.session_state.answer_submitted = False
    st.session_state.feedback_message = ''
    st.session_state.reset_user_answer = True  # Set the flag instead of resetting directly
    st.rerun()
