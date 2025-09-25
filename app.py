import streamlit as st

st.title("Powerpoint Generator")
prompt = st.text_input("Enter your prompt:")
uploaded_file = st.file_uploader(
    "Upload a document (pdf, docx, pptx, txt)", 
    type=["pdf", "docx", "pptx", "txt"]
)
num_slides = st.number_input(
    "Number of slides to generate:", 
    min_value=1, 
    max_value=50, 
    value=5, 
    step=1
)
if st.button("Generate"):
    st.write("### 🔹 Input Summary")
    st.write(f"**Prompt:** {prompt}")
    st.write(f"**Number of slides:** {num_slides}")
    if uploaded_file:
        st.write(f"**Uploaded file:** {uploaded_file.name}")
    else:
        st.write("No file uploaded.")

    st.success("✨ Ready to process your request!")
