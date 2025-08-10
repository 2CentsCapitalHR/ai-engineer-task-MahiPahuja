[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)
#  ADGM Corporate Agent – AI-Powered Document Review System

##  Overview
The **ADGM Corporate Agent** is an AI-powered tool designed to assist in **legal document review and compliance checking** for Abu Dhabi Global Market (ADGM) processes such as company incorporation, licensing, and regulatory filings.  

It uses **Retrieval-Augmented Generation (RAG)** with official ADGM reference documents to:
- Parse uploaded `.docx` and `.pdf` files
- Detect document type (e.g., Articles of Association, Board Resolution, UBO Form)
- Check against **mandatory ADGM document checklists**
- Identify **red flags & legal compliance issues**
- Insert inline comments into `.docx` files
- Produce a structured JSON/Python report
- Provide a **Streamlit-based UI** for easy interaction

---

## ⚙️ Features
1. **Document Ingestion**
   - Reads `.docx` and `.pdf` files from the `data/raw` folder
   - Extracts text content and stores embeddings in a Chroma vector DB
   - Uses RAG to match with ADGM official references

2. **Document Classification**
   - Identifies document type from predefined categories:
     - Articles of Association (AoA)
     - Memorandum of Association (MoA)
     - Board Resolution
     - Shareholder Resolution
     - Incorporation Application Form
     - UBO Declaration Form
     - Register of Members
     - Register of Directors
     - Change of Registered Office Address
     - Register of Charges
     - Register of Directors – Residential Addresses

3. **Checklist Verification**
   - Detects missing mandatory documents for each legal process
   - Notifies user of which files are missing

4. **Red Flag Detection**
   - Finds issues like:
     - Missing clauses
     - Incorrect jurisdiction
     - Ambiguous language
     - Missing signatures
     - Non-ADGM compliant wording
   - Cites the relevant ADGM regulation or guideline

5. **Document Annotation**
   - Adds inline comments into `.docx` files at the exact location of issues
   - Saves reviewed files into `data/reviewed/`

6. **Structured Output**
   - Generates `report_issues.json` under `data/reports/` with:
     - Process name
     - Document checklist
     - Missing docs
     - All detected issues (with severity, snippet, and suggestion)

7. **User Interface**
   - Built with **Streamlit**
   - Upload `.docx` files directly via browser
   - Download:
     - Reviewed `.docx` with comments
     - JSON/Python report
