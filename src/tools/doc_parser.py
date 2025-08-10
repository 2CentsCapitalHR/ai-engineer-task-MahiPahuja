import os
import docx
import fitz  # PyMuPDF

# Direct filename-to-type mapping for tricky or oddly named files
FILENAME_MAPPING = {
    "templates_shreso_amendmentarticles-v1-20220107": "Board Resolution",
    "resolution-single-individual-shareholder-ltd-incorporation-v2": "Shareholder Resolution",
    "incorporation-by-body-corporate": "Incorporation Application Form",
    "adgm-ra-model-articles-private-company-limited-by-shares-bilingual": "Memorandum of Association (MoA)"
}

# Keywords for content/filename-based detection
DOCUMENT_KEYWORDS = {
    "Articles of Association (AoA)": [
        "articles of association", "model-articles"
    ],
    "Memorandum of Association (MoA)": [
        "memorandum of association", "moa", "memorandum"
    ],
    "Board Resolution": [
        "board resolution", "shreso", "amendmentarticles"
    ],
    "Shareholder Resolution": [
        "shareholder resolution", "shreso"
    ],
    "Incorporation Application Form": [
        "incorporation application", "incorporation-by-body-corporate", "application form"
    ],
    "UBO Declaration Form": [
        "ubo declaration", "beneficial ownership", "ultimate beneficial owner"
    ],
    "Register of Members": [
        "registerofshareholder", "register of members"
    ],
    "Register of Directors": [
        "register-of-directors", "registerofdirectors"
    ],
    "Register of Directors – Residential Addresses": [
        "registerofdirresadd", "residential addresses"
    ],
    "Register of Charges": [
        "registerofcharges", "charges"
    ],
    "Change of Registered Office Address": [
        "change-of-registered-office-address"
    ]
}

def normalize_text(text: str) -> str:
    """Lowercase and strip spaces/newlines for matching."""
    return text.lower().replace("\n", " ").strip()

def read_docx_text(filepath: str) -> str:
    """Extract text from a .docx file."""
    try:
        doc = docx.Document(filepath)
        return normalize_text(" ".join([p.text for p in doc.paragraphs]))
    except Exception as e:
        print(f"⚠️ Could not read DOCX {filepath}: {e}")
        return ""

def read_pdf_text(filepath: str) -> str:
    """Extract text from a PDF using PyMuPDF (no OCR)."""
    try:
        pdf = fitz.open(filepath)
        text = " ".join([page.get_text() for page in pdf])
        pdf.close()
        return normalize_text(text)
    except Exception as e:
        print(f"⚠️ Could not read PDF {filepath}: {e}")
        return ""

def detect_document_type(filepath: str) -> str:
    filename = normalize_text(os.path.splitext(os.path.basename(filepath))[0])  # without extension

    # 1️⃣ Check for partial match in mapping
    for key, doc_type in FILENAME_MAPPING.items():
        if key in filename:
            return doc_type

    # 2️⃣ Read content for keyword search
    content = ""
    if filepath.lower().endswith(".docx"):
        content = read_docx_text(filepath)
    elif filepath.lower().endswith(".pdf"):
        content = read_pdf_text(filepath)

    # 3️⃣ Match against keywords
    for doc_type, keywords in DOCUMENT_KEYWORDS.items():
        for kw in keywords:
            if kw in filename or kw in content:
                return doc_type

    return "Unknown"

def parse_raw_folder(folder_path: str) -> dict:
    """Parse all files in the folder and detect their types."""
    detected_files = {}
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            detected_files[file] = detect_document_type(file_path)
    return detected_files
