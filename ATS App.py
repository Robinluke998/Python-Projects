from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key="AIzaSyCjAu_y0MaC-et9YZOuueMUvjdBteA3TeE")

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

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
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced ATS (Applicant Tracking System) evaluator with expertise in assessing resumes across various domains, including Data Analytics, Business Analytics, Data Science, Full Stack Development, Product Management, and Project Management. 
Your task is to analyze the provided resume against the given job description for the [role]. 
- Evaluate the candidate's core technical skills, experience, and ability to align with the specific requirements of the role.
- For technical roles, assess experience with tools and technologies like SQL, Python, R, TensorFlow, JavaScript, and Agile.
- For leadership/management roles, evaluate the candidate’s strategic thinking, team management, and experience leading projects or cross-functional teams.
- Provide a detailed evaluation highlighting the strengths, gaps, and areas where the candidate may excel or require improvement.

"""

input_prompt3 = """
You are an ATS evaluator with deep knowledge of data science, engineering, and product management. Your task is to evaluate the candidate’s resume against the provided job description and provide the following:
- **Percentage match**: Calculate the overall match percentage between the resume and job description based on skills, experience, and qualifications.
- **Missing Keywords**: List the key skills, certifications, or experience missing in the resume that are critical for the job role.
- **Final Thoughts**: Provide a summary of the candidate’s suitability for the job. Highlight areas where the candidate excels and suggest any improvements or gaps that need to be addressed.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


