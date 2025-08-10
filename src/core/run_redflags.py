import os
import json
from src.tools.doc_parser import parse_raw_folder
from src.tools.redflag_rules import run_redflag_scan

REQUIRED_DOCS = [
    "Articles of Association (AoA)",
    "Memorandum of Association (MoA)",
    "Board Resolution",
    "Shareholder Resolution",
    "Incorporation Application Form",
    "UBO Declaration Form",
    "Register of Members",
    "Register of Directors",
    "Register of Directors – Residential Addresses",
    "Register of Charges",
    "Change of Registered Office Address"
]

def process_uploaded_files(raw_folder, output_json):
    detected_files = parse_raw_folder(raw_folder)
    issues = run_redflag_scan(raw_folder, detected_files)

    # Check missing docs
    found_doc_types = set(detected_files.values())
    missing_docs = [doc for doc in REQUIRED_DOCS if doc not in found_doc_types]

    report = {
        "documents_uploaded": len(detected_files),
        "required_documents": len(REQUIRED_DOCS),
        "missing_documents": missing_docs,
        "documents_detected": detected_files,
        "issues_found": issues
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report

if __name__ == "__main__":
    RAW_FOLDER = os.path.join("data", "raw")
    REPORT_PATH = os.path.join("data", "reports", "report_issues.json")
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    print(process_uploaded_files(RAW_FOLDER, REPORT_PATH))
