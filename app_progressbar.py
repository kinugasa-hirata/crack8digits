import streamlit as st
import random
import time

def generate_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def crack_number(target, progress_bar):
    start_time = time.time()
    total_possibilities = 100_000_000  # 10^8 possibilities
    for guess in range(total_possibilities):
        if guess % 1000000 == 0:  # Update progress every million attempts
            progress = guess / total_possibilities
            progress_bar.progress(progress)
        if f"{guess:08d}" == target:
            end_time = time.time()
            progress_bar.progress(1.0)  # Complete the progress bar
            return guess, end_time - start_time
    return None, None

st.title("8-Digit Number Generator and Cracker")

if 'number' not in st.session_state:
    st.session_state.number = None
    st.session_state.hidden = False
    st.session_state.cracking = False
    st.session_state.cracked = False
    st.session_state.time_taken = None

col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Random Number"):
        st.session_state.number = generate_number()
        st.session_state.hidden = False
        st.session_state.cracked = False
        st.session_state.time_taken = None

with col2:
    if st.button("Hide/Show Number"):
        st.session_state.hidden = not st.session_state.hidden

if st.session_state.number:
    if st.session_state.hidden:
        st.write("Number: XXXXXXXX")
    else:
        st.write(f"Number: {st.session_state.number}")

col3, col4 = st.columns(2)
with col3:
    if st.button("Start Cracking"):
        st.session_state.cracking = True

with col4:
    if st.button("Stop Cracking"):
        st.session_state.cracking = False

if st.session_state.cracking and st.session_state.number and not st.session_state.cracked:
    progress_bar = st.progress(0)
    cracked_number, time_taken = crack_number(st.session_state.number, progress_bar)
    if cracked_number is not None:
        st.session_state.cracked = True
        st.session_state.time_taken = time_taken
        st.success(f"Number cracked: {cracked_number}")
        st.info(f"Time taken: {time_taken:.2f} seconds")
    else:
        st.error("Failed to crack the number")
    st.session_state.cracking = False

if st.session_state.cracked:
    st.write(f"Cracked number: {st.session_state.number}")
    st.write(f"Time taken: {st.session_state.time_taken:.2f} seconds")