# import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# from dotenv import load_dotenv
# import json

# load_dotenv() ## load all our environment variables

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_repsonse(input):
#     model=genai.GenerativeModel('gemini-2.5-flash')
#     response=model.generate_content(input)
#     return response.text

# def input_pdf_text(uploaded_file):
#     reader=pdf.PdfReader(uploaded_file)
#     text=""
#     for page in range(len(reader.pages)):
#         page=reader.pages[page]
#         text+=str(page.extract_text())
#     return text

# #Prompt Template

# input_prompt="""
# Hey Act Like a skilled or very experience ATS(Application Tracking System)
# with a deep understanding of tech field,software engineering,data science ,data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# best assistance for improving thr resumes. Assign the percentage Matching based 
# on Jd and
# the missing keywords with high accuracy
# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """

# ## streamlit app
# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")
# jd=st.text_area("Paste the Job Description")
# uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

# submit = st.button("Submit")

# if submit:
#     if uploaded_file is not None:
#         text=input_pdf_text(uploaded_file)
#         response=get_gemini_repsonse(input_prompt)
#         st.subheader(response)





#///////chatgpt

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# -------------------- UI PART --------------------

st.set_page_config(
    page_title="Smart ATS Resume Checker",
    page_icon="📄",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align:center;'>📄 Smart ATS</h1>
    <p style='text-align:center; font-size:18px; color:gray;'>
    Improve Your Resume & Beat ATS Filters 🚀
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

jd = st.text_area(
    "📝 Paste Job Description",
    placeholder="Paste the complete job description here...",
    height=200
)

uploaded_file = st.file_uploader(
    "📤 Upload Your Resume (PDF only)",
    type="pdf",
    help="Upload your resume in PDF format"
)

submit = st.button("🔍 Analyze Resume")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("⏳ Analyzing your resume... Please wait"):
            text = input_pdf_text(uploaded_file)
            response = get_gemini_repsonse(input_prompt)

        st.success("✅ Analysis Completed!")

        st.markdown("### 📊 ATS Evaluation Result")
        st.code(response, language="json")

    else:
        st.warning("⚠️ Please upload resume and paste job description")
