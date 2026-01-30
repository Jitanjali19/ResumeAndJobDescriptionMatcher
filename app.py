# https://resumeandjobdescriptionmatcher-l9uxfi8drbrtsjwwd9x3rz.streamlit.app/
#  ye original deployeent link hai


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



# ///////chatgpt

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# -------------------- Load Environment Variables --------------------
load_dotenv()  # load .env variables locally

# ----------- Configure API Key ----------------
if "GOOGLE_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
elif "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("❌ Google API Key not found! Please set it in .env or Streamlit Secrets.")

# ----------- Configure Service Account JSON (Optional but recommended) --------
if "GOOGLE_APP_CRED_JSON" in os.environ or "GOOGLE_APP_CRED_JSON" in st.secrets:
    json_str = os.environ.get("GOOGLE_APP_CRED_JSON", None) or st.secrets.get("GOOGLE_APP_CRED_JSON")
    service_account_file = "/tmp/service_account.json"
    try:
        service_account_info = json.loads(json_str)
        with open(service_account_file, "w") as f:
            json.dump(service_account_info, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file
    except Exception as e:
        st.error(f"❌ Failed to load Service Account JSON: {e}")

# -------------------- Functions --------------------

def get_gemini_response(input_prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        return f"❌ API call failed: {e}"


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text


# -------------------- Prompt Template --------------------
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
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
    <div style="white-space: pre-wrap; word-break: break-word;">
    <h1 style='text-align:center;'>📄 Smart ATS</h1>
    <p style='text-align:center; font-size:18px; color:gray;'>
    Improve Your Resume & Beat ATS Filters 🚀
    </p>
    <hr>
    >
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
            # Fill the prompt template with resume text and JD
            input_prompt_filled = input_prompt_template.format(text=text, jd=jd)
           # Fill the prompt with resume text and job description
            input_prompt_filled = input_prompt.format(text=text, jd=jd)
            response = get_gemini_repsonse(input_prompt_filled)


        st.success("✅ Analysis Completed!")
        st.markdown("### 📊 ATS Evaluation Result")
        st.code(response, language="json")

    else:
        st.warning("⚠️ Please upload resume and paste job description")
