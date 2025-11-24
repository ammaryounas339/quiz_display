import streamlit as st
import json
import os

# --- CONFIGURATION ---
QUIZ_DATA_PATH = "quiz_data.json"
BASE_IMAGE_PATH = "indicator_explainer_images"

# Map indicators to their specific image filenames
# UPDATED: Supports lists for multiple images
INDICATOR_IMAGE_MAP = {
    "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand. Grade 6 - Math": [
        "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand..jpg",
        "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand1.jpg"
    ],
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms. Grade 6 - Math": [
        "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms..jpg",
        "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms1.jpg"
    ],
    "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers. Grade 6 - Math": [
        "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers..jpg",
        "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers1..jpg"
    ],
    "4. Comparing and ordering numbers up to four digits using symbols (>, <, =) in ascending and descending order. Grade 6 - Math": [
        "4. Comparing and ordering numbers up to four digits using symbols (>, <, =) in ascending and descending order..jpg"
    ]
}

# --- HELPER FUNCTIONS ---
def load_quiz_data():
    if not os.path.exists(QUIZ_DATA_PATH):
        st.error(f"Quiz data file not found: {QUIZ_DATA_PATH}")
        return {}
    try:
        with open(QUIZ_DATA_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading quiz data: {e}")
        return {}

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="AI Quiz Viewer", layout="wide")
    
    st.title("🤖 AI-Generated Quiz Viewer")
    st.caption("Reviewing novel practice questions generated from visual learning aids.")
    st.divider()

    quiz_data = load_quiz_data()

    if not quiz_data:
        st.warning("No quiz data found. Please run the generation script first.")
        return

    # Iterate through each indicator in the JSON file
    for indicator_name, quiz_content in quiz_data.items():
        with st.container():
            st.subheader(f"Indicator: {indicator_name}")
            
            # --- 1. Display Visual Learning Aids (Images) ---
            image_files = INDICATOR_IMAGE_MAP.get(indicator_name)
            
            if image_files:
                # Normalize to list if it's a single string
                if isinstance(image_files, str):
                    image_files = [image_files]
                
                # Create columns for images
                cols = st.columns(len(image_files))
                for idx, img_file in enumerate(image_files):
                    full_path = os.path.join(BASE_IMAGE_PATH, img_file)
                    with cols[idx]:
                        if os.path.exists(full_path):
                            st.image(full_path, caption=f"Visual Aid {idx+1}", use_container_width=True)
                        else:
                            st.warning(f"Image not found: {img_file}")
            else:
                st.info("No specific images mapped for this indicator.")

            # --- 2. Display Generated Questions ---
            st.markdown("### 📝 Generated Practice Questions")
            
            for i, q in enumerate(quiz_content['questions']):
                with st.expander(f"Question {i+1}: {q['question_text'][:50]}...", expanded=True):
                    st.markdown(f"**{q['question_text']}**")
                    
                    # Display Options
                    for opt in q['options']:
                        st.write(f"- **{opt['label']}**: {opt['text']}")
                    
                    # Answer Section
                    st.markdown("---")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.success(f"Correct: **{q['correct_option_label']}**")
                    with col2:
                        st.info(f"**Reasoning:** {q['explanation']}")
            
            st.divider() # Separator between indicators

if __name__ == "__main__":
    main()