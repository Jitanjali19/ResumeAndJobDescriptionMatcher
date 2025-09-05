import os
os.environ["NO_GCE_CHECK"] = "True"

from dotenv import load_dotenv
# from pdf2image import convert_from_bytes

load_dotenv()

import base64
#these are all reuirement imported so i can use to access
import streamlit as st

import io
#convert pdf into image
from PIL import Image
import pdf2image
from pdf2image import convert_from_path
import pytesseract
#google gemini pro so we can connect AI to proejct for keywords and other detailing 
import google.generativeai as genai

#google_api_key from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt],timeout=120)
    return response.text

#this prompt play a very imaportant role because it tell -> what model need to be do
#pdf to text and the  text is given to the gemini and and it give text formate answer



def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        uploaded_file.seek(0) 
        #convert pdf to image 
        # poppler_path = r"C:\poppler-25.07.0\Library\bin"
        images=pdf2image.convert_from_bytes(pdf_bytes)
        
        #take the page
        first_page=images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('No File Uploaded')

    



## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload Your Resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

#we are adding some more functionality which make this project very intresting 

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improve my SKills")

submit3 = st.button("What are the keywords thet are Missing")

submit4 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of any job role from Data Science,
 Full Stack Web Development, Big Data Engineering,DEVOPS, Data Analyst,
 your task is to review the provided resume against the job description for these profiles.
 Please share your professional evaluation on whether the candidate's profile aligns with the role.
 Highlight the streangths and weakness of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced Technical HR Manager with expertise in Data Science,
Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis.
Your task is to carefully evaluate the resume and job description. Suggest clear
and practical improvements that the candidate can make to their skills, tools,
and technologies to increase their chances of getting selected for the role.
Focus on technical gaps, relevant certifications, and practical projects that
can strengthen the profile.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) expert. Review the given resume and
job description, and identify the important **keywords, skills, and phrases**
from the job description that are missing in the resume. Provide a list of
missing keywords first, then suggest how and where the candidate can add them
in the resume naturally to improve ATS score.
"""


input_prompt4 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of any one job role
Data Science, Full Stack Web Development, Big Data Engineering,DEVOPS, Data Analyst,
and deep ATS functionality, your task is to evalute the resume against the provided job description.
Give me the percentage of match if the resume matches job description.
First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        #geminiResponse function which takes prompt,pdfcontent and input as job description
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")


elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")


elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
