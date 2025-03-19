from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import pdfplumber
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyCjAu_y0MaC-et9YZOuueMUvjdBteA3TeE")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            first_page = pdf.pages[0]  # Get the first page

            # Convert the first page to an image
            img = first_page.to_image()

            # Convert the image to a byte array
            img_byte_arr = io.BytesIO()
            img.to_image().save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Encode the image in base64
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# Define prompt for evaluation
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches 
the job description. First, the output should come as a percentage, followed by the keywords missing, and finally, your final thoughts.
"""

# Handling button clicks and generating responses
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
