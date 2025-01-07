import streamlit as st
import base64
import os

# Function to display the background image
def display_background():
    bg_path = 'testcase/assets/image.png'
    if os.path.isfile(bg_path):
        st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_image(bg_path)}");
                background-size: cover;
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 120vh;
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Background image not found at path: {bg_path}")

# Function to convert image to base64
def base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Display the background image
display_background()

# Add a button to navigate to the Test Case Generator page
st.markdown("""
<div class="button-container">
    <a href="/Test_Case_Generator" target="_self">
        <button style="font-size: 20px; padding: 10px 20px;">Go to Test Case Generator</button>
    </a>
</div>
""", unsafe_allow_html=True)
