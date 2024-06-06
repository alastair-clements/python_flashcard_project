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
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'submit_count' not in st.session_state:
    st.session_state.submit_count = 0

# Function to display flashcard
def display_flashcard(index):
    card = flashcards[index]
    st.markdown(f"### Description: {card['description']}")
    st.write(f"**Difficulty Level:** {card['difficulty']}")

# UI elements
st.title("Pandas Flashcards")
st.write("Learn the most important functions in pandas.")

if flashcards:
    card = flashcards[st.session_state.index % len(flashcards)]
    display_flashcard(st.session_state.index % len(flashcards))

    # Input for the function name
    user_input = st.text_input("Enter the function name (e.g., pd.read_csv):", key="user_input")

    if st.button("Submit"):
        st.session_state.submit_count += 1
        if user_input == card['function']:
            st.success("Correct!")
            st.session_state.correct_count += 1
        else:
            st.error("Incorrect. Try again!")

    # Display score
    st.write(f"Score: {st.session_state.correct_count} out of {st.session_state.submit_count}")

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous"):
            st.session_state.index -= 1
            if st.session_state.index < 0:
                st.session_state.index = len(flashcards) - 1
            st.session_state.show_hint = False
            st.experimental_rerun()

    with col3:
        if st.button("Next"):
            st.session_state.index += 1
            if st.session_state.index >= len(flashcards):
                st.session_state.index = 0
            st.session_state.show_hint = False
            st.experimental_rerun()

    # Spacing for hint buttons
    st.write("")
    st.write("")

    # Show hint
    if st.button("Hint"):
        st.session_state.show_hint = True

    if st.button("Hide Hint"):
        st.session_state.show_hint = False

    if st.session_state.show_hint:
        options = random.sample([c['function'] for c in flashcards], 5)
        if card['function'] not in options:
            options[0] = card['function']
        random.shuffle(options)
        st.write("Possible answers:")
        for option in options:
            st.write(option)
else:
    st.write("No flashcards available. Please check the flashcards.json file.")
