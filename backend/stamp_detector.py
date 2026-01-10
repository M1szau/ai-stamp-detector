"""
YOLO v11 Stamp Detection Module
"""

from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import List, Dict, Tuple, Optional, Union
import pdf2image
import os


class StampDetector:
    """Handles stamp detection on documents using trained YOLO model"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the stamp detector
        
        Args:
            model_path: Path to the trained YOLO model. If None, uses default model.
        """
        self.project_root = Path(__file__).parent.parent
        self.models_dir = self.project_root / 'backend' / 'models'
        
        # Set up poppler path (local to project)
        self.poppler_path = Path(__file__).parent / 'poppler-25.12.0' / 'Library' / 'bin'
        if not self.poppler_path.exists():
            print(f"Warning: Poppler not found at {self.poppler_path}")
            self.poppler_path = None
        else:
            print(f"Using Poppler from: {self.poppler_path}")
        
        #Load model
        if model_path is None:
            #Look for the default trained model
            model_path = self.models_dir / 'stamp_detector_n_best.pt'

            if not Path(model_path).exists():
                possible_models = list(self.models_dir.glob('stamp_detector_*.pt'))
                if possible_models:
                    model_path = possible_models[0]
                else:
                    raise FileNotFoundError(
                        f"No trained model found in {self.models_dir}. "
                        "Please train a model first using train_model.py"
                    )
        
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        
        print(f"Loading model from: {self.model_path}")
        self.model = YOLO(str(self.model_path))
        
        # Auto-detect device: use CUDA if available, otherwise CPU
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(device)
        print(f"Using device: {device}")
        
    def detect_stamps_image(
        self,
        image: Union[str, Path, np.ndarray, Image.Image],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45
    ) -> Dict:
        """
        Detect stamps in an image
        
        Args:
            image: Image as file path, numpy array, or PIL Image
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
            
        Returns:
            Dictionary containing detection results
        """
        #Run inference
        results = self.model.predict(
            source=image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False
        )[0]
        
        #Extract detection information
        detections = []
        boxes = results.boxes
        
        for i in range(len(boxes)):
            box = boxes[i]
            
            #Get box coordinates (xyxy format)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            #Get confidence and class
            confidence = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            class_name = results.names[class_id]
            
            detections.append({
                'bbox': [float(x1), float(y1), float(x2), float(y2)],
                'confidence': confidence,
                'class': class_name,
                'class_id': class_id
            })
        
        #Get the original image with detections drawn
        annotated_image = results.plot()
        
        return {
            'detections': detections,
            'count': len(detections),
            'annotated_image': annotated_image,
            'image_shape': results.orig_shape
        }
    
    def detect_stamps_pdf(
        self,
        pdf_path: Union[str, Path],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        dpi: int = 200
    ) -> Dict:
        """
        Detect stamps in a PDF document
        
        Args:
            pdf_path: Path to the PDF file
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
            dpi: DPI for PDF to image conversion
            
        Returns:
            Dictionary containing detection results for all pages
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        #Convert PDF to images
        print(f"Converting PDF to images (DPI: {dpi})...")
        
        #Local poppler path
        poppler_kwargs = {}
        if self.poppler_path:
            poppler_kwargs['poppler_path'] = str(self.poppler_path)
        
        images = pdf2image.convert_from_path(
            str(pdf_path),
            dpi=dpi,
            fmt='jpeg',
            **poppler_kwargs
        )
        
        print(f"Processing {len(images)} pages...")
        
        #Process each page
        results_per_page = []
        total_stamps = 0
        
        for page_num, image in enumerate(images, start=1):
            print(f"Processing page {page_num}/{len(images)}...")
            
            #Convert PIL Image to numpy array
            image_np = np.array(image)
            
            #Detect stamps on this page
            page_results = self.detect_stamps_image(
                image_np,
                conf_threshold=conf_threshold,
                iou_threshold=iou_threshold
            )
            
            page_results['page_number'] = page_num
            results_per_page.append(page_results)
            total_stamps += page_results['count']
        
        return {
            'total_pages': len(images),
            'total_stamps': total_stamps,
            'pages': results_per_page,
            'has_stamps': total_stamps > 0
        }
    
    def process_upload(
        self,
        file_path: Union[str, Path],
        conf_threshold: float = 0.25,
        output_dir: Optional[Path] = None
    ) -> Dict:
        """
        Process an uploaded file (PDF or image) for stamp detection
        
        Args:
            file_path: Path to the uploaded file
            conf_threshold: Confidence threshold for detections
            output_dir: Directory to save annotated images (optional)
            
        Returns:
            Dictionary containing detection results and file paths
        """
        file_path = Path(file_path)
        file_ext = file_path.suffix.lower()
        
        if output_dir is None:
            output_dir = file_path.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        #Process based on file type
        if file_ext == '.pdf':
            results = self.detect_stamps_pdf(
                file_path,
                conf_threshold=conf_threshold
            )
            
            #Save annotated images for each page
            annotated_paths = []
            for page_result in results['pages']:
                page_num = page_result['page_number']
                output_path = output_dir / f"{file_path.stem}_page_{page_num}_annotated.jpg"
                
                #Save annotated image
                annotated_img = page_result['annotated_image']
                cv2.imwrite(str(output_path), cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))
                annotated_paths.append(str(output_path))
            
            results['annotated_paths'] = annotated_paths
            
        elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            results = self.detect_stamps_image(
                str(file_path),
                conf_threshold=conf_threshold
            )
            
            #Save annotated image
            output_path = output_dir / f"{file_path.stem}_annotated{file_ext}"
            annotated_img = results['annotated_image']
            cv2.imwrite(str(output_path), cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))
            
            results['annotated_path'] = str(output_path)
            results['total_pages'] = 1
            results['total_stamps'] = results['count']
            results['has_stamps'] = results['count'] > 0
        
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        return results
    
    @staticmethod
    def image_to_base64(image: Union[np.ndarray, str, Path]) -> str:
        """
        Convert image to base64 string for API responses
        
        Args:
            image: Image as numpy array or file path
            
        Returns:
            Base64 encoded string
        """
        if isinstance(image, (str, Path)):
            with open(image, 'rb') as f:
                image_bytes = f.read()
        else:
            #Convert numpy array to bytes
            is_success, buffer = cv2.imencode('.jpg', image)
            if not is_success:
                raise ValueError("Failed to encode image")
            image_bytes = buffer.tobytes()
        
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary containing model information
        """
        return {
            'model_path': str(self.model_path),
            'model_name': self.model_path.name,
            'model_type': 'YOLOv11',
            'classes': self.model.names
        }


def test_detector(image_path: str = None, pdf_path: str = None):
    """
    Test the stamp detector on an image or PDF
    
    Args:
        image_path: Path to test image (optional)
        pdf_path: Path to test PDF (optional)
    """
    detector = StampDetector()
    
    print("\nModel Info:")
    print(detector.get_model_info())
    
    if image_path:
        print(f"\nTesting on image: {image_path}")
        results = detector.detect_stamps_image(image_path)
        print(f"Detected {results['count']} stamps")
        for i, det in enumerate(results['detections'], 1):
            print(f"  {i}. {det['class']}: {det['confidence']:.2f}")
    
    if pdf_path:
        print(f"\nTesting on PDF: {pdf_path}")
        results = detector.detect_stamps_pdf(pdf_path)
        print(f"Total pages: {results['total_pages']}")
        print(f"Total stamps: {results['total_stamps']}")


if __name__ == '__main__':
    """
    Run this script directly to test the detector:
    python stamp_detector.py --image path/to/image.jpg
    python stamp_detector.py --pdf path/to/document.pdf
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Test YOLO stamp detector')
    parser.add_argument('--image', type=str, help='Path to test image')
    parser.add_argument('--pdf', type=str, help='Path to test PDF')
    
    args = parser.parse_args()
    
    if not args.image and not args.pdf:
        print("Please provide either --image or --pdf argument")
    else:
        test_detector(image_path=args.image, pdf_path=args.pdf)
