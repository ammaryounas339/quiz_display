import streamlit as st
import json
import os

# --- CONFIGURATION ---
BASE_IMAGE_PATH = "indicator_explainer_images"

# 1. Standard Images (For Batch A & B)
STANDARD_IMAGE_MAP = {
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

# 2. Gamified Images (For Batch C)
GAMIFIED_IMAGE_MAP = {
    "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand.": [
        "gamified_rounding_rollercoaster.png"
    ],
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": [
        "gamified_camel_caravan.png"
    ],
    "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers.": [
        "gamified_place_value_palace.png"
    ],
    "5. Computing the distance between two points in the coordinate plane, and finding the coordinates of the midpoint.": [
        "gamified_soccer_coordinate.png",
        "gamified_drone_delivery.png"
    ],
    "6. Utilizing the concept of percentage to determine a missing value when given two of the following: percentage, whole, and part.": [
        "gamified_file_download.png",
        "gamified_storage_usage.png"
    ]
}

# 3. Context Descriptions for Gamified Scenarios
SCENARIO_CONTEXT_MAP = {
    "gamified_rounding_rollercoaster.png": "Welcome to the Rounding Rollercoaster! Your goal is to predict where the carts will go. The track has 'peaks' at multiples of 10 or 100. If a cart hasn't reached the halfway point (the peak), gravity pulls it back. If it has passed the peak, it zooms forward to the next number.",
    
    "gamified_camel_caravan.png": "You are leading a desert caravan. The camels must walk in a specific order to deliver the correct message. The biggest camels carry the Thousands, and the smallest carry the Ones. Watch out for gaps in the line—a missing camel means a '0' in that place value!",
    
    "gamified_place_value_palace.png": "You are exploring the ancient Place Value Palace. To climb higher, you must combine your treasure. You can only step up to the next level if you trade exactly 10 items from your current level for 1 item on the level above.",
    
    "gamified_soccer_coordinate.png": "You are the team strategist analyzing the field. The pitch is laid out on a grid where the center circle is (0,0). Use the coordinates to calculate exactly how far the ball needs to travel and where the defenders are positioned to intercept it.",
    
    "gamified_drone_delivery.png": "You are piloting a delivery drone across the city grid. Your dashboard shows your start point at the Warehouse (0,0) and your destination. Use the linear flight path to calculate your exact battery needs, speed, and drop-off coordinates.",
    
    "gamified_file_download.png": "You are managing a large data transfer. The progress bar visually shows how much of the Total File (the Whole) has been completed. Use the filled section to estimate or calculate the exact GBs downloaded (the Part) based on the percentage shown.",
    
    "gamified_storage_usage.png": "Your phone is running out of space! The storage bar shows your Total Capacity and how much you have Used. Your task is to calculate the missing percentage number to see exactly how full your device is."
}

# 4. Metadata Map (Grade & Subject)
INDICATOR_META_MAP = {
    "1. Understanding place value and representing numbers using models, graphs, and number lines, rounding to the nearest ten, hundred, or thousand.": "Grade 3 - Math",
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": "Grade 3 - Math",
    "3. Counting number in ascending, descending, and jumping of (two, five, ten, hundred, and thousands), and determining even and odd numbers.": "Grade 3 - Math",
    "4. Comparing and ordering numbers up to four digits using symbols (>, <, =) in ascending and descending order.": "Grade 3 - Math",
    "5. Computing the distance between two points in the coordinate plane, and finding the coordinates of the midpoint.": "Grade 9 - Math",
    "6. Utilizing the concept of percentage to determine a missing value when given two of the following: percentage, whole, and part.": "Grade 9 - Math"
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
    st.markdown("Reviewing novel practice questions generated from visual learning aids.")
    st.divider()
    
    # --- Sidebar: Configuration ---
    st.sidebar.header("Configuration")
    data_source = st.sidebar.radio(
        "Select Generation Batch:",
        ("Batch A: Questions not referring to the image directly", 
         "Batch B: Questions referring to the image directly",
         "Batch C: Gamified/Scenario based approach"),
        index=2
    )
    
    # Configure variables based on selection
    if "Batch A" in data_source:
        selected_file = "quiz_data.json"
        active_image_map = STANDARD_IMAGE_MAP
        show_context = False
        st.sidebar.info("Questions not referring to the image directly but using it as a visual aid to generate new questions on the concepts defined in image")
    elif "Batch B" in data_source:
        selected_file = "quiz_data_new.json"
        active_image_map = STANDARD_IMAGE_MAP
        show_context = False
        st.sidebar.info("Questions referring to the image directly to generate questions like Look at the image and answer, what happens next etc.")
    else:
        selected_file = "quiz_data_gamified.json"
        active_image_map = GAMIFIED_IMAGE_MAP
        show_context = True
        st.sidebar.success("Gamified/Scenario based approach where each image represents a game scenario and questions are generated around that scenario. We can use cartoonish images for grade 3 and move towards real life images for grade 9.")

    # --- Load Data ---
    quiz_data = load_quiz_data(selected_file)

    if not quiz_data:
        st.warning(f"Data file `{selected_file}` not found or empty.")
        return

    # --- Render Content (Sequential List) ---
    for indicator_name, quiz_content in quiz_data.items():
        with st.container():
            # NEW: Get Grade/Subject Meta
            meta_info = INDICATOR_META_MAP.get(indicator_name, "Grade Unknown - Subject Unknown")
            
            # Display Header with Meta
            st.header(f"📌 {indicator_name}")
            st.caption(f"**{meta_info}**") # Display Grade/Subject here
            
            # Get images from the ACTIVE map (Standard or Gamified)
            image_files = active_image_map.get(indicator_name)
            
            # Normalize single string to list
            if isinstance(image_files, str): image_files = [image_files]
            
            questions = quiz_content.get('questions', [])
            
            # Determine how to split questions per image
            if image_files:
                # If we have images, split questions evenly among them
                qs_per_img = len(questions) // len(image_files) if len(questions) > 0 else 3
                if qs_per_img == 0: qs_per_img = len(questions) 
                
                for idx, img_file in enumerate(image_files):
                    st.subheader(f"Scenario {idx + 1}")
                    
                    # 1. Visual Aid (Full Width)
                    full_path = os.path.join(BASE_IMAGE_PATH, img_file)
                    if os.path.exists(full_path):
                        st.image(full_path, use_container_width=True)
                        
                        # Show Context Description
                        if show_context and img_file in SCENARIO_CONTEXT_MAP:
                            st.info(f"**Scenario Context:** {SCENARIO_CONTEXT_MAP[img_file]}")
                    else:
                        st.warning(f"Image not found: {img_file}")
                    
                    # 2. Questions (Below the image)
                    # Calculate slice indices
                    start_q = idx * qs_per_img
                    end_q = start_q + qs_per_img
                    
                    if idx == len(image_files) - 1:
                        end_q = len(questions)
                        
                    current_batch = questions[start_q:end_q]
                    
                    if not current_batch:
                        st.info("No specific questions generated for this image.")
                    else:
                        for q_idx, q in enumerate(current_batch):
                            global_q_num = start_q + q_idx + 1
                            with st.expander(f"**Q{global_q_num}**: {q['question_text'][:80]}...", expanded=True):
                                st.write(f"**{q['question_text']}**")
                                for opt in q['options']:
                                    st.markdown(f"- **{opt['label']}**: {opt['text']}")
                                
                                st.markdown("---")
                                st.success(f"Correct: **{q['correct_option_label']}**")
                                st.caption(f"*Reasoning: {q['explanation']}*")
            
            else:
                st.warning("No images mapped for this indicator in the selected configuration.")
                for i, q in enumerate(questions):
                    st.write(f"**Q{i+1}: {q['question_text']}**")
            
            st.divider()

if __name__ == "__main__":
    main()