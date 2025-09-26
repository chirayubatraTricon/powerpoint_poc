import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_text(uploaded_file):
    """Extract all text from a PDF file."""
    text = ""
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        try:
            text += page.extract_text() or ""
        except Exception as e:
            text += f"\n[Error extracting page: {e}]"
    return text

def get_text_chunks(text, chunk_size=2000, chunk_overlap=200):
    """Split text into manageable chunks for AI models."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)


def generate_ppt_raw_content(raw_text: str, topic: str = "Create a resume ppt"):
    SYSTEM_PROMPT = """
You are a presentation content generator.
You will be given raw, unstructured text (often messy, with broken words/lines).
Your task is to clean, organize, and extract informative content to build a PowerPoint presentation.

Rules:
- Fix broken words/sentences from PDF line breaks.
- Remove duplicates, filler words, and noise.
- Group related ideas into clear sections.
- Highlight important facts, skills, achievements, projects, or themes.
- Output should be informative and structured, but **not yet formatted into slides**.
- Think of it as producing a structured "raw outline" which another step will later map into actual slides.

Output format:
{
  "title": "...",
  "subtitle": "...",
  "summary": "...",
  "sections": [
    {
      "heading": "...",
      "content": [
        "point 1",
        "point 2",
        "point 3"
      ]
    }
  ],
  "key_highlights": [
    "important highlight 1",
    "important highlight 2"
  ]
}
"""

    user_prompt = f"""
TOPIC: {topic}

RAW TEXT FROM PDF:
{raw_text}
"""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite", system_instruction=SYSTEM_PROMPT)
    response = model.generate_content(user_prompt)
    return response.text  # returns JSON string (structured raw content)



# streamlit
st.title("PowerPoint generation with AI")
prompt = st.text_input("Enter your prompt:")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
num_slides = st.number_input("Number of slides:", min_value=1, max_value=50, value=5)
if st.button("Process PDF"):
    if uploaded_file is not None:

        # processing starts
        raw_text = extract_pdf_text(uploaded_file)
        chunks = get_text_chunks(raw_text)
        all_text = "\n".join(chunks)
        llm_content = generate_ppt_raw_content(chunks)
        print(llm_content)
        # processing ends

        st.success("✅ PDF processed successfully!")
        
        # Preview
        st.subheader("Extracted Raw Text (first 1000 chars):")
        st.write(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)

        st.subheader(f"🔹 Text Chunks ({len(chunks)})")
        st.write(chunks[:5])  # show only first few chunks
    else:
        st.warning("Please upload a PDF file.")
