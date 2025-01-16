# Smart Query Engine

Smart Query Engine is a robust Python application that enables document processing and intelligent query handling using embedding models. It supports file uploads, tracks query usage, and integrates Stripe for secure payment processing. Built with Flask, it is ideal for applications requiring intelligent document interaction.

---

## Features

- **File Uploads**: Supports PDF, text, and markdown files up to 10 MB.
- **Query Processing**: Leverages advanced embedding models for intelligent query resolution.
- **Payment Integration**: Tracks queries and processes payments using Stripe.
- **Customizable Models**: Easily switch between different NLP and embedding models.
- **Secure & Scalable**: Built with Flask, with clear configuration and extensibility.

---

## Installation

Follow these steps to set up the application locally:

### Prerequisites

1. Install Python (version 3.8 or higher).
2. Install `pip` and `virtualenv` for managing dependencies.

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-query-engine.git
   cd smart-query-engine
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   
   Create a `.env` file in the project root and add the following:
   ```env
   STRIPE_KEY=your-stripe-secret-key
   MODEL_NAME=llama3-8b-8192
   EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
   UPLOAD_FOLDER=uploads
   MAX_FILE_SIZE=10485760
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Usage

### Quick Testing with `simple_usage.ipynb`

- **File**: `simple_usage.ipynb`
- **Purpose**: Simplifies testing the application's core features in a Jupyter Notebook environment.
- **How to Use**:
  1. Open the notebook:
     ```bash
     jupyter notebook simple_usage.ipynb
     ```
  2. Follow the instructions in the notebook to test:
     - File uploads.
     - Query processing.
     - API interactions.

This is especially useful for developers or testers who want to validate the application quickly without using external tools like Postman.

---

## API Endpoints

1. **`/upload`**
   - **Method**: POST
   - **Description**: Uploads a file for processing.
   - **Request**:
     ```json
     { "file": <file> }
     ```
   - **Response**:
     - Success: `{ "message": "File uploaded and processed successfully" }`
     - Error: `{ "error": "Error message" }`

2. **`/set_sender`**
   - **Method**: POST
   - **Description**: Sets sender information.
   - **Request**:
     ```json
     {
       "sender_email": "user@example.com",
       "sender_name": "John Doe"
     }
     ```
   - **Response**:
     - Success: `{ "customer_id": "cus_12345", "email": "user@example.com" }`
     - Error: `{ "error": "Error message" }`

3. **`/query`**
   - **Method**: POST
   - **Description**: Handles queries and tracks usage.
   - **Request**:
     ```json
     {
       "question": "What is the main topic of the document?"
     }
     ```
   - **Response**:
     - Success: `{ "answer": "Response text", "timestamp": "2023-01-01T00:00:00Z" }`
     - Error: `{ "error": "Error message" }`

---

## Testing

The application includes automated test scripts and a Jupyter Notebook for easy testing.

1. **Using Test Script**:
   - Run the test suite:
     ```bash
     python test.py
     ```
   - View logs to verify test results.

2. **Using Jupyter Notebook**:
   - Open `simple_usage.ipynb` for a guided testing experience.

---

## Folder Structure

```
smart-query-engine/
├── app.py                # Main Flask application
├── config.py             # Configuration settings
├── test.py               # Test suite for API
├── simple_usage.ipynb    # Jupyter Notebook for easy testing
├── uploads/              # Directory for uploaded files
├── requirements.txt      # Dependency list
├── .env                  # Environment variables (not included in repo)
├── README.md             # Project documentation
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- Flask for the web framework.
- Stripe for payment integration.
- HuggingFace for embedding models.
