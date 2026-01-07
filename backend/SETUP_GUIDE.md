# Stamp Detector - Backend Setup Guide for Team

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-stamp-detector/backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```
`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
python main.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Upload PDF File
```
POST /api/upload
Content-Type: multipart/form-data

Body: file (PDF)
```

**Success Response (200):**
```json
{
  "message": "File uploaded successfully",
  "filename": "document.pdf",
  "filepath": "/path/to/uploads/document.pdf"
}
```

### Health Check
```
GET /api/health
```

## Project Structure
```
backend/
├── main.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── uploads/           # Uploaded PDF files (auto-created, not tracked)
├── venv/              # Virtual environment (not tracked)
└── README.md          # This file
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update `.env` with your local settings if needed

## Deactivate Virtual Environment
```bash
deactivate
```

## Troubleshooting

**Port 5000 already in use:**
- Change `SERVER_PORT` in `.env` and update `API_URL` in frontend accordingly

**Module not found errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**CORS errors in frontend:**
- Check `CORS_ORIGINS` in `.env.example`
- Ensure frontend is running on the correct port

## Frontend Connection
The frontend is configured to connect to `http://localhost:5000`. 
To run the full application:

1. Start backend:
```bash
cd backend
python main.py
```

2. In another terminal, start frontend:
```bash
cd frontend
npm install
npm run dev
```

## Next Steps
- Add PDF processing logic in `main.py`
- Implement stamp detection model
- Add database integration if needed
