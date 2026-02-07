import requests
import json

# Test query with document selection
BASE_URL = "http://localhost:8000/api/v1"

# Get documents first
docs_response = requests.get(f"{BASE_URL}/documents/")
print("Documents:")
print(json.dumps(docs_response.json(), indent=2))

# Find the orthodontics document
docs = docs_response.json()["documents"]
ortho_doc = [d for d in docs if "orthodontics" in d["filename"].lower()][0]
print(f"\nQuerying document: {ortho_doc['filename']}")
print(f"Document ID: {ortho_doc['id']}")

# Test query with document selection
query_payload = {
    "query": "Notions of occlusiology in orthodontics?",
    "mode": "pdf",
    "document_ids": [ortho_doc["id"]],
    "top_k": 5
}

print("\nSending query...")
print(json.dumps(query_payload, indent=2))

response = requests.post(f"{BASE_URL}/query/", json=query_payload, timeout=30)

print(f"\nStatus Code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"\nAnswer: {result['answer']}")
    print(f"\nConfidence: {result['confidence']}")
    print(f"\nSources: {len(result['sources'])}")
    for i, source in enumerate(result['sources'], 1):
        print(f"\n  Source {i}:")
        print(f"    Reference: {source['reference']}")
        print(f"    Relevance: {source.get('relevance_score', 'N/A')}")
        print(f"    Content preview: {source['content'][:100]}...")
else:
    print(f"Error: {response.text}")
