import os
from src.tools.checklist import check_required_documents

if __name__ == "__main__":
    # Get absolute path to 'data/raw' folder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw")

    # Check if the folder exists
    if not os.path.exists(RAW_FOLDER):
        print(f" Error: RAW folder not found at {RAW_FOLDER}")
        exit(1)

    # Run the checklist
    result = check_required_documents(RAW_FOLDER)

    print("\n Detected files and their document types:")
    for fname, dtype in result["detected"].items():
        print(f"- {fname}: {dtype}")

    print("\n Found document types:")
    for f in result["found"]:
        print(f"  - {f}")

    print("\n Missing document types:")
    for m in result["missing"]:
        print(f"  - {m}")
