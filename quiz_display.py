import streamlit as st
import json
import os

# --- CONFIGURATION ---
BASE_IMAGE_PATH = "indicator_explainer_images"

# 1. Standard Images (For Batch A & B)
STANDARD_IMAGE_MAP = {
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gpt-image-2]": ["std_Understanding_the_difference_between_kinetic_and_p_gpt-image-2.jpg"],
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gemini-3-pro-image]": ["std_Understanding_the_difference_between_kinetic_and_p_gemini-3-pro-image.jpg"],
    "Identifying the properties of acids and bases and understanding the pH scale [gpt-image-2]": ["std_Identifying_the_properties_of_acids_and_bases_and__gpt-image-2.jpg"],
    "Identifying the properties of acids and bases and understanding the pH scale. [gemini-3-pro-image]": ["std_Identifying_the_properties_of_acids_and_bases_and__gemini-3-pro-image.jpg"],
    "Identifying the components of the human’s body systems (circulatory, immune, digestive, respiratory, excretory, muscular, skeletal, nervous, hormonal, and reproductive) and their specific functions that support the functioning of the body. [gpt-image-2]": ["std_Identifying_the_components_of_the_human’s_body_sys_gpt-image-2.jpg"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gpt-image-2]": ["std_1_Describing_the_apparent_shape_of_the_moon_durin.jpg"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gemini-3-pro-image]": ["std_1_Describing_the_apparent_shape_of_the_moon_durin.jpg"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": ["std_1_Describing_the_apparent_shape_of_the_moon_durin.jpg"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": ["std_1_Describing_the_apparent_shape_of_the_moon_durin.jpg"],
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": ["std_2_Reading_and_writing_numbers_up_to_four_digits_i.jpg"],
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
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gpt-image-2]": ["gamified_Understanding_the_difference_between_kinetic_and_p_gpt-image-2.png"],
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gemini-3-pro-image]": ["gamified_Understanding_the_difference_between_kinetic_and_p_gemini-3-pro-image.png"],
    "Identifying the properties of acids and bases and understanding the pH scale [gpt-image-2]": ["gamified_Identifying_the_properties_of_acids_and_bases_and__gpt-image-2.png"],
    "Identifying the properties of acids and bases and understanding the pH scale. [gemini-3-pro-image]": ["gamified_Identifying_the_properties_of_acids_and_bases_and__gemini-3-pro-image.png"],
    "Identifying the components of the human’s body systems (circulatory, immune, digestive, respiratory, excretory, muscular, skeletal, nervous, hormonal, and reproductive) and their specific functions that support the functioning of the body. [gpt-image-2]": ["gamified_Identifying_the_components_of_the_human’s_body_sys_gpt-image-2.png"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gpt-image-2]": ["gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gemini-3-pro-image]": ["gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": ["gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png"],
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": ["gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png"],
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": ["gamified_2_Reading_and_writing_numbers_up_to_four_digits_i.png"],
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
    "gamified_Understanding_the_difference_between_kinetic_and_p_gpt-image-2.png": "Welcome to 'Energy Coaster Challenge'! In this game, students design and modify roller coaster tracks to guide a coaster car from start to finish. As the car ascends, a visual 'Potential Energy' meter (blue) fills, showing stored energy. During descents, this energy transforms into 'Kinetic Energy' (yellow), indicated by speed lines and a filling kinetic meter. The objective is to strategically adjust track height and slope to maintain momentum, collect 'Energy Tokens,' and avoid stalling on hills or derailing on sharp turns due to unbalanced energy. This hands-on approach helps students directly observe and manipulate the conversion between potential and kinetic energy, understanding their inverse relationship in a dynamic system.",
    "gamified_Understanding_the_difference_between_kinetic_and_p_gemini-3-pro-image.png": "Welcome to 'Energy Coaster Tycoon'! In this game, your mission is to design and operate the most thrilling roller coaster while mastering the principles of energy. You'll start by building your track, strategically placing high peaks to store 'Potential Energy' and steep drops to convert it into exhilarating 'Kinetic Energy'. As your coaster car travels, watch the on-screen meters: the 'Potential Energy' meter will fill up as you climb, indicating stored energy, and the 'Kinetic Energy' meter will surge as you speed down, showing energy of motion. Your challenge levels will require you to achieve specific energy targets at different points on the track – for example, reaching maximum kinetic energy at the bottom of a loop, or ensuring enough potential energy to clear the next hill. Successfully balancing these energy types earns you points and unlocks new track pieces and coaster designs, helping you become the ultimate Energy Coaster engineer!",
    "gamified_Identifying_the_properties_of_acids_and_bases_and__gpt-image-2.png": "Welcome, aspiring Potion Masters, to 'pH Potion Master'! Your mission is to accurately identify and categorize a series of mysterious liquid samples. Each round, you'll be presented with an unknown potion. Use your trusty pH strips to observe color changes, or deploy the advanced digital pH meter to get a precise numerical reading. Based on your observations, you must correctly classify the potion as an acid, a base, or a neutral substance, and then place it on the correct segment of the giant pH scale. Earn points for speed and accuracy, unlock new analytical tools, and climb the ranks to become the ultimate pH Potion Master!",
    "gamified_Identifying_the_properties_of_acids_and_bases_and__gemini-3-pro-image.png": "Welcome, aspiring 'pH Potion Masters'! In this game, your mission is to become the ultimate expert in acids and bases. You'll be presented with a series of mysterious ingredients, from glowing fruits to bubbling rocks, and your task is to accurately identify their properties and place them correctly on the pH scale. Use your virtual pH indicator strips and digital pH meter to test each substance, observing color changes or numerical readings to determine if it's an acid, a base, or neutral, and how strong it is. Earn points for correct classifications and quick thinking, unlocking new challenges like neutralizing dangerous concoctions or creating specific pH solutions. Master the pH scale and uncover the secrets of chemical reactions!",
    "gamified_Identifying_the_components_of_the_human’s_body_sys_gpt-image-2.png": "Welcome, aspiring 'Bio-Explorer,' to 'Anatomy Quest'! Your mission is to journey through the incredible landscape of the human body, mastering its ten vital systems. As you navigate each system – from the pulsating heart of the circulatory system to the intricate network of the nervous system – you'll encounter interactive challenges. Your goal is to correctly identify specific organs, tissues, and cells (the 'components') within each system, and then accurately match them to their unique 'functions' that keep the body running. For example, you might need to pinpoint the stomach in the digestive system and explain its role in breaking down food, or identify a neuron in the nervous system and describe how it transmits signals. Success in these challenges earns you points and unlocks new areas, ultimately proving your mastery of human anatomy and physiology.",
    "gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png": "Welcome to 'Lunar Navigator,' a cosmic challenge where you'll guide your spaceship through the solar system by mastering the moon's ever-changing face! In each round, a holographic projection of the moon will appear, illuminated from a specific angle as it orbits Earth. Your mission is twofold: first, accurately describe the apparent shape of the moon you see – is it a thin sliver, half-lit, or fully bright? Then, from a selection of choices, correctly name that specific phase (e.g., 'Waxing Crescent' or 'Waning Gibbous'). Earn 'Stardust Points' for correct answers and unlock new star systems, but be careful – incorrect answers might send you off course! The game progresses, showing the moon at various points in its rotation, helping you visualize its journey and understand why its appearance changes.",
    "gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png": "Welcome to 'Lunar Navigator'! In this interactive game, students take on the role of a space explorer tasked with accurately identifying the Moon's appearance as it journeys around Earth. As the Moon orbits, its illuminated portion changes, and players must observe its apparent shape – from a sliver to a full circle – and then select the correct name for that specific phase from a given list (e.g., 'Waxing Crescent', 'First Quarter', 'Waning Gibbous'). Correct identifications earn points and unlock new levels, while incorrect answers provide helpful hints and visual explanations of why the Moon appears that way. The ultimate goal is to master all eight major moon phases, understanding both their visual characteristics and their proper astronomical names, to become a certified Lunar Navigator!",
    "gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png": "Welcome to 'Lunar Navigator'! Your mission, should you choose to accept it, is to become a master of the moon's ever-changing face. In this interactive space adventure, you'll observe a dynamic 3D model of the Moon orbiting Earth. At various points in its rotation, the game will pause, highlighting a specific moon phase. Your task is to correctly identify and name that phase from a selection of choices provided on your control panel, describing its apparent shape. Earn points for accurate identifications and unlock new 'orbital paths' or 'telescope upgrades' as you successfully navigate through all eight major phases, learning how the Moon's apparent shape transforms as it journeys around our home planet.",
    "gamified_1_Describing_the_apparent_shape_of_the_moon_durin.png": "Welcome to 'Lunar Navigator'! Your mission, should you choose to accept it, is to become a master of the moon's ever-changing face. In this interactive space adventure, you'll observe a dynamic 3D model of the Moon orbiting Earth. At various points in its rotation, the game will pause, highlighting a specific moon phase. Your task is to correctly identify and name that phase from a selection of choices provided on your control panel, describing its apparent shape. Earn points for accurate identifications and unlock new 'orbital paths' or 'telescope upgrades' as you successfully navigate through all eight major phases, learning how the Moon's apparent shape transforms as it journeys around our home planet.",
    "gamified_2_Reading_and_writing_numbers_up_to_four_digits_i.png": "Welcome, Number Explorer, to 'Digit Dimension Dash'! Your mission is to navigate through the fantastical Number World by correctly identifying and matching numbers in their various forms. Each level presents you with a challenge: a central 'Number Portal' will display a number in one form – either standard (like 3,456), verbal (like 'three thousand four hundred fifty-six'), or expanded (like '3000 + 400 + 50 + 6'). Your task is to then locate and select the corresponding two other forms from a set of floating scrolls and crystal blocks scattered around the landscape. Successfully matching all three forms for a given number will unlock the next portal, allowing you to continue your adventure and earn 'Digit Gems' for your accuracy and speed!",
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
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gpt-image-2]": "Generated - New",
    "Understanding the difference between kinetic and potential energy in a physical system like a roller coaster. [gemini-3-pro-image]": "Generated - New",
    "Identifying the properties of acids and bases and understanding the pH scale [gpt-image-2]": "Generated - New",
    "Identifying the properties of acids and bases and understanding the pH scale. [gemini-3-pro-image]": "Generated - New",
    "Identifying the components of the human’s body systems (circulatory, immune, digestive, respiratory, excretory, muscular, skeletal, nervous, hormonal, and reproductive) and their specific functions that support the functioning of the body. [gpt-image-2]": "Generated - New",
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gpt-image-2]": "Generated - New",
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon. [gemini-3-pro-image]": "Generated - New",
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": "Generated - New",
    "1. Describing the apparent shape of the moon during its rotation around the earth, and naming the different phases of the moon.": "Generated - New",
    "2. Reading and writing numbers up to four digits in standard, verbal and expanded forms.": "Generated - New",
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

    # --- Sidebar: Generate New Quiz ---
    st.sidebar.divider()
    st.sidebar.header("Generate New Quiz")
    new_indicator = st.sidebar.text_area("Enter Educational Indicator:", placeholder="e.g. 7. Understanding fractions as parts of a whole.")
    image_model = st.sidebar.selectbox("Select Image Model:", ["gemini-3-pro-image", "gpt-image-2"])
    
    if st.sidebar.button("Generate Quizzes & Images"):
        if new_indicator:
            with st.spinner(f"Generating Quizzes and Images via LLM... This may take a minute."):
                try:
                    from quiz_generator import generate_quiz_for_indicator
                    generate_quiz_for_indicator(new_indicator.strip(), image_model)
                    st.sidebar.success("Generation complete! Refresh to see the new data.")
                except Exception as e:
                    st.sidebar.error(f"Error generating: {e}")
        else:
            st.sidebar.warning("Please enter an indicator first.")

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