import streamlit as st
import google.generativeai as genai
import os
import io
import base64
from pdf2image import convert_from_bytes

# Directly set your API key here
API_KEY = "AIzaSyCjAu_y0MaC-et9YZOuueMUvjdBteA3TeE"

# Ensure the API key is available
if not API_KEY:
    st.error("API Key is missing! Please set your API key.")
    st.stop()

# Configure Google Gemini API with the API key
genai.configure(api_key=API_KEY)

# Function to check available models (debugging)
def list_available_models():
    models = genai.list_models()
    return models

# Call to get the response from the Gemini model
def get_gemini_response(input_prompt, pdf_content, job_desc):
    model = genai.GenerativeModel(model_name='gemini-1.5-pro')  # Ensure this model exists
    response = model.generate_content(contents=[input_prompt, pdf_content[0], job_desc])
    return response.text

# Function to convert PDF to image for processing
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read())  # Convert PDF to image
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# User inputs
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

# Buttons for processing
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Define the prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please provide a professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Evaluate the resume against the provided job description and provide a percentage match. 
First, output a match percentage, followed by missing keywords, and then final thoughts.
"""

# Handling button clicks
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Evaluation Result:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Match Percentage:")
        st.write(response)
    else:
        st.warning("Please upload the resume.")
