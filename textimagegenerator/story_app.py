# =========================================================
# 🎬 AI Story Weaver (Upgraded UI/UX Version)
# =========================================================

import streamlit as st
import os
import re
from gtts import gTTS
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="🎬 AI Story Weaver",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for an attractive UI ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(-45deg, #0E1117, #1B212D, #0E1117, #212E40);
    background-size: 400% 400%;
    animation: gradient-animation 15s ease infinite;
    color: #FAFAFA;
}

@keyframes gradient-animation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton>button {
    border-radius: 20px;
    border: 2px solid #00BFFF; /* DeepSkyBlue */
    color: #00BFFF;
    background-color: transparent;
    transition: all 0.3s ease-in-out;
    font-weight: 600;
}

.stButton>button:hover {
    transform: scale(1.05);
    background-color: #00BFFF;
    color: #0E1117;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.6);
}

/* Style for the output containers */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    border: 1px solid #4A4A4A;
    border-radius: 10px;
    padding: 25px;
    margin-top: 20px;
    background-color: rgba(42, 50, 68, 0.3); /* Semi-transparent background */
}
"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)


# --- Helper and Generation Functions ---

def simple_sent_tokenize(text, max_scenes=5):
    """Splits text into sentences."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return sentences[:max_scenes]

def generate_story(prompt, hf_token):
    """Generates a short story using the Zephyr-7B model."""
    try:
        client = InferenceClient(token=hf_token)
        messages = [
            {"role": "system", "content": "You are a creative, vivid storyteller. Write a short, engaging story (around 5 sentences)."},
            {"role": "user", "content": f"Write a story based on this idea: '{prompt}'"}
        ]
        # --- CHANGED MODEL ---
        # Using a different, highly reliable model to rule out endpoint issues.
        response = client.chat_completion(
            model="HuggingFaceH4/zephyr-7b-beta", 
            messages=messages, 
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Story Generation Error: {e}")
        return None

def generate_images(scenes, character_sheet, hf_token, status_updater):
    """Generates an image for each scene with a progress bar."""
    images = []
    progress_bar = st.progress(0, text="Kicking off illustration process...")
    try:
        client = InferenceClient("stabilityai/stable-diffusion-xl-base-1.0", token=hf_token)
        for i, scene in enumerate(scenes, 1):
            # Update the main status
            status_updater.update(label=f"🎨 Creating illustration {i} of {len(scenes)}...")
            
            full_prompt = f"cinematic film still, epic, masterpiece, {character_sheet}, {scene}"
            negative_prompt = "cartoon, anime, 3d, painting, blurry, deformed, signature, watermark, text"
            
            # --- THIS IS THE CORRECTED PART ---
            # The result is saved to the 'image' variable...
            image = client.text_to_image(
                prompt=full_prompt, negative_prompt=negative_prompt, width=1024, height=768
            )
            # ...and the SAME 'image' variable is appended to the list.
            images.append(image)
            
            # Update the progress bar
            progress_percentage = int(((i) / len(scenes)) * 100)
            progress_bar.progress(progress_percentage, text=f"Illustration {i} ready!")
            
        progress_bar.empty() # Clear the progress bar on completion
        return images
    except Exception as e:
        st.error(f"Image Generation Error: {e}")
        progress_bar.empty()
        return []
    
def generate_audio(story, path="story_narration.mp3"):
    """Generates an MP3 audio file from the story text."""
    try:
        tts = gTTS(story, lang="en")
        tts.save(path)
        return path
    except Exception as e:
        st.error(f"Audio Generation Error: {e}")
        return None

# --- UI Layout ---

# Main Title using HTML for gradient effect
st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 3.5rem; font-weight: 600; background: -webkit-linear-gradient(45deg, #00BFFF, #1E90FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎬 AI Story Weaver
        </h1>
        <p style="font-size: 1.2rem; color: #b0c4de;">
            Turn your ideas into illustrated and narrated stories with the power of AI.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("✍️ Your Inputs")

    with st.expander("🔑 API Configuration", expanded=False):
        hf_token_input = st.text_input(
            "Hugging Face API Token", type="password", help="Get your token from https://huggingface.co/settings/tokens"
        )

    user_input = st.text_input(
        "Enter your story idea", placeholder="e.g., A robot discovering an ancient, magical forest."
    )

    character_input = st.text_area(
        "Describe your character & style", placeholder="e.g., A small, curious robot with a polished chrome finish, cinematic film still.", height=150
    )

    generate_btn = st.button("✨ Weave My Story!", use_container_width=True)

# --- Main Logic with Advanced Loading ---
if generate_btn:
    if not all([hf_token_input, user_input, character_input]):
        st.warning("Please fill in all the fields in the sidebar to begin.")
    else:
        # Use st.status for a better loading experience
        with st.status("🚀 Kicking off the creative process...", expanded=True) as status:
            status.update(label="✍️ Writing a compelling story...")
            story_text = generate_story(user_input, hf_token_input)
            
            if story_text:
                st.session_state.story_text = story_text
                scenes = simple_sent_tokenize(story_text)
                
                # Pass the status object to the image generator
                story_images = generate_images(scenes, character_input, hf_token_input, status)
                st.session_state.story_images = story_images

                status.update(label="🎙️ Recording the narration...")
                audio_file_path = generate_audio(story_text)
                st.session_state.audio_file_path = audio_file_path
                
                status.update(label="✅ Story complete!", state="complete", expanded=False)
                st.session_state.story_generated = True

# --- Display Area for Outputs ---
if 'story_generated' in st.session_state and st.session_state.story_generated:
    with st.container():
        st.header("📖 Your Generated Story")
        st.markdown(f"> _{st.session_state.story_text}_")
        
        if st.session_state.audio_file_path:
            st.audio(st.session_state.audio_file_path)
    
    with st.container():
        st.header("🎨 Story Illustrations")
        if st.session_state.story_images:
            cols = st.columns(min(len(st.session_state.story_images), 3))
            for i, img in enumerate(st.session_state.story_images):
                cols[i % len(cols)].image(img, caption=f"Scene {i+1}", use_container_width=True)
        else:
            st.warning("Could not generate images for this story.")