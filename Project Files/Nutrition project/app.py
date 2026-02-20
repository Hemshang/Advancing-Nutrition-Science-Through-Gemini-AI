import streamlit as st
import google.generativeai as genai
import os
from PIL import Image # Image processing kosam idi avasaram
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = "AIzaSyB6VlTBfizgKXeQHsXy_xfbDTvZj8eddi0"

if not API_KEY:
    st.error("API Key missing! Please set GOOGLE_API_KEY in your .env file.")
else:
    genai.configure(api_key=API_KEY)

# Streamlit page setup
st.set_page_config(page_title="Advancing Nutrition Science through Gemini AI")
st.title("🍎 Nutrition Science with Gemini AI")
st.write("AI-powered nutritional analysis for smarter health decisions.")

# User text input
food_items = st.text_area(
    "Enter food items (comma separated):",
    placeholder="e.g. 1 banana, 1 glass milk"
)

# Optional image upload
uploaded_file = st.file_uploader("Upload food image (optional)", type=["jpg", "png", "jpeg"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Analyze button
if st.button("Analyze Nutrition"):
    # Either text or image should be present
    if not food_items.strip() and image is None:
        st.warning("Please enter food items or upload an image.")
    else:
        try:
            # Corrected Model Name (Gemini 1.5 Flash is stable)
            model = genai.GenerativeModel("gemini-2.5-flash")

            # Prompt setting
            prompt = f"""
            Provide a detailed nutritional analysis and a health score (0-10) for the food items mentioned or shown in the image.
            Input: {food_items}

            Include:
            - Calories, Protein, Carbohydrates, Fat
            - Vitamins and minerals
            - Health score (0-10) with a brief reason.
            """

            # Generate response (Sending both text and image if available)
            inputs = [prompt]
            if image:
                inputs.append(image)
            
            response = model.generate_content(inputs)

            # Display result
            st.success("Analysis Complete!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {str(e)}")