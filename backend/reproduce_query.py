import requests
import time
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
UPLOAD_URL = f"{BASE_URL}/upload/"
QUERY_URL = f"{BASE_URL}/query/"
PDF_FILE = "test.pdf"

def create_dummy_pdf():
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(PDF_FILE)
    c.drawString(100, 750, "This is a test PDF document for RAG system debugging.")
    c.drawString(100, 730, "The secret code is: ALPHA-BETA-GAMMA.")
    c.save()
    print(f"Created dummy PDF: {PDF_FILE}")

def upload_pdf():
    print(f"Uploading {PDF_FILE}...")
    with open(PDF_FILE, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(UPLOAD_URL, files=files, timeout=10)
            if response.status_code == 200:
                print("Upload success:", response.json())
                return response.json()["document_id"]
            else:
                print(f"Upload failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Upload error: {e}")
            return None

def query_pdf(document_id, query="What is the secret code?"):
    print(f"Querying: '{query}' for document {document_id}")
    payload = {
        "query": query,
        "mode": "pdf",
        "document_ids": [document_id] if document_id else [],
        "top_k": 3
    }
    
    try:
        response = requests.post(QUERY_URL, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer')}")
            print(f"Sources: {len(data.get('sources', []))}")
            if data.get('answer') and "ALPHA-BETA-GAMMA" in data.get('answer'):
                print("SUCCESS: Retrieved correct answer.")
                return True
            else:
                print("FAILURE: Answer incorrect or missing.")
                return False
        return False
    except Exception as e:
        print(f"Query Error: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists(PDF_FILE):
        create_dummy_pdf()
        
    doc_id = upload_pdf()
    if doc_id:
        # Wait a bit for indexing if async? (Though implementation seemed synchronous await)
        time.sleep(2)
        success = query_pdf(doc_id)
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
