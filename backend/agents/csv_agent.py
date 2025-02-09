import pandas as pd
from io import StringIO
import os
import numpy as np

def clean_data(request: str, data: str = None) -> dict:
    try:
        if data is None:
            return {"error": "No CSV data provided"}
        
        # Read the CSV data
        df = pd.read_csv(StringIO(data))
        
        # Store original shape
        original_shape = df.shape
        
        # Basic cleaning operations
        # 1. Remove duplicate rows
        df = df.drop_duplicates()
        
        # 2. Handle missing values
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].mean())
        
        # Fill remaining non-numeric missing values with empty string
        df = df.fillna('')
        
        # 3. Save cleaned dataset locally
        output_path = os.path.join(os.getcwd(), 'cleaned_dataset.csv')
        df.to_csv(output_path, index=False)
        
        # 4. Prepare cleaning summary
        cleaning_summary = {
            "original_rows": int(original_shape[0]),  # Convert to standard Python int
            "cleaned_rows": int(df.shape[0]),
            "duplicates_removed": int(original_shape[0] - df.shape[0]),
            "columns": list(df.columns),
            "missing_values_filled": int(df.isnull().sum().sum())
        }
        
        # Convert DataFrame to dict with standard Python types
        sample_df = df.head(3).copy()
        for col in sample_df.select_dtypes(include=[np.number]).columns:
            sample_df[col] = sample_df[col].astype(float)
        
        return {
            "message": "Dataset cleaned successfully",
            "sample": sample_df.to_dict('records'),
            "shape": (int(df.shape[0]), int(df.shape[1])),  # Convert to standard Python tuple
            "cleaning_summary": cleaning_summary,
            "cleaned_file_path": output_path
        }
        
    except Exception as e:
        return {"error": f"Error cleaning data: {str(e)}"} 