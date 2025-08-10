from .doc_parser import parse_raw_folder

REQUIRED_DOCUMENTS = [
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

def check_required_documents(raw_folder: str):
    detected_docs = parse_raw_folder(raw_folder)
    found_types = set(detected_docs.values()) - {"Unknown"}
    missing = [doc for doc in REQUIRED_DOCUMENTS if doc not in found_types]

    print("\n✅ Found document types:")
    for doc in sorted(found_types):
        print(f"  - {doc}")

    print("\n❌ Missing document types:")
    for doc in sorted(missing):
        print(f"  - {doc}")

    return {
        "detected": detected_docs,
        "found": list(found_types),
        "missing": missing
    }


