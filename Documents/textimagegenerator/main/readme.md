🎬 AI Story Weaver
An interactive web application built with Python and Streamlit that generates short stories, illustrations, and audio narration using AI. This app turns a simple idea into a complete multimedia experience.

Note: You can add a screenshot of your running app here.

✨ Core Goal & Qualities
The primary goal of this project is to provide a seamless and creative platform where users can instantly visualize their ideas. It leverages powerful, open-source AI models to automate the entire creative process from script to screen (and sound).

Key Features:

📝 AI Story Generation: Takes a user's idea and generates a short, coherent story using a powerful language model (Mistral-7B).

🎨 Consistent Illustrations: Creates a series of high-quality images that visually represent each scene of the story, maintaining character consistency based on user descriptions.

🎙️ Text-to-Speech Narration: Narrates the final story with a selection of different high-quality voices using advanced TTS models.

🚀 Interactive & Modern UI: A polished, attractive, and user-friendly interface built with Streamlit, featuring an animated background and real-time progress updates.

🛠️ Tech Stack
This project is built using a modern stack of Python libraries and AI models:

Framework: Streamlit

AI Models & API: Hugging Face Inference API

Text Generation: mistralai/Mistral-7B-Instruct-v0.2

Image Generation: stabilityai/stable-diffusion-xl-base-1.0

Audio Generation: gTTS / microsoft/speecht5_tts (if implemented)

Libraries: Pillow, gtts, transformers, torch, datasets

🚀 How to Run This Project Locally
Follow these steps to set up and run the project on your local machine.

Prerequisites

Python 3.8 or higher.

A Hugging Face account and an API Token with write permissions.

1. Clone the Repository

First, clone the project from GitHub to your local machine.

git clone [https://github.com/eng-yash007/AI-Story-Generator.git](https://github.com/eng-yash007/AI-Story-Generator.git)
cd AI-Story-Generator

2. Create and Activate a Virtual Environment

It's a best practice to create a virtual environment to keep your project dependencies isolated.

# Create the environment
python3 -m venv .venv

# Activate it (on macOS/Linux)
source .venv/bin/activate

3. Install Dependencies

This project uses a requirements.txt file to manage all necessary libraries. This command will install them all at once.

pip install -r requirements.txt

Note: If you haven't created a requirements.txt file yet, you can do so by running pip freeze > requirements.txt after installing the packages manually.

4. Run the Application

Now, you can launch the Streamlit app. It will automatically open in your web browser.

streamlit run story_app.py

Once the app is running, you will need to enter your Hugging Face API token in the sidebar to start generating stories.