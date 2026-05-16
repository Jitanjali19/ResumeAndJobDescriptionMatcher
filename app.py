# https://resumeandjobdescriptionmatcher-l9uxfi8drbrtsjwwd9x3rz.streamlit.app/
# https://resumeandjobdescriptionmatcher-l9uxfi8drbrtsjwwd9x3rz.streamlit.app/
#  ye original deployment link hai


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
import tempfile

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
    try:
        service_account_info = json.loads(json_str)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(service_account_info, f)
            service_account_file = f.name
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
        <style>
            :root{
                --bg:#0b1220; --card:#0f1724; --muted:#9ca3af; --accent:#10b981; --accent-2:#60a5fa;
            }
            .header-container{max-width:900px;margin:8px auto 18px;padding:18px 8px;text-align:center}
            .header-title{font-size:36px;margin:0;color:whitesmoke;font-weight:700}
            .header-sub{color:var(--muted);margin-top:6px;margin-bottom:8px}
            .stButton>button{background:linear-gradient(90deg,var(--accent),var(--accent-2));color:white;border:none;padding:10px 16px;border-radius:8px}
            .stButton>button:hover{filter:brightness(1.05)}
            .stTextArea>div>textarea, .stTextArea>div>div>textarea{background:#071028;color:#e6eef6;border-radius:8px}
            .ats-card{background:var(--card);padding:12px;border-radius:10px;color:#d1fae5;margin-bottom:10px;white-space:pre-wrap}
            .ats-key{color:#a7f3d0;font-weight:600;margin-bottom:6px}
        </style>
        <div class="header-container">
            <div style="display:flex;align-items:center;justify-content:center;gap:12px">
                <div style="font-size:28px">📄</div>
                <div style="text-align:left">
                    <div class="header-title">Smart ATS</div>
                    <div class="header-sub">Improve Your Resume & Beat ATS Filters 🚀</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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

# Let user choose what type of analysis they want
analysis_type = st.radio(
    "🔎 Select analysis",
    (
        "Tell Me About the Resume",
        "How Can I Improve my Skills",
        "What Keywords Are Missing",
        "Percentage Match",
    ),
)

submit = st.button("🔍 Analyze Resume")

# Prompt templates for different analysis types
input_prompt_about = """
You are an experienced HR with Tech Experience in the field of Data Science,
Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis.
Review the provided resume against the job description and provide a professional
evaluation on whether the candidate's profile aligns with the role. Highlight the
strengths and weaknesses of the applicant in relation to the specified job requirements.
Resume:
{text}

Job Description:
{jd}
"""

input_prompt_improve = """
You are an experienced Technical HR Manager. Carefully evaluate the resume and job description.
Suggest clear and practical improvements that the candidate can make to their skills, tools,
and technologies to increase their chances of getting selected for the role. Focus on
technical gaps, relevant certifications, and practical projects that can strengthen the profile.
Resume:
{text}

Job Description:
{jd}
"""

input_prompt_missing = """
You are an ATS expert. Review the given resume and job description, and identify the important
keywords, skills, and phrases from the job description that are missing in the resume. Provide
a list of missing keywords first, then suggest how and where the candidate can add them in the
resume naturally to improve ATS score.
Resume:
{text}

Job Description:
{jd}
"""

input_prompt_percentage = """
You are a skilled ATS scanner. Evaluate the resume against the provided job description and give
the percentage match of the resume to the job description. Then list the missing keywords and
final thoughts.
Resume:
{text}

Job Description:
{jd}
"""

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("⏳ Analyzing your resume... Please wait"):
            text = input_pdf_text(uploaded_file)
            # choose prompt based on user selection
            if analysis_type == "Tell Me About the Resume":
                prompt = input_prompt_about.format(text=text, jd=jd)
            elif analysis_type == "How Can I Improve my Skills":
                prompt = input_prompt_improve.format(text=text, jd=jd)
            elif analysis_type == "What Keywords Are Missing":
                prompt = input_prompt_missing.format(text=text, jd=jd)
            else:
                prompt = input_prompt_percentage.format(text=text, jd=jd)

            response = get_gemini_response(prompt)


        st.success("✅ Analysis Completed!")
        st.markdown("### 📊 ATS Evaluation Result")
        # Try to parse the assistant response as JSON and render vertically for better UX
        try:
            parsed = json.loads(response)
        except Exception:
            parsed = None

        if isinstance(parsed, dict):
            # Vertical stacked cards with wrapped content
            for key, val in parsed.items():
                st.markdown(f"**{key}**")
                if isinstance(val, (list, tuple)):
                    for item in val:
                        st.markdown(f"- {item}")
                else:
                    # card-like container
                    st.markdown(
                        f"<div style='background:#0f1724;padding:12px;border-radius:8px;color:#d1fae5;white-space:pre-wrap;'>{val}</div>",
                        unsafe_allow_html=True,
                    )
                st.write("")
        else:
            # Fallback: show wrapped text area so users don't need horizontal scrolling
            st.text_area("Evaluation (raw)", value=response, height=300)

    else:
        st.warning("⚠️ Please upload resume and paste job description")
