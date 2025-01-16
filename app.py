from flask import Flask, request, jsonify
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
import stripe
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
import os
from pathlib import Path
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
stripe.api_key = Config.STRIPE_KEY

class QueryEngineInstance:
    def __init__(self, model=Config.MODEL_NAME, embedding_model=Config.EMBEDDING_MODEL):
        self.llm = Groq(model=model)
        self.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
        
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
        self.index = None
        self.memory = None
        self.query_engine = None
        self._initialize()
    
    def _initialize(self):
        """Initialize memory and create empty index"""
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        self.initialize_memory()
        self.create_query_engine()

    def load_documents(self, file_path):
        """Load documents with error handling"""
        try:
            logger.info(f"Loading documents from {file_path}")
            documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
            self.index = VectorStoreIndex.from_documents(documents)
            self.create_query_engine()
            return True
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            return False

    def initialize_memory(self):
        """Initialize memory buffer with error handling"""
        try:
            self.memory = ChatMemoryBuffer.from_defaults()
            return True
        except Exception as e:
            logger.error(f"Error initializing memory: {str(e)}")
            return False

    def create_query_engine(self, similarity_top_k=3):
        """Create query engine with error handling"""
        try:
            if not self.index:
                self.index = VectorStoreIndex.from_documents([])
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=similarity_top_k,
                memory=self.memory
            )
            return True
        except Exception as e:
            logger.error(f"Error creating query engine: {str(e)}")
            return False

    def query(self, question):
        """Query with enhanced response"""
        if not self.query_engine:
            raise ValueError("Query engine not initialized")
        try:
            response = self.query_engine.query(question)
            return {
                "answer": str(response),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            raise

class PaymentHandler:
    def __init__(self, receiver_instance, price_per_5_questions):
        self.receiver_instance = receiver_instance
        self.price_per_5_questions = price_per_5_questions
        self.question_count = 0
        self.sender = None
        self._payment_lock = False

    def set_sender(self, sender_email, sender_name="Sender Name"):
        """Set sender with validation and error handling"""
        try:
            customer = stripe.Customer.create(
                email=sender_email,
                name=sender_name,
                metadata={"registration_date": datetime.utcnow().isoformat()}
            )
            self.sender = customer
            logger.info(f"Sender set: {sender_email}")
            return {"customer_id": customer.id, "email": customer.email}
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise

    def process_payment(self):
        """Process payment with error handling"""
        if not self.sender:
            raise ValueError("Sender not initialized")
            
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=self.price_per_5_questions,
                currency="usd",
                customer=self.sender.id,
                payment_method="pm_card_visa",
                confirm=True,
                off_session=True,
                metadata={
                    "questions_count": self.question_count,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            logger.info(f"Payment processed: {payment_intent.id}")
            return payment_intent
        except stripe.error.StripeError as e:
            logger.error(f"Payment processing error: {str(e)}")
            raise

    def track_question_and_charge(self, question):
        """Track questions and handle payments"""
        if not self.sender:
            raise ValueError("Sender not initialized")
        
        self.question_count += 1
        response = self.receiver_instance.query(question)
        
        if self.question_count % 5 == 0:
            payment_result = self.process_payment()
            response["payment"] = {
                "status": payment_result.status,
                "amount": payment_result.amount / 100
            }
            
        return response

# Initialize components
Path(Config.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
receiver_instance = QueryEngineInstance()
handler = PaymentHandler(receiver_instance, price_per_5_questions=100)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if not file or not file.filename:
        return jsonify({"error": "Invalid file"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
        
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        if receiver_instance.load_documents(file_path):
            return jsonify({"message": "File uploaded and processed successfully"})
        else:
            return jsonify({"error": "Error processing file"}), 500
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/set_sender', methods=['POST'])
def set_sender():
    try:
        data = request.json
        if not data or 'sender_email' not in data:
            return jsonify({"error": "sender_email is required"}), 400
            
        result = handler.set_sender(
            data['sender_email'],
            data.get('sender_name', 'Sender Name')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in set_sender: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        if not data or 'question' not in data:
            return jsonify({"error": "question is required"}), 400
            
        response = handler.track_question_and_charge(data['question'])
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in query: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)