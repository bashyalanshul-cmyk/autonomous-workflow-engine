import os
import pandas as pd
import numpy as np
from pathlib import Path
import uuid
from datetime import datetime
import json
from config.config import INPUT_DIR, OUTPUT_DIR


def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj


class DataProcessor:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.processed_data = {}
        self.metadata = {}
        
    def ingest_file(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_ext = file_path.suffix.lower()
        data = None
        file_info = {
            "filename": file_path.name,
            "extension": file_ext,
            "size_bytes": file_path.stat().st_size,
            "ingested_at": datetime.now().isoformat()
        }
        
        if file_ext == '.csv':
            data = pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            data = pd.read_excel(file_path)
        elif file_ext == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
            data = pd.json_normalize(data) if isinstance(data, list) else pd.DataFrame([data])
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
            
        self.processed_data[file_path.stem] = data
        self.metadata[file_path.stem] = file_info
        return data
    
    def analyze_dataset(self, df, name):
        analysis = {
            "dataset_name": name,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "column_types": df.dtypes.astype(str).to_dict(),
            "missing_values": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
            "basic_stats": df.describe(include='all').to_dict() if len(df) > 0 else {},
            "memory_usage": int(df.memory_usage(deep=True).sum())
        }
        return analysis
    
    def clean_data(self, df):
        cleaned_df = df.copy()
        cleaned_df = cleaned_df.drop_duplicates()
        
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            
        categorical_cols = cleaned_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else "Unknown")
            
        return cleaned_df
    
    def save_processed_data(self, output_subdir):
        output_path = OUTPUT_DIR / output_subdir
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, df in self.processed_data.items():
            cleaned_df = self.clean_data(df)
            cleaned_df.to_csv(output_path / f"{name}_cleaned.csv", index=False)
            
            analysis = self.analyze_dataset(cleaned_df, name)
            analysis = convert_numpy_types(analysis)
            with open(output_path / f"{name}_analysis.json", 'w') as f:
                json.dump(analysis, f, indent=2)
                
        with open(output_path / "session_metadata.json", 'w') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": self.timestamp,
                "datasets": self.metadata
            }, f, indent=2)
            
        return output_path
