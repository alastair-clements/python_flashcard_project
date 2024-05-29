import streamlit as st
import pandas as pd
import json
import random
import os

# Load flashcard data from JSON file
def load_flashcards():
    try:
        with open('flashcards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Flashcards data file not found. Please ensure 'flashcards.json' is in the same directory as this script.")
        return []

flashcards = load_flashcards()

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 1
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False

# Function to display flashcard
def display_flashcard(index):
    card = flashcards[index]
    st.write(f"**Description:** {card['description']}")
    st.write(f"**Example:** `{card['example']}`")

# UI elements
st.title("Pandas Flashcards")
st.write("Learn the most important functions in pandas.")

if flashcards:
    # Difficulty filter
    difficulty = st.slider("Select difficulty level", 1, 3, 1)
    st.session_state.difficulty = difficulty

    # Filter flashcards by difficulty
    filtered_flashcards = [card for card in flashcards if card['difficulty'] == difficulty]

    if not filtered_flashcards:
        st.write("No flashcards available for the selected difficulty level.")
    else:
        card = filtered_flashcards[st.session_state.index % len(filtered_flashcards)]
        display_flashcard(st.session_state.index % len(filtered_flashcards))

        # Input for the function name
        user_input = st.text_input("Enter the function name (e.g., pd.read_csv):")

        if st.button("Submit"):
            if user_input == card['function']:
                st.success("Correct!")
            else:
                st.error("Incorrect. Try again!")

        # Show hint
        if st.button("Hint"):
            st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            options = random.sample([c['function'] for c in flashcards], 5)
            if card['function'] not in options:
                options[0] = card['function']
            random.shuffle(options)
            st.write("Possible answers:")
            for option in options:
                st.write(option)

        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Previous"):
                st.session_state.index -= 1
                if st.session_state.index < 0:
                    st.session_state.index = len(filtered_flashcards) - 1
                st.session_state.show_hint = False

        with col3:
            if st.button("Next"):
                st.session_state.index += 1
                if st.session_state.index >= len(filtered_flashcards):
                    st.session_state.index = 0
                st.session_state.show_hint = False

        st.write(f"Flashcard {st.session_state.index + 1} of {len(filtered_flashcards)}")
else:
    st.write("No flashcards available. Please check the flashcards.json file.")
