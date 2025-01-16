import requests
import logging
from datetime import datetime
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APITester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def upload_file(self, file_path):
        """Upload and process a document"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f"{self.base_url}/upload", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return {"error": str(e)}

    def set_sender(self, email, name="Test User"):
        """Set sender information"""
        try:
            data = {"sender_email": email, "sender_name": name}
            response = self.session.post(f"{self.base_url}/set_sender", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Set sender error: {str(e)}")
            return {"error": str(e)}

    def query(self, question):
        """Send a query to the API"""
        try:
            data = {"question": question}
            response = self.session.post(f"{self.base_url}/query", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            return {"error": str(e)}

def run_tests():
    """Run a complete test workflow"""
    tester = APITester()
    test_file = "your file-path"  # Keep your original path
    test_email = "test@example.com"
    
    # Test file upload
    logger.info("Testing file upload...")
    upload_result = tester.upload_file(test_file)
    logger.info(f"Upload result: {upload_result}")
    
    # Test sender registration
    logger.info("Testing sender registration...")
    sender_result = tester.set_sender(test_email)
    logger.info(f"Sender registration result: {sender_result}")
    
    # Test queries
    questions = [
        "What is the main topic of the document?",
        "Provide a summary.",
        "What are the key points?",
        "Provide a table of contents.",
        "Conclude the document."
    ]
    
    for i, question in enumerate(questions, 1):
        logger.info(f"Testing query {i}/5: {question}")
        result = tester.query(question)
        logger.info(f"Query result: {result}")
        if i % 5 == 0:
            logger.info("Payment should have been processed")

def test_error_handling():
    """Test error handling scenarios"""
    tester = APITester()
    
    # Test invalid file upload
    logger.info("Testing invalid file upload...")
    result = tester.upload_file("nonexistent.pdf")
    assert "error" in result
    
    # Test missing sender email
    logger.info("Testing missing sender email...")
    result = tester.set_sender("")
    assert "error" in result
    
    # Test query without sender
    logger.info("Testing query without sender...")
    result = tester.query("Test question")
    assert "error" in result

if __name__ == "__main__":
    logger.info("Starting API tests...")
    run_tests()
    logger.info("Testing error handling...")
    test_error_handling()
    logger.info("Tests completed!")