import streamlit as st
import os
from PIL import Image
import pandas as pd
import json
from grid import show_masonry_grid

SAMPLE_TITLES = {
    1: "Angel Woman",
    2: "Saint In Mountains",
    3: "Blue Hair Anime Girl",
    4: "Girl In Field",
    5: "Double Starship",
    6: "Bright Jumble Woman",
    7: "Cherub",
    8: "Praying In Garden",
    9: "Tropical Garden",
    10: "Ancient Gate",
    11: "Green Hills",
    12: "Bucolic Scene",
    13: "Anime Girl In Black",
    14: "Fancy Car",
    15: "Greek Temple",
    16: "String Doll",
    17: "Angry Crosses",
    18: "Rainbow Girl",
    19: "Creepy Skull",
    20: "Leafy Lane",
    21: "Ice Princess",
    22: "Celestial Display",
    23: "Mother And Child",
    24: "Fractured Lady",
    25: "Giant Ship",
    26: "Muscular Man",
    27: "Minaret Boat",
    28: "Purple Squares",
    29: "People Sitting",
    30: "Girl In White",
    31: "Riverside Cafe",
    32: "Serene River",
    33: "Turtle House",
    34: "Still Life",
    35: "Wounded Christ",
    36: "White Blob",
    37: "Weird Bird",
    38: "Ominous Ruin",
    39: "Vague Figures",
    40: "Dragon Lady",
    41: "White Flag",
    42: "Woman Unicorn",
    43: "Rooftops",
    44: "Paris Scene",
    45: "Pretty Lake",
    46: "Landing Craft",
    47: "Flailing Limbs",
    48: "Colorful Town",
    49: "Mediterranean Town",
    50: "Punk Robot"
}

SAMPLE_ANSWERS = {
    1: "human",    # Angel Woman
    2: "human",    # Saint In Mountains
    3: "human",    # Blue Hair Anime Girl
    4: "ai",       # Girl In Field
    5: "human",    # Double Starship
    6: "ai",       # Bright Jumble Woman
    7: "ai",       # Cherub
    8: "human",    # Praying In Garden
    9: "human",    # Tropical Garden
    10: "ai",      # Ancient Gate
    11: "ai",      # Green Hills
    12: "human",   # Bucolic Scene
    13: "ai",      # Anime Girl In Black
    14: "human",   # Fancy Car
    15: "human",   # Greek Temple
    16: "ai",      # String Doll
    17: "ai",      # Angry Crosses
    18: "human",   # Rainbow Girl
    19: "human",   # Creepy Skull
    20: "ai",      # Leafy Lane
    21: "ai",      # Ice Princess
    22: "human",   # Celestial Display
    23: "ai",      # Mother And Child
    24: "ai",      # Fractured Lady
    25: "human",   # Giant Ship
    26: "ai",      # Muscular Man
    27: "ai",      # Minaret Boat
    28: "human",   # Purple Squares
    29: "human",   # People Sitting
    30: "human",   # Girl In White
    31: "ai",      # Riverside Cafe
    32: "human",   # Serene River
    33: "ai",      # Turtle House
    34: "ai",      # Still Life
    35: "human",   # Wounded Christ
    36: "human",   # White Blob
    37: "ai",      # Weird Bird
    38: "ai",      # Ominous Ruin
    39: "human",   # Vague Figures
    40: "ai",      # Dragon Lady
    41: "human",   # White Flag
    42: "human",   # Woman Unicorn
    43: "ai",      # Rooftops
    44: "ai",      # Paris Scene
    45: "ai",      # Pretty Lake
    46: "ai",      # Landing Craft
    47: "human",   # Flailing Limbs
    48: "human",   # Colorful Town
    49: "ai",      # Mediterranean Town
    50: "ai"       # Punk Robot
}

def calculate_scores(user_answers, correct_answers):
    """Calculate various scoring metrics"""
    total_questions = len(correct_answers)
    correct_count = sum(1 for q, ans in user_answers.items() 
                       if ans == correct_answers[q])
    
    # Separate AI and Human scores
    ai_questions = {q: ans for q, ans in correct_answers.items() if ans == "ai"}
    human_questions = {q: ans for q, ans in correct_answers.items() if ans == "human"}
    
    ai_correct = sum(1 for q in ai_questions.keys() 
                    if q in user_answers and user_answers[q] == "ai")
    human_correct = sum(1 for q in human_questions.keys() 
                       if q in user_answers and user_answers[q] == "human")
    
    return {
        "total_score": (correct_count / total_questions) * 100,
        "ai_score": (ai_correct / len(ai_questions)) * 100 if ai_questions else 0,
        "human_score": (human_correct / len(human_questions)) * 100 if human_questions else 0,
        "total_correct": correct_count,
        "ai_correct": ai_correct,
        "human_correct": human_correct
    }

def show_landing_page():
    """Display the enhanced landing page with attribution"""
    st.markdown("""
        <style>
        .centered {
            text-align: center;
            padding: 0 15%;
        }
        .big-title {
            font-size: 3em;
            margin-bottom: 1em;
        }
        .description {
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 2em;
        }
        .highlight {
            color: #FF4B4B;
            font-weight: bold;
        }
        .attribution {
            font-size: 1em;
            font-style: italic;
            margin-bottom: 2em;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="centered">', unsafe_allow_html=True)
        st.markdown('<h1 class="big-title">Welcome to the AI Art Turing Test</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="description">
        Can you tell the difference between <span class="highlight">AI-generated</span> and 
        <span class="highlight">human-created</span> artwork? \n
        You will be shown 50 images one at a time. For each image, you need to decide whether 
        it was created by AI or created by a human artist. \n
        Ready to begin?
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="attribution">
        Based on <a href="https://www.astralcodexten.com/p/ai-art-turing-test" target="_blank" 
        class="hover:underline">Scott Alexander's AI Art Turing Test</a>. 
        Unlike the original Google Form, this version scores you automatically
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        button_col1, button_col2, button_col3 = st.columns([1,1,1])
        with button_col2:
            if st.button("Start Test", use_container_width=True):
                st.session_state.current_question = 1
                st.session_state.show_quiz = True
                st.rerun()
def show_question_page(question_number):
    """Display an enhanced question page with improved layout and navigation"""
    st.markdown("""
        <style>
        .image-title {
            color: var(--text-color);
            font-size: 1.8em;
            text-align: center;
            margin: 0.5rem 0 1rem 0;
            font-weight: 600;
        }
        
        .progress-indicator {
            color: var(--text-color);
            font-size: 0.9em;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .progress-bar {
            height: 4px;
            background-color: var(--secondary-background-color);
            border-radius: 2px;
            margin: 0 auto 1.5rem auto;
            max-width: 400px;
        }
        
        .progress-bar-fill {
            height: 100%;
            background-color: #FF4B4B;
            border-radius: 2px;
            transition: width 0.3s ease;
        }
        
        .image-container {
            margin: 0 auto;
            padding: 10px;
            border-radius: 10px;
            background: var(--background-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                        0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .choice-container {
            margin: 20px auto;
            max-width: 800px;
            text-align: center;
        }
        
        .nav-button {
            background-color: #4A4A4A;
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            font-size: 0.9em;
        }
        
        .nav-button:hover {
            background-color: #333333;
        }
        
        .choice-button {
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            margin: 0 0.5rem;
        }
        
        .choice-button:hover {
            background-color: #FF3333;
        }
        
        .choice-button.selected {
            background-color: #2E7D32;
        }
        
        .submit-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            margin-top: 1rem;
        }
        
        .submit-button:hover {
            background-color: #45a049;
        }

        /* Center buttons vertically */
        [data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Image title
    st.markdown(f"""
        <div class="image-title">{SAMPLE_TITLES[question_number]}</div>
    """, unsafe_allow_html=True)

    # Progress indicator and bar
    progress = (len(st.session_state.user_answers) / 50) * 100
    st.markdown(f"""
        <div class="progress-indicator">{question_number}/50</div>
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress}%;"></div>
        </div>
    """, unsafe_allow_html=True)

    # Image display
    try:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(os.path.join("images", f"{question_number}.png"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    # Human + AI Button
    col1, col2 = st.columns([1, 1])
    
    # Human button
    with col1:
        current_answer = st.session_state.user_answers.get(question_number, None)
        human_selected = current_answer == "human"
        if st.button("Human", key="human", use_container_width=True,
                    type="primary" if human_selected else "secondary"):
            st.session_state.user_answers[question_number] = "human"
            if question_number < 50:
                st.session_state.current_question += 1
            st.rerun()

    # AI button
    with col2:
        ai_selected = current_answer == "ai"
        if st.button("AI", key="ai", use_container_width=True,
                    type="primary" if ai_selected else "secondary"):
            st.session_state.user_answers[question_number] = "ai"
            if question_number < 50:
                st.session_state.current_question += 1
            st.rerun()
    # Other buttons
    col1, col2, col3 = st.columns([1, 3, 1])

    # Previous button
    with col1:
        if question_number > 1:
            if st.button("←", key="prev", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()

    # Next button
    with col3:
        if question_number < 50 and len(st.session_state.user_answers) >= st.session_state.current_question:
            if st.button("→", key="next", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()

    # Submit button (centered, only shows when all questions are answered)
    if len(st.session_state.user_answers) == 50:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("See Results", key="submit", use_container_width=True,
                        type="primary"):
                st.session_state.quiz_complete = True
                st.rerun()

def show_results_page():
    """Display enhanced results page with optimized image grid"""
    st.markdown("""
        <style>
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-bottom: 3rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        .metric-card {
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #FF4B4B;
        }
        
        .metric-label {
            font-size: 1em;
            opacity: 0.8;
        }

        /* Custom styling for the image grid */
        .stImage {
            position: relative;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stImage > img {
            width: 100% !important;
            height: 150px !important;  /* Fixed height for thumbnails */
            object-fit: cover !important;
            border-radius: 4px !important;
        }

        /* Remove default column gaps */
        .row-widget.stHorizontal {
            gap: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="results-header">', unsafe_allow_html=True)
    st.title("🎯 Quiz Results")
    st.markdown('</div>', unsafe_allow_html=True)

    scores = calculate_scores(st.session_state.user_answers, SAMPLE_ANSWERS)
    
    # Display metrics
    st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{scores['total_score']:.1f}%</div>
                <div class="metric-label">Overall Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{scores['ai_score']:.1f}%</div>
                <div class="metric-label">AI Detection</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{scores['human_score']:.1f}%</div>
                <div class="metric-label">Human Detection</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Detailed results table
    st.subheader("Detailed Results")
    results_data = []
    for q_num in range(1, 51):
        results_data.append({
            "Image": q_num,
            "Title": SAMPLE_TITLES[q_num],
            "Actual": SAMPLE_ANSWERS[q_num].upper(),
            "Your Answer": st.session_state.user_answers[q_num].upper(),
            "Correct?": "✅" if SAMPLE_ANSWERS[q_num] == st.session_state.user_answers[q_num] else "❌"
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, use_container_width=True)
    # Image grid
    with open('image_cache.json') as f:
        image_data = json.load(f)
    
    show_masonry_grid(
        images=list(range(1, 51)),  
        titles=SAMPLE_TITLES,
        answers=SAMPLE_ANSWERS,
        user_answers=st.session_state.user_answers,
        image_data=image_data,
        key="results_grid"
    )

    # Center the restart button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Take Quiz Again", use_container_width=True):
            st.session_state.current_question = 1
            st.session_state.user_answers = {}
            st.session_state.quiz_complete = False
            st.session_state.show_quiz = False
            st.rerun()

def main():
    st.set_page_config(page_title="AI Art Turing Test", layout="wide")
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'show_quiz' not in st.session_state:
        st.session_state.show_quiz = False

    if not st.session_state.show_quiz and not st.session_state.quiz_complete:
        show_landing_page()
    elif not st.session_state.quiz_complete:
        show_question_page(st.session_state.current_question)
    else:
        show_results_page()

if __name__ == "__main__":
    main()