import streamlit as st

# Page title
st.title("📊 Simple Streamlit Dashboard")

# Prompt input
prompt = st.text_input("Enter your prompt:")

# File uploader (PDF, DOCX, PPTX, TXT, etc.)
uploaded_file = st.file_uploader(
    "Upload a document (pdf, docx, pptx, txt)", 
    type=["pdf", "docx", "pptx", "txt"]
)

# Number input for slides
num_slides = st.number_input(
    "Number of slides to generate:", 
    min_value=1, 
    max_value=50, 
    value=5, 
    step=1
)

# Submit button
if st.button("Generate"):
    st.write("### 🔹 Input Summary")
    st.write(f"**Prompt:** {prompt}")
    st.write(f"**Number of slides:** {num_slides}")
    if uploaded_file:
        st.write(f"**Uploaded file:** {uploaded_file.name}")
    else:
        st.write("No file uploaded.")

    st.success("✨ Ready to process your request!")
