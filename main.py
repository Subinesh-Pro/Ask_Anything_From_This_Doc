import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import logging

# Configure API Key
def configure_genai_api(api_key):
    try:
        genai.configure(api_key=api_key)
        st.success("API key configured successfully!")
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        logging.error(f"Error configuring API: {e}")

# Extract text from uploaded PDF
def extract_pdf_text(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.success("Text extracted from PDF successfully.")
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

# Generate content with Gemini model
def generate_content_with_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating content with Gemini model: {e}")
        logging.error(f"Error generating content with Gemini model: {e}")
        return "Sorry, I couldn't generate a response."

# Main Streamlit app
def main():
    st.set_page_config(page_title="Chat with PDF", layout="wide")

    # Page Title and Description
    st.title("Chat with PDF using Gemini 1.5")
    st.markdown("""Upload your PDF and ask questions about its content. The Gemini 1.5 API will provide answers based on the extracted text from the PDF.""")

    # Sidebar for easy navigation
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
            1. **Upload your PDF file**: Click the 'Upload' button to upload your PDF document.
            2. **Enter your Gemini API key**: Enter your valid Gemini API key to configure the API.
            3. **Ask questions**: After the text is extracted, ask questions about the content of the PDF.
        """)
        st.markdown("---")
        st.title("Settings:")
        api_key = st.text_input("Enter your Gemini API key:", type="password")

        # Step 2: API Key Configuration
        if api_key:
            configure_genai_api(api_key)

    # Upload PDF file (smaller section)
    st.subheader("Upload PDF File")
    pdf_file = st.file_uploader("Upload your PDF file", type="pdf", key="pdf_uploader", label_visibility="collapsed")

    # Make the file uploader smaller by controlling the UI elements' layout
    st.markdown("""
        <style>
            .stFileUploader {
                height: 100px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Only show the rest of the content if the API key and PDF are present
    if pdf_file and api_key:
        # Step 3: Extract text from PDF
        st.subheader("Extracting Text from PDF...")
        pdf_text = extract_pdf_text(pdf_file)
        
        if pdf_text:
            # Step 4: Ask a question about the PDF
            st.subheader("Ask a Question")
            question = st.text_input("What would you like to know about the PDF?")

            if question:
                # Get answer from Gemini model based on PDF context
                prompt = f"Answer the following question based on this context:\n\n{pdf_text}\n\nQuestion: {question}"
                answer = generate_content_with_gemini(prompt)

                # Display answer with a highlighted, brighter background
                st.markdown(f"""
                    <div style="background-color: #87CEEB; padding: 15px; border-radius: 5px; font-size: 18px;">
                        <strong>Answer:</strong><br>{answer}
                    </div>
                """, unsafe_allow_html=True)

    else:
        st.info("Please upload a PDF file and provide an API key to proceed.")

if __name__ == "__main__":
    main()
