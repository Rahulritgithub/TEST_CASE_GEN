import base64
import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Test Case Generator",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTy0x5TXAZwt1-8S7dMnehqGlTOLIffkE6CQvW2R2C9&s",
    layout="wide",
)

# Configure Gemini AI model with the provided API key
API_KEY = "AIzaSyA1uirBqpZIKp2j6V1wB-w9e9Qh4WvYTKE"  # Ensure you have the API key in your .env file
genai.configure(api_key=API_KEY)


def display_logo_and_title():
    logo_path = 'assets/Tessolve_logo.png.png'
    if os.path.isfile(logo_path):
        st.markdown(f"""
        <style>
            .logo {{
                position: absolute;
                top: 20px;  /* Space from the top of the page */
                left: 2px;  /* Space from the left of the page */
                z-index: 1000;
            }}
            .logo img {{
                width: 250px;  /* Increased width */
                height: auto;  
            }}
            .main-title {{
                position: absolute;  /* Absolute positioning to place it directly below the logo */
                top: 80px;  /* Adjust based on logo height and desired spacing */
                left: 2px;  /* Align with logo */
                z-index: 1000;
                font-family: Arial, sans-serif;
                font-size: 24px;  /* Adjust title font size */
                font-weight: bold;
            }}
            .content {{
                margin-top: 100px; /* Space to ensure content is below the title */
            }}
            .disclaimer {{
                position: fixed;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                text-align: center;
                font-size: 12px;
                color: black;
            }}
            .header-spacing {{
                margin-top: -50px; /* Adjust this value to move the header up */
            }}
        </style>
        <div class="logo">
            <img src="data:image/png;base64,{base64_image(logo_path)}">
        </div>
        <div class="content">
        """, unsafe_allow_html=True)
    else:
        st.error(f"Logo file not found at path: {logo_path}")


def base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def display_disclaimer():
    st.markdown("""
    <div class="disclaimer">
        Disclaimer: The content is generated by a Gen AI model. It may make mistakes, so please review the results carefully.
    </div>
    """, unsafe_allow_html=True)


# Function to get response from Gemini AI with retry mechanism
def get_gemini_response(input, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(input)
            time.sleep(0.5)
            return response.text
        except Exception as e:
            st.error(f"An error occurred while fetching response: {e}")
            if retries < max_retries - 1:
                retries += 1
                st.warning(f"Retrying attempt {retries}/{max_retries}...")
                time.sleep(2 ** retries)
            else:
                raise RuntimeError("Exceeded maximum retries. Failed to get response.")


# Function to read Excel file and extract requirement based on id
def get_requirement(excel_file, req_id):
    try:
        df = pd.read_excel(excel_file)
        required_columns = ["id", "Primary Text", "Risk", "isHeading", "Requirement Type"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"The Excel file must contain the following columns: {required_columns}")
            return None

        # Convert req_id to float for comparison
        req_id = float(req_id)

        # Check if the id exists in the DataFrame
        requirement = df.loc[df["id"] == req_id, required_columns]
        if requirement.empty:
            st.error(f"No requirement found for id: {req_id}")
            return None
        return requirement.iloc[0]  # Return the first matching row as a Series
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None


# Function to parse the AI response into a DataFrame with the specified fields
def parse_ai_response(response, test_case_id):
    try:
        # Initialize variables to store sections
        sections = {
            "Test Case": "Generated Test Case",  # Placeholder for the test case name
            "Test Case ID": test_case_id,  # Use the provided test case ID
            "Precondition": "",
            "Expected Result": "",
            "Steps": "",
            "Post Condition": "",
            "Actual Result": ""  # Placeholder for actual result (can be filled manually later)
        }

        # Split the response into lines
        lines = response.strip().split("\n")

        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith("Pre-condition:"):
                current_section = "Precondition"
                sections[current_section] = line.replace("Pre-condition:", "").strip()
            elif line.startswith("Expected results:"):
                if current_section == "Precondition":
                    sections["Expected Result"] = line.replace("Expected results:", "").strip()
                elif current_section == "Steps":
                    sections["Expected Result"] += "\n" + line.replace("Expected results:", "").strip()
            elif line.startswith("Step1:"):
                current_section = "Steps"
                sections[current_section] = line.replace("Step1:", "").strip()
            elif line.startswith("Step2:"):
                if sections["Steps"]:  # Append Step2 if Steps already has content
                    sections["Steps"] += "\n" + line.replace("Step2:", "").strip()
                else:
                    sections["Steps"] = line.replace("Step2:", "").strip()
            elif line.startswith("Post-condition:"):
                current_section = "Post Condition"
                sections[current_section] = line.replace("Post-condition:", "").strip()
            else:
                if current_section:
                    sections[current_section] += "\n" + line.strip()

        # Create a DataFrame
        df = pd.DataFrame([sections])

        return df
    except Exception as e:
        st.error(f"Error parsing AI response: {e}")
        return None


# Constant prompt for Gemini AI
PROMPT = """
Generate a detailed test case for the given requirement in the following all data which should be in table format:


Pre-condition:
<pre-condition>

Expected results:
<expected results>

Step1:
<step1 description>

Expected results:
<expected results for step1>

Step2:
<step2 description>

Expected results:
<expected results for step2>

Post-condition:
<post-condition>

Expected results:
<expected results for post-condition>
"""

# Display logo and title
display_logo_and_title()

# Add spacing above the header
st.markdown('<div class="header-spacing"></div>', unsafe_allow_html=True)

# Streamlit app
st.header("Test Case Generation for Requirements")

# Upload Excel file
excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# Input id
req_id = st.text_input("Enter id")

# Submit button
if st.button("Generate Test Cases"):
    if excel_file is None or not req_id:
        st.error("Please upload an Excel file and provide an id.")
    else:
        # Extract requirement from Excel
        requirement = get_requirement(excel_file, req_id)
        if requirement is not None:
            # Display the extracted requirement details
            st.subheader("Extracted Requirement Details")
            st.write(f"**ID:** {requirement['id']}")
            st.write(f"**Risk:** {requirement['Risk']}")
            st.write(f"**isHeading:** {requirement['isHeading']}")
            st.write(f"**Requirement Type:** {requirement['Requirement Type']}")

            # Generate output using Gemini AI
            input_text = f"Requirement: {requirement['Primary Text']}\nPrompt: {PROMPT}"
            try:
                output = get_gemini_response(input_text)
                st.subheader("Generated Test Case")
                st.write(output)

               
                
            except Exception as e:
                st.error(f"Error generating test case: {e}")

# Display disclaimer
display_disclaimer()