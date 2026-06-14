import os
import sys
import json
import re
from pydantic import BaseModel, Field
from typing import List

# Add the base BE directory to path so we can import llm_client
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from chat.pipeline_components.llm_client import LLMClient

# --- Pydantic Schemas for Structured JSON ---
class Option(BaseModel):
    label: str = Field(description="A, B, C, or D")
    text: str = Field(description="The text of the option")

class Question(BaseModel):
    question_text: str = Field(description="The question itself")
    options: List[Option] = Field(description="List of exactly 4 options (A, B, C, D)")
    correct_option_label: str = Field(description="The correct option label (e.g., 'A')")
    explanation: str = Field(description="Explanation of why this option is correct")

class QuizData(BaseModel):
    questions: List[Question] = Field(description="List of 3 to 4 questions")

# --- Image Generation ---
def generate_image(prompt: str, output_path: str, model_id: str):
    """
    Generates an image using either Gemini or OpenAI based on the model_id.
    """
    try:
        if model_id == "gemini-3-pro-image":
            import os
            from dotenv import load_dotenv
            from google import genai
            from google.genai import types
            from PIL import Image
            import io
            
            load_dotenv()
            project_id = os.getenv("GCP_PROJECT_ID", "alw-dev-433706")
            location = "global"
            
            client = genai.Client(vertexai=True, project=project_id, location=location)
            MODEL_ID = "gemini-3-pro-image-preview"
            
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT'],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1"
                    ),
                ),
            )
            
            if response.candidates[0].finish_reason != types.FinishReason.STOP:
                reason = response.candidates[0].finish_reason
                raise ValueError(f"Prompt Content Error: {reason}")
            
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save(output_path)
                    print(f"✅ Image generated and saved to {output_path} via {model_id}")
                    return

        elif model_id == "gpt-image-2":
            from openai import OpenAI
            import base64
            
            client = OpenAI()
            result = client.images.generate(
                model="gpt-image-2",
                prompt=prompt
            )
            image_base64 = result.data[0].b64_json
            if image_base64:
                image_bytes = base64.b64decode(image_base64)
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                print(f"✅ Image generated and saved to {output_path} via {model_id}")
                return
            else:
                # Fallback if URL is returned instead of b64
                import requests
                img_url = result.data[0].url
                img_data = requests.get(img_url).content
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"✅ Image downloaded and saved to {output_path} via {model_id}")
                return
    except Exception as e:
        print(f"⚠️ Error generating image: {e}")
        pass

# --- Helper logic to update python file variables ---
def update_python_dictionary_in_file(filepath: str, dict_name: str, key: str, value: any):
    """
    Updates a python dictionary in a file using regex and basic formatting.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Create the string to insert based on type
    if isinstance(value, list):
        # Format list as string: ["item1", "item2"]
        val_str = "[" + ", ".join(f'"{v}"' for v in value) + "]"
    elif isinstance(value, str):
        val_str = f'"{value}"'
    else:
        val_str = str(value)

    # Find the dictionary
    pattern = r"(" + dict_name + r"\s*=\s*\{)(.*?)(\})"
    
    # We will just insert the new key at the beginning of the dictionary
    insertion = f'\n    "{key}": {val_str},'
    
    def repl(match):
        return match.group(1) + insertion + match.group(2) + match.group(3)
        
    new_content = re.sub(pattern, repl, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

# --- Generator Pipeline ---
def generate_quiz_for_indicator(indicator: str, image_model: str = "gemini-3-pro-image"):
    # Append the image model to the indicator so that running the same indicator 
    # with different models creates unique side-by-side entries instead of overwriting.
    indicator = f"{indicator} [{image_model}]"
    
    print(f"🚀 Starting generation for: {indicator}")
    
    # Initialize Gemini 3.1 Flash client
    llm_client = LLMClient(model_type='gemini-2.5-flash')
    llm = llm_client.client
    structured_llm = llm.with_structured_output(QuizData)
    
    # Base paths
    image_dir = os.path.join(os.path.dirname(__file__), "indicator_explainer_images")
    os.makedirs(image_dir, exist_ok=True)
    
    # --- Batch A: Standard Image & General Questions ---
    print("⏳ Generating Batch A (Standard)...")
    prompt_res = llm.invoke(f"Write a short, descriptive prompt for an AI image generator to create a highly visual, educational infographic/illustration for kids explaining this concept: '{indicator}'. Just return the prompt text.")
    std_image_prompt = prompt_res.content.strip()
    
    # Generate Standard Image
    # Extract the base indicator for the filename, but ensure the model name is appended to avoid overwriting
    clean_indicator_name = indicator.replace(f" [{image_model}]", "")[:50].replace(" ", "_").replace(".", "")
    std_image_filename = f"std_{clean_indicator_name}_{image_model}.jpg"
    generate_image(std_image_prompt, os.path.join(image_dir, std_image_filename), image_model)
    
    # Update dicts
    update_python_dictionary_in_file(os.path.join(os.path.dirname(__file__), "quiz_display.py"), "STANDARD_IMAGE_MAP", indicator, [std_image_filename])
    update_python_dictionary_in_file(os.path.join(os.path.dirname(__file__), "quiz_display.py"), "INDICATOR_META_MAP", indicator, "Generated - New")
    
    # Generate Questions (Batch A)
    batch_a_prompt = f"Create 3 multiple-choice questions for students based on this learning indicator: '{indicator}'. The questions should test their understanding of the concept generally. Output as JSON."
    batch_a_data = structured_llm.invoke(batch_a_prompt)
    
    # Save Batch A
    batch_a_file = os.path.join(os.path.dirname(__file__), "quiz_data.json")
    save_to_json(batch_a_file, indicator, batch_a_data)

    # --- Batch B: Image Referenced Questions ---
    print("⏳ Generating Batch B (Image Referenced)...")
    batch_b_prompt = f"Create 3 multiple-choice questions for the indicator: '{indicator}'. These questions should be phrased as if the student is looking at a visual diagram. Use phrases like 'Look at the image' or 'Based on the diagram'. Output as JSON."
    batch_b_data = structured_llm.invoke(batch_b_prompt)
    
    batch_b_file = os.path.join(os.path.dirname(__file__), "quiz_data_new.json")
    save_to_json(batch_b_file, indicator, batch_b_data)

    # --- Batch C: Gamified Questions ---
    print("⏳ Generating Batch C (Gamified)...")
    gamified_prompt_res = llm.invoke(f"Design a fun, gamified scenario for students to learn: '{indicator}'. Provide exactly two paragraphs. First paragraph: A DALL-E/Imagen image generation prompt for the game scene. Second paragraph: A brief context description of the game rules for the student.")
    parts = gamified_prompt_res.content.split('\n\n')
    gamified_img_prompt = parts[0].strip() if len(parts) > 0 else "A gamified educational scene."
    scenario_context = parts[1].strip() if len(parts) > 1 else "Welcome to the game!"
    
    gamified_image_filename = f"gamified_{clean_indicator_name}_{image_model}.png"
    generate_image(gamified_img_prompt, os.path.join(image_dir, gamified_image_filename), image_model)
    
    # Update maps
    update_python_dictionary_in_file(os.path.join(os.path.dirname(__file__), "quiz_display.py"), "GAMIFIED_IMAGE_MAP", indicator, [gamified_image_filename])
    update_python_dictionary_in_file(os.path.join(os.path.dirname(__file__), "quiz_display.py"), "SCENARIO_CONTEXT_MAP", gamified_image_filename, scenario_context)
    
    batch_c_prompt = f"Indicator: '{indicator}'. Scenario context: '{scenario_context}'. Create 3 multiple-choice questions where the student plays the game described in the context to solve the problems. Output as JSON."
    batch_c_data = structured_llm.invoke(batch_c_prompt)
    
    batch_c_file = os.path.join(os.path.dirname(__file__), "quiz_data_gamified.json")
    save_to_json(batch_c_file, indicator, batch_c_data)
    
    print("🎉 All generations complete!")

def save_to_json(filepath, indicator, quiz_data_pydantic):
    data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except:
                pass
                
    # Convert pydantic model to dictionary
    data[indicator] = {
        "indicator": indicator,
        "questions": quiz_data_pydantic.dict()["questions"]
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
