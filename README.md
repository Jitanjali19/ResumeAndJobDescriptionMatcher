# Smart ATS Resume Checker

Smart ATS is a Streamlit app that compares a resume PDF with a job description using Google Gemini and returns ATS-style feedback.

## Features

- Upload a resume in PDF format
- Paste a job description
- Choose the type of analysis you want:
  - Tell me about the resume
  - How can I improve my skills
  - What keywords are missing
  - Percentage match
- View the result in a cleaner, vertical UI

## Tech Stack

- Python
- Streamlit
- PyPDF2
- Google Gemini API (`google-generativeai`)
- python-dotenv

## Project Structure

- `app.py` - main Streamlit app
- `requirements.txt` - Python dependencies

## Setup

1. Create and activate a virtual environment if needed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Gemini API key.

For local development, create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

If you are using Streamlit Cloud, add the key in Streamlit Secrets.

## Run Locally

```bash
streamlit run app.py
```

## How It Works

1. Enter a job description.
2. Upload a resume PDF.
3. Select the analysis type.
4. Click **Analyze Resume**.
5. The app extracts resume text and sends it with the selected prompt to Gemini.

## Notes

- The app expects PDF resumes.
- Make sure `GOOGLE_API_KEY` is available before running.
- `google.generativeai` is currently deprecated upstream; the app still works, but a future migration to `google.genai` is recommended.

## Deployment

For Streamlit Cloud, ensure these dependencies are installed from `requirements.txt`:

- `streamlit`
- `PyPDF2`
- `google-generativeai`
- `python-dotenv`

Also set `GOOGLE_API_KEY` in app secrets.
