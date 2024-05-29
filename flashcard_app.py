import streamlit as st
from PIL import Image
import pandas as pd
import json

# Load flashcard data from JSON file
def load_flashcards():
    with open('flashcards.json', 'r') as f:
        return json.load(f)

flashcards = load_flashcards()

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 1

# Function to display flashcard
def display_flashcard(index):
    card = flashcards[index]
    st.write(f"### Function: {card['function']}")
    st.write(f"**Description:** {card['description']}")
    st.write(f"**Example:** `{card['example']}`")

# UI elements
st.title("Pandas Flashcards")
st.write("Learn the most important functions in pandas.")

# Difficulty filter
difficulty = st.slider("Select difficulty level", 1, 3, 1)
st.session_state.difficulty = difficulty

# Filter flashcards by difficulty
filtered_flashcards = [card for card in flashcards if card['difficulty'] == difficulty]

if not filtered_flashcards:
    st.write("No flashcards available for the selected difficulty level.")
else:
    # Display the current flashcard
    display_flashcard(st.session_state.index % len(filtered_flashcards))

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous"):
            st.session_state.index -= 1
            if st.session_state.index < 0:
                st.session_state.index = len(filtered_flashcards) - 1

    with col3:
        if st.button("Next"):
            st.session_state.index += 1
            if st.session_state.index >= len(filtered_flashcards):
                st.session_state.index = 0

    st.write(f"Flashcard {st.session_state.index + 1} of {len(filtered_flashcards)}")
