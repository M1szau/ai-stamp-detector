# Backend - Stamp Detector API

Flask-based REST API for processing PDF files and images, detecting stamps using YOLOv11 deep learning model.

## Features

- **YOLOv11 Stamp Detection** - Trained model for accurate stamp detection
- **PDF Processing** - Automatic PDF-to-image conversion with Poppler
- **Multi-format Support** - Accepts PDF, JPG, JPEG, PNG files
- **GPU Acceleration** - Automatic CUDA detection for faster processing
- **Visual Annotations** - Returns annotated images with detected stamps highlighted

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

### Upload & Analyze Document
**POST** `/api/upload`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (PDF or image), `confidence` (optional, default: 0.25)

**Response (Success - 200):**
```json
{
  "message": "File processed successfully",
  "filename": "document.pdf",
  "has_stamps": true,
  "total_stamps": 3,
  "total_pages": 2,
  "pages": [
    {
      "page_number": 1,
      "stamps_count": 2,
      "detections": [...]
    }
  ],
  "annotated_paths": ["document_page_1.jpg", "document_page_2.jpg"]
}
```

**Response (Error - 400/500):**
```json
{
  "error": "Error message"
}
```

### Get Annotated Result Image
**GET** `/api/results/<filename>`

Returns the annotated image with detected stamps highlighted.

### Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "ok",
  "model_status": "ready"
}
```

### Model Information
**GET** `/api/model/info`

Returns information about the loaded YOLOv11 model.

## Project Structure
```
backend/
├── main.py                     # Main Flask application
├── stamp_detector.py           # YOLO stamp detection module
├── train_model.py              # Model training script
├── requirements.txt            # Python dependencies
├── models/
│   ├── stamp_detector_n_best.pt    # Trained YOLOv11 model
│   └── data.yaml               # Dataset configuration
├── poppler-25.12.0/            # PDF processing library (Windows)
├── uploads/                    # Uploaded files (auto-created)
├── results/                    # Annotated results (auto-created)
└── README.md                   # This file
```

## Notes
- PDF and image files (jpg, jpeg, png) are accepted
- Maximum file size: 50MB
- Files are saved in the `uploads/` folder
- Annotated results are saved in the `results/` folder
- CORS is enabled for frontend integration
- Poppler is bundled for Windows PDF processing

## Model Training

To train or retrain the stamp detection model:

```bash
python train_model.py
```

The script will use the dataset from `docs/Stamps Dataset 2/` and save the trained model to `models/`.
