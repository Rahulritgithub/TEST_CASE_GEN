import streamlit as st
import time
import base64
import os  # Import the os module

# Custom CSS for the splash screen
def splash_screen_css():
    st.markdown(f"""
    <style>
        .splash-screen {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 20vh;
        /* Light gray background */
            background-size: 400% 400%;
            animation: gradientAnimation 15s ease infinite; /* Gradient animation */
        }}
        @keyframes gradientAnimation {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .splash-logo {{
            width: 250px;
            height: auto;
            animation: fadeInText 1s ease-in-out forwards;
        }}
        @keyframes fadeInText {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes logoAnimation {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }} /* Slightly enlarges logo at midpoint */
        }}
        .main-content {{
            display: none; /* Hide main content initially */
        }}
    </style>
    """, unsafe_allow_html=True)

# Function to convert image to base64
def base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Display the splash screen
def display_splash_screen():
    logo_path = 'assets/Tessolve_logo.png.png'
    if os.path.isfile(logo_path):  # Check if the logo file exists
        st.markdown(f"""
        <div class="splash-screen">
            <img class="splash-logo" src="data:image/png;base64,{base64_image(logo_path)}">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Logo file not found at path: {logo_path}")

# Main page configuration
st.set_page_config(
    page_title="Test Case Generator App",
    page_icon="🧪",
    layout="wide",
)

# Apply custom CSS
splash_screen_css()

# Display the splash screen
display_splash_screen()

# Wait for 2 seconds (simulate splash screen delay)
time.sleep(1)

# Hide the splash screen and show the main content
st.markdown("""
<script>
    // Hide the splash screen after 2 seconds
    setTimeout(function() {
        document.querySelector(".splash-screen").style.display = "none";
        document.querySelector(".main-content").style.display = "block";
    }, 1000); // 2000 milliseconds = 2 seconds
</script>
""", unsafe_allow_html=True)

# Main content (hidden initially, shown after splash screen)
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Main page content
st.title("Welcome to the Test Case Generator App")
st.write("Navigate to the appropriate page using the sidebar.")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- **Home Page**: The main landing page with navigation options.
- **Test Case Generator**: The page to generate test cases.
""")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Your Name")

# Close the main content div
st.markdown('</div>', unsafe_allow_html=True)