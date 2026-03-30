import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import zipfile

# --- APP CONFIG ---
st.set_page_config(page_title="Accounting Smart Splitter", layout="centered")
st.title("📂 Accounting PDF Smart Splitter")
st.write("Upload a bulk PDF (e.g., a month of invoices) to split into individual, named files.")

# --- HELPER FUNCTIONS ---
def extract_metadata_placeholder(text):
    """
    Placeholder for AI extraction logic.
    In a real scenario, you'd send 'text' to Gemini/Claude here.
    """
    # For now, we'll just return a generic name.
    return "Split_Invoice"

def split_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            
            # Extract text for naming logic (First 500 chars usually enough)
            page_text = page.extract_text()[:500]
            file_name_base = extract_metadata_placeholder(page_text)
            
            # Create individual PDF in memory
            pdf_out = io.BytesIO()
            writer.write(pdf_out)
            
            # Add to Zip
            zip_file.writestr(f"{file_name_base}_Page_{i+1}.pdf", pdf_out.getvalue())
            
    return zip_buffer

# --- UI LAYOUT ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if st.button("🚀 Process and Split"):
        with st.spinner("Analyzing and splitting..."):
            zip_data = split_pdf(uploaded_file)
            
            st.success("Extraction Complete!")
            st.download_button(
                label="📥 Download All as ZIP",
                data=zip_data.getvalue(),
                file_name="processed_invoices.zip",
                mime="application/zip"
            )

# --- INSTRUCTIONS ---
with st.expander("How to use this tool"):
    st.markdown("""
    1. **Upload** a multi-page PDF document.
    2. The app iterates through **every page**.
    3. It prepares a **ZIP file** where each page is a separate PDF.
    4. **Next Step**: Integrate an LLM API to replace 'Split_Invoice' with actual vendor names.
    """)
