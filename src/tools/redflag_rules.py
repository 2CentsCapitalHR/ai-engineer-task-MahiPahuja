# src/tools/redflag_rules.py

from src.tools.doc_parser import parse_raw_folder, read_docx_text, read_pdf_text

# Example placeholder rules
RULES = [
    {"id": "signature-block", "name": "Signature block", "keyword": "signature"},
    {"id": "jurisdiction-adgm", "name": "ADGM jurisdiction present", "keyword": "adgm"},
]

def run_redflag_scan(folder_path):
    detected_docs = parse_raw_folder(folder_path)
    issues = []

    for filename, doc_type in detected_docs.items():
        file_path = f"{folder_path}/{filename}"
        content = ""
        if filename.lower().endswith(".docx"):
            content = read_docx_text(file_path)
        elif filename.lower().endswith(".pdf"):
            content = read_pdf_text(file_path)

        for rule in RULES:
            if rule["keyword"] not in content.lower():
                issues.append({
                    "document": filename,
                    "document_type": doc_type,
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "severity": "Medium",
                    "issue": f"Required item not found: {rule['name']}",
                    "suggestion": f"Add {rule['name']} to comply with ADGM rules."
                })

    return detected_docs, issues
