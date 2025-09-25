import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    print(text_splitter.split_text(text))
    return text_splitter.split_text(text)




# streamlit
st.title("PowerPoint generation with AI")
prompt = st.text_input("Enter your prompt:")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
num_slides = st.number_input("Number of slides:", min_value=1, max_value=50, value=5)
if st.button("Process PDF"):
    if uploaded_file is not None:
        raw_text = extract_pdf_text(uploaded_file)
        chunks = get_text_chunks(raw_text)

        st.success("✅ PDF processed successfully!")
        
        # Preview
        st.subheader("Extracted Raw Text (first 1000 chars):")
        st.write(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)

        st.subheader(f"🔹 Text Chunks ({len(chunks)})")
        st.write(chunks[:5])  # show only first few chunks
    else:
        st.warning("Please upload a PDF file.")
