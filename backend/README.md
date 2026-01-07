# Backend - Stamp Detector API

Flask-based REST API for processing PDF files and detecting stamps.

## Setup

### 1. Activate Virtual Environment

**Windows:**
```bash
cd backend
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python main.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Upload PDF File
**POST** `/api/upload`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF)

**Response (Success - 200):**
```json
{
  "message": "File uploaded successfully",
  "filename": "document.pdf",
  "filepath": "/path/to/uploads/document.pdf"
}
```

**Response (Error - 400/500):**
```json
{
  "error": "Error message"
}
```

### Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "ok"
}
```

## Project Structure
```
backend/
├── main.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── uploads/           # Uploaded PDF files (auto-created)
├── venv/              # Virtual environment
└── README.md          # This file
```

## Notes
- Only PDF files are accepted
- Maximum file size: 50MB
- Files are saved in the `uploads/` folder
- CORS is enabled for frontend integration

## Future Features
- PDF to image conversion
- Stamp detection using ML model
- Stamp analysis and reporting
