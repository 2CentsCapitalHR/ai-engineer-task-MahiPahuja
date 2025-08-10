import streamlit as st
import os
import json
from src.core.run_redflags import process_uploaded_files
from src.core.add_docx_comments import add_comments_to_docs

RAW_FOLDER = os.path.join("data", "raw")
REVIEW_FOLDER = os.path.join("data", "reviewed")
REPORTS_FOLDER = os.path.join("data", "reports")

st.set_page_config(page_title="ADGM Corporate Agent", layout="wide")

st.title("🏛️ ADGM Corporate Agent")
st.markdown("Upload `.docx` files for compliance checking and red-flag analysis.")

uploaded_files = st.file_uploader("Upload .docx files", type=["docx"], accept_multiple_files=True)

if uploaded_files:
    os.makedirs(RAW_FOLDER, exist_ok=True)

    # Save uploaded files to raw folder
    for file in uploaded_files:
        file_path = os.path.join(RAW_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

    st.success(f" {len(uploaded_files)} file(s) uploaded successfully.")

    if st.button(" Run Compliance & Red-Flag Analysis"):
        st.info("Running analysis, please wait...")

        # Step 1: Run ingestion + red-flag detection
        report_path = os.path.join(REPORTS_FOLDER, "report_issues.json")
        os.makedirs(REPORTS_FOLDER, exist_ok=True)
        analysis_results = process_uploaded_files(RAW_FOLDER, report_path)

        # Step 2: Insert comments in DOCX files
        add_comments_to_docs(report_path, REVIEW_FOLDER)

        st.success(" Analysis complete!")

        # Show summary
        st.subheader(" Summary Report")
        st.json(analysis_results)

        # Download JSON
        with open(report_path, "rb") as f:
            st.download_button("⬇️ Download JSON Report", f, file_name="analysis_results.json", mime="application/json")

        # Download reviewed DOCX files
        for file in os.listdir(REVIEW_FOLDER):
            reviewed_path = os.path.join(REVIEW_FOLDER, file)
            with open(reviewed_path, "rb") as f:
                st.download_button(f"⬇️ Download Reviewed File: {file}", f, file_name=file, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
