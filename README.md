# AI Stamp Detector

An intelligent document analysis system that automatically detects and identifies stamps in PDF documents and images using YOLOv11 deep learning model. Upload your documents and get instant stamp detection results with visual annotations.

## Features

- **AI-Powered Detection**: Uses YOLOv11 (Ultralytics) for accurate stamp detection in documents
- **Multi-Format Support**: Process both PDF documents and images (JPG, JPEG, PNG)
- **PDF Page-by-Page Analysis**: Automatically converts PDF pages to images and analyzes each page
- **Visual Annotations**: Returns annotated images with detected stamps highlighted
- **Confidence Threshold Control**: Adjustable confidence levels for detection accuracy
- **RESTful API**: Flask-based backend with CORS support for easy integration
- **Modern Web Interface**: React + TypeScript frontend with drag-and-drop file upload
- **Real-Time Results**: Get instant detection results with detailed statistics

## Current Capabilities

**Stamp Detection** - Detects stamps in PDF documents and images  
**Trained Model** - Pre-trained YOLOv11n model included (`stamp_detector_n_best.pt`)  
**API Endpoints** - Upload, analyze, and retrieve annotated results  
**PDF Processing** - Built-in Poppler integration for PDF-to-image conversion  
**GPU Support** - Automatic CUDA detection for faster processing  
**File Management** - Automatic handling of uploads and results  

## Project Structure

```
ai-stamp-detector/
├── backend/
│   ├── main.py                         # Flask API server
│   ├── stamp_detector.py               # YOLO stamp detection module
│   ├── train_model.py                  # Model training script
│   ├── requirements.txt                # Python dependencies
│   ├── models/
│   │   ├── stamp_detector_n_best.pt    # Trained YOLOv11 model
│   │   └── data.yaml                   # Dataset configuration
│   ├── poppler-25.12.0/                # PDF processing library
│   ├── uploads/                        # Uploaded files directory
│   └── results/                        # Annotated results directory
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Dashboard/
│   │   │       ├── Dashboard.tsx       # Main dashboard component
│   │   │       ├── Header.tsx          # Application header
│   │   │       ├── Description.tsx     # Feature showcase
│   │   │       ├── FileUpload.tsx      # File upload interface
│   │   │       └── Box.tsx             # UI box component
│   │   ├── App.tsx                     # Main application
│   │   └── main.tsx                    # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docs/
│   └── Stamps Dataset 2/               # Training dataset
└── README.md
```

## Tech Stack

### Backend
- **Python 3.13** - Programming language
- **Flask 3.0.0** - Web framework
- **YOLOv11 (Ultralytics)** - Deep learning model for object detection
- **PyTorch** - Deep learning framework
- **OpenCV** - Image processing
- **pdf2image** - PDF to image conversion
- **Poppler** - PDF rendering (included in project)

### Frontend
- **React 19.2.0** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite 7.2.4** - Build tool and dev server
- **Tailwind CSS 4** - Utility-first CSS framework
- **React Icons** - Icon library

## Prerequisites

- **Python 3.13** (or 3.10+)
- **Node.js v18+** and npm
- **Git** (for cloning the repository)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-stamp-detector
```

### Step 2: Setup Backend

#### 2.1 Navigate to backend directory
```bash
cd backend
```

#### 2.2 Create a Python virtual environment (recommended)
```bash
python -m venv venv
```

#### 2.3 Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 2.4 Install Python dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask and Flask-CORS
- Ultralytics (YOLOv11)
- PyTorch and torchvision
- OpenCV, NumPy, Pillow
- pdf2image
- Other required packages

#### 2.5 Verify Poppler installation

The project includes Poppler 25.12.0 in `backend/poppler-25.12.0/`. The application is configured to use this local installation automatically. Verify it exists:

```bash
# Windows
dir poppler-25.12.0\Library\bin

# macOS/Linux
ls poppler-25.12.0/Library/bin
```

You should see executables like `pdfinfo.exe`, `pdftoppm.exe`, etc.

### Step 3: Setup Frontend

#### 3.1 Open a new terminal and navigate to frontend directory
```bash
cd frontend
```

#### 3.2 Install Node.js dependencies
```bash
npm install
```

## Running the Application

### Step 1: Start the Backend Server

In the backend directory (with virtual environment activated):

```bash
python main.py
```

The Flask server will start on `http://localhost:5000`

You should see output like:
```
Using Poppler from: <path>/backend/poppler-25.12.0/Library/bin
Loading model from: <path>/backend/models/stamp_detector_n_best.pt
Using device: cuda  # or 'cpu' if no GPU
Stamp detector initialized successfully!
 * Running on http://127.0.0.1:5000
```

### Step 2: Start the Frontend Development Server

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

The Vite development server will start on `http://localhost:5173`

### Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## Usage

1. **Upload a Document**: Drag and drop a PDF or image file, or click to browse
2. **Wait for Processing**: The AI model analyzes the document page by page
3. **View Results**: See detection statistics and download annotated images with stamps highlighted

### API Endpoints

#### `POST /api/upload`
Upload and analyze a document for stamps

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF or image), `confidence` (optional, default: 0.25)

**Response:**
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
  ]
}
```

#### `GET /api/results/<filename>`
Download annotated result image

#### `GET /api/health`
Check API health status

**Response:**
```json
{
  "status": "ok",
  "model_status": "ready"
}
```

#### `GET /api/model/info`
Get information about the loaded YOLOv11 model

## Model Information

- **Model Type**: YOLOv11n (nano - optimized for speed)
- **Training Dataset**: Custom stamp dataset with annotated stamps
- **Model File**: `backend/models/stamp_detector_n_best.pt`
- **Classes**: Stamp detection (single class)
- **Input**: Images at various resolutions (auto-scaled)
- **Output**: Bounding boxes with confidence scores

## Configuration

### Adjusting Detection Confidence

In the upload request, set the `confidence` parameter (0.0 - 1.0):
- Lower values (0.15-0.25): More detections, may include false positives
- Higher values (0.5-0.75): Fewer, more confident detections

### File Size Limits

Default: 50MB per file (configurable in `backend/main.py`)

### Supported File Types

- **Images**: `.jpg`, `.jpeg`, `.png`
- **Documents**: `.pdf`

## Build for Production

### Frontend

```bash
cd frontend
npm run build
```

Output: `frontend/dist/` directory

### Backend

The backend runs with Flask. For production deployment, consider using:
- **Gunicorn** (Linux/macOS): `gunicorn -w 4 -b 0.0.0.0:5000 main:app`
- **Waitress** (Windows): `waitress-serve --listen=*:5000 main:app`

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` for packages  
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

**Problem**: Model not found error  
**Solution**: Verify `backend/models/stamp_detector_n_best.pt` exists. If missing, train a model using `train_model.py`

**Problem**: Poppler not found / PDF processing fails  
**Solution**: Ensure `backend/poppler-25.12.0/Library/bin` directory exists with executables

**Problem**: CUDA out of memory  
**Solution**: The model will automatically fall back to CPU. Restart the backend to clear GPU memory.

### Frontend Issues

**Problem**: Cannot connect to backend  
**Solution**: Ensure Flask server is running on `http://localhost:5000` and CORS is enabled

**Problem**: Build errors  
**Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

## Development

### Training a New Model

To train or retrain the stamp detection model:

```bash
cd backend
python train_model.py
```

The script will:
1. Load the dataset from `docs/Stamps Dataset 2/`
2. Train YOLOv11 model
3. Save the best model to `models/stamp_detector_n_best.pt`

### Testing the Detector

Test the stamp detector directly:

```bash
cd backend
python stamp_detector.py --pdf path/to/document.pdf
python stamp_detector.py --image path/to/image.jpg
```

### Available Frontend Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build optimized production bundle
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality checks

## Project Timeline

- **Initial Setup**: Frontend interface with React + TypeScript + Vite
- **Backend Development**: Flask API with YOLOv11 integration
- **Model Training**: Custom stamp detection model trained on annotated dataset
- **PDF Support**: Poppler integration for multi-page PDF processing
- **Current Status**: Fully functional stamp detection system

## Future Enhancements

- [ ] Stamp authenticity verification (genuine vs. fake)
- [ ] User authentication and session management
- [ ] Document history and search functionality
- [ ] Batch processing for multiple files
- [ ] Export detection reports (PDF/CSV)
- [ ] Advanced filtering by confidence level
- [ ] Mobile-responsive design improvements
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)

## Contributing

This is an academic project. Contributions are welcome for educational purposes.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## License

This project is part of an Artificial Intelligence course project (Term 5). All rights reserved.

## Acknowledgments

- **Ultralytics** - For the YOLOv11 framework
- **Roboflow** - For dataset annotation tools
- **Poppler** - For PDF rendering capabilities

## Contact & Support

For questions or issues related to this project:
- Open an issue on the GitHub repository
- Contact the development team

---

**Last Updated**: January 31, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
