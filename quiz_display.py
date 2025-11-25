import streamlit as st
import json
import os

# --- CONFIGURATION ---
BASE_IMAGE_PATH = "indicator_explainer_images"

# Map indicators to their specific image filenames
INDICATOR_IMAGE_MAP = {
    "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand.": [
        "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand..jpg",
        "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand1.jpg"
    ],
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": [
        "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms..jpg",
        "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms1.jpg"
    ],
    "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers.": [
        "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers..jpg",
        "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers1..jpg"
    ],
    "4. Comparing and ordering numbers up to four digits using symbols (>, <, =) in ascending and descending order.": [
        "4. Comparing and ordering numbers up to four digits using symbols (>, <, =) in ascending and descending order..jpg"
    ]
}

# --- HELPER FUNCTIONS ---
def load_quiz_data(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return {}

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="AI Quiz Viewer", layout="wide")
    
    st.title("🤖 AI-Generated Quiz Viewer")
    st.markdown("Compare generation strategies for creating practice questions from visual learning aids.")
    st.divider()
    
    # --- Sidebar Controls ---
    st.sidebar.header("Configuration")
    
    data_source = st.sidebar.radio(
        "Select Generation Batch:",
        ("Batch A: Questions not referring to the image", "Batch B: Questions referring to each image like 'Look at the image and answer this'"),
        index=1
    )
    
    # Determine file path based on selection
    if "Batch A" in data_source:
        selected_file = "quiz_data.json"
        st.sidebar.info("Showing questions directly generated for the INDICATOR as a whole concept (not specifically tied to images).")
        batch_mode = "A"
    else:
        selected_file = "quiz_data_new.json"
        st.sidebar.info("Showing questions generated specifically for EACH image, referencing the visual aid directly.")
        batch_mode = "B"

    # --- Load Data ---
    quiz_data = load_quiz_data(selected_file)

    if quiz_data is None:
        st.error(f"File not found: `{selected_file}`. Please ensure the file exists in the directory.")
        return
    
    if not quiz_data:
        st.warning("Quiz data is empty or invalid.")
        return

    # --- Render Content ---
    for indicator_name, quiz_content in quiz_data.items():
        with st.container():
            st.subheader(f"📌 Indicator: {indicator_name}")
            
            image_files = INDICATOR_IMAGE_MAP.get(indicator_name)
            if isinstance(image_files, str): image_files = [image_files]
            
            questions = quiz_content.get('questions', [])
            
            # --- BATCH A RENDERING (Images then Questions) ---
            if batch_mode == "A":
                # 1. Show ALL Images first
                if image_files:
                    cols = st.columns(len(image_files))
                    for idx, img_file in enumerate(image_files):
                        with cols[idx]:
                            st.markdown(f"**Visual Learning Aid {idx + 1}**")
                            full_path = os.path.join(BASE_IMAGE_PATH, img_file)
                            if os.path.exists(full_path):
                                st.image(full_path, use_container_width=True)
                            else:
                                st.warning(f"Image not found: {img_file}")
                
                # 2. Show ALL Questions below
                st.markdown("### 📝 Practice Questions")
                if not questions:
                    st.info("No questions found in this batch.")
                else:
                    for q_idx, q in enumerate(questions):
                        with st.expander(f"**Q{q_idx + 1}:** {q['question_text'][:60]}...", expanded=True):
                            st.write(q['question_text'])
                            for opt in q['options']:
                                st.markdown(f"- **{opt['label']}**: {opt['text']}")
                            
                            if st.checkbox("Reveal Answer", key=f"{selected_file}_{indicator_name}_{q_idx}"):
                                st.success(f"Correct: {q['correct_option_label']}")
                                st.caption(f"**Explanation:** {q['explanation']}")

            # --- BATCH B RENDERING (Interleaved Vertical) ---
            else: 
                QUESTIONS_PER_IMAGE = 3
                
                if image_files:
                    for idx, img_file in enumerate(image_files):
                        # Container for each Image+Questions set
                        with st.container():
                            st.markdown(f"#### Context {idx + 1}")
                            
                            # 1. The Visual Aid
                            full_path = os.path.join(BASE_IMAGE_PATH, img_file)
                            if os.path.exists(full_path):
                                st.image(full_path, caption=f"Visual Aid for Questions Set {idx+1}", use_container_width=True)
                            else:
                                st.warning(f"Image not found: {img_file}")
                            
                            # 2. The Questions (Vertical list below image)
                            start_q = idx * QUESTIONS_PER_IMAGE
                            end_q = start_q + QUESTIONS_PER_IMAGE
                            current_batch = questions[start_q:end_q]
                            
                            if not current_batch:
                                st.info("No specific questions generated for this image in this batch.")
                            else:
                                for q_idx, q in enumerate(current_batch):
                                    global_q_num = start_q + q_idx + 1
                                    
                                    with st.expander(f"**Q{global_q_num}:** {q['question_text'][:60]}...", expanded=True):
                                        st.write(q['question_text'])
                                        for opt in q['options']:
                                            st.markdown(f"- **{opt['label']}**: {opt['text']}")
                                        
                                        if st.checkbox("Reveal Answer", key=f"{selected_file}_{indicator_name}_{global_q_num}"):
                                            st.success(f"Correct: {q['correct_option_label']}")
                                            st.caption(f"**Explanation:** {q['explanation']}")
                        
                        st.divider() 
                else:
                    st.info("No images mapped for this indicator.")

if __name__ == "__main__":
    main()
