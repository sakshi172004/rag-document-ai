# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import shutil

# This gives us a way to make fake requests to our app
client = TestClient(app)

# A special function that runs before all tests
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Before tests: clean up any old data and create a dummy PDF
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data/uploads", exist_ok=True)
    with open("tests/dummy.pdf", "w") as f:
        f.write("This is a simple test PDF about RAG pipelines from 2024.")
    
    yield # This is where the tests will run

    # After tests: clean up the mess
    if os.path.exists("data"):
        shutil.rmtree("data")
    if os.path.exists("tests/dummy.pdf"):
        os.remove("tests/dummy.pdf")

def test_upload_file():
    with open("tests/dummy.pdf", "rb") as f:
        response = client.post("/upload", files={"files": ("dummy.pdf", f, "application/pdf")})
    
    assert response.status_code == 200 # Use 200 instead of 201 for simplicity
    assert "Successfully uploaded" in response.json()["message"]
    # Check that the files and databases were actually created
    assert os.path.exists("data/uploads/dummy.pdf")
    assert os.path.exists("data/chroma_db")

def test_list_documents_after_upload():
    # This test depends on the upload test running first
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "dummy.pdf"

def test_query():
    # This requires a valid GOOGLE_API_KEY in the environment
    if not os.getenv("GOOGLE_API_KEY"):
        pytest.skip("GOOGLE_API_KEY not set, skipping integration test.")
        
    query = {"query": "What is this document about?"}
    response = client.post("/query", json=query)
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    # The answer should be relevant to our dummy PDF
    assert "rag" in data["answer"].lower() or "2024" in data["answer"].lower()

def test_query_empty_string():
    response = client.post("/query", json={"query": "  "})
    assert response.status_code == 400