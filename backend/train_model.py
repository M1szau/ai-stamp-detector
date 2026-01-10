"""
YOLO v11 Model Training Module
This module handles training the YOLOv11 model for stamp detection on documents.
"""

from ultralytics import YOLO
import os
from pathlib import Path
import yaml
import shutil


class StampModelTrainer:
    """Handles training of YOLO model for stamp detection"""
    
    def __init__(self, model_name='yolo11n.pt'):
        """
        Initialize the trainer
        
        Args:
            model_name: Pre-trained YOLO model to start from (yolo11n.pt, yolo11s.pt, yolo11m.pt, etc.)
        """
        self.model_name = model_name
        self.model = None
        self.project_root = Path(__file__).parent.parent
        self.models_dir = self.project_root / 'backend' / 'models'
        self.models_dir.mkdir(exist_ok=True)
        
    def prepare_dataset_config(self, dataset_path, output_path=None):
        """
        Prepare and validate the dataset configuration file
        
        Args:
            dataset_path: Path to the dataset directory containing data.yaml
            output_path: Optional path to save the updated data.yaml
            
        Returns:
            Path to the prepared data.yaml file
        """
        dataset_path = Path(dataset_path)
        yaml_path = dataset_path / 'data.yaml'
        
        if not yaml_path.exists():
            raise FileNotFoundError(f"data.yaml not found in {dataset_path}")
        
        #Read the existing yaml
        with open(yaml_path, 'r') as f:
            data_config = yaml.safe_load(f)
        
        #Update paths to be absolute
        data_config['path'] = str(dataset_path.absolute())
        data_config['train'] = 'train/images'
        data_config['val'] = 'valid/images'
        data_config['test'] = 'test/images'
        
        #Save updated config
        if output_path is None:
            output_path = self.models_dir / 'data.yaml'
        
        with open(output_path, 'w') as f:
            yaml.dump(data_config, f, default_flow_style=False)
        
        print(f"Dataset config prepared at: {output_path}")
        return output_path
    
    def train(
        self,
        data_yaml_path,
        epochs=100,
        imgsz=640,
        batch=16,
        patience=50,
        save_period=10,
        device='cpu',
        name='stamp_detector'
    ):
        """
        Train the YOLO model
        
        Args:
            data_yaml_path: Path to the data.yaml configuration file
            epochs: Number of training epochs
            imgsz: Image size for training
            batch: Batch size
            patience: Early stopping patience
            save_period: Save checkpoint every N epochs
            device: 'cpu' or 'cuda' for GPU
            name: Name for the training run
            
        Returns:
            Path to the best trained model
        """
        print(f"\n{'='*60}")
        print(f"Starting YOLO v11 Training")
        print(f"{'='*60}")
        print(f"Model: {self.model_name}")
        print(f"Dataset: {data_yaml_path}")
        print(f"Epochs: {epochs}")
        print(f"Image Size: {imgsz}")
        print(f"Batch Size: {batch}")
        print(f"Device: {device}")
        print(f"{'='*60}\n")
        
        #Load pre-trained model
        self.model = YOLO(self.model_name)
        
        #Train the model
        results = self.model.train(
            data=str(data_yaml_path),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=patience,
            save_period=save_period,
            device=device,
            project=str(self.models_dir / 'runs'),
            name=name,
            exist_ok=True,
            plots=True,
            val=True,
            save=True,
            save_txt=True,
            save_conf=True
        )
        
        #Get the best model path
        best_model_path = self.models_dir / 'runs' / name / 'weights' / 'best.pt'
        
        #Copy the best model to a standard location
        final_model_path = self.models_dir / f'{name}_best.pt'
        if best_model_path.exists():
            shutil.copy(best_model_path, final_model_path)
            print(f"\n{'='*60}")
            print(f"Training completed successfully!")
            print(f"Best model saved to: {final_model_path}")
            print(f"{'='*60}\n")
        
        return final_model_path
    
    def validate(self, model_path, data_yaml_path):
        """
        Validate the trained model
        
        Args:
            model_path: Path to the trained model
            data_yaml_path: Path to the data.yaml configuration file
            
        Returns:
            Validation metrics
        """
        model = YOLO(str(model_path))
        metrics = model.val(data=str(data_yaml_path))
        
        print(f"\n{'='*60}")
        print(f"Validation Results")
        print(f"{'='*60}")
        print(f"mAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")
        print(f"Precision: {metrics.box.mp:.4f}")
        print(f"Recall: {metrics.box.mr:.4f}")
        print(f"{'='*60}\n")
        
        return metrics


def train_stamp_detector(
    dataset_name='Stamps Dataset 2',
    model_size='n',  # n, s, m, l, x
    epochs=100,
    batch=16,
    device='cpu'
):
    """
    Convenience function to train a stamp detector
    
    Args:
        dataset_name: Name of the dataset folder in docs/
        model_size: YOLO model size (n=nano, s=small, m=medium, l=large, x=xlarge)
        epochs: Number of training epochs
        batch: Batch size
        device: 'cpu' or 'cuda'
        
    Returns:
        Path to the trained model
    """
    #Setup paths
    project_root = Path(__file__).parent.parent
    dataset_path = project_root / 'docs' / dataset_name
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    #Initialize trainer
    model_name = f'yolo11{model_size}.pt'
    trainer = StampModelTrainer(model_name=model_name)
    
    #Prepare dataset config
    data_yaml = trainer.prepare_dataset_config(dataset_path)
    
    #Train the model
    model_path = trainer.train(
        data_yaml_path=data_yaml,
        epochs=epochs,
        batch=batch,
        device=device,
        name=f'stamp_detector_{model_size}'
    )
    
    #Validate the model
    trainer.validate(model_path, data_yaml)
    
    return model_path


if __name__ == '__main__':
    """
    Run this script directly to train the model:
    python train_model.py
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Train YOLO v11 for stamp detection')
    parser.add_argument('--dataset', type=str, default='Stamps Dataset 2',
                      help='Dataset folder name in docs/')
    parser.add_argument('--model', type=str, default='n',
                      choices=['n', 's', 'm', 'l', 'x'],
                      help='Model size (n=nano, s=small, m=medium, l=large, x=xlarge)')
    parser.add_argument('--epochs', type=int, default=100,
                      help='Number of training epochs')
    parser.add_argument('--batch', type=int, default=16,
                      help='Batch size')
    parser.add_argument('--device', type=str, default='cpu',
                      help='Device to use (cpu or cuda)')
    
    args = parser.parse_args()
    
    print("Starting stamp detector training...")
    model_path = train_stamp_detector(
        dataset_name=args.dataset,
        model_size=args.model,
        epochs=args.epochs,
        batch=args.batch,
        device=args.device
    )
    print(f"\nTraining complete! Model saved at: {model_path}")
