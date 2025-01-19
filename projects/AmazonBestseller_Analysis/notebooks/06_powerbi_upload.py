import msal
import requests
import json
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/powerbi_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PowerBIUploader:
    def __init__(self):
        self.workspace_id = "f807765b-a960-448c-81ee-9193a6c52b4c"
        self.powerbi_url = "https://api.powerbi.com/v1.0/myorg"
        self.scope = ["https://analysis.windows.net/powerbi/api/.default"]
        
        # Directory containing the CSV files
        self.data_dir = Path('../data/powerbi')
        
        # Store dataset IDs after creation
        self.dataset_ids = {}
    
    def get_token(self):
        """Get authentication token using device code flow"""
        app = msal.PublicClientApplication(
            "51bb465f-8900-4d5f-8bf6-297d42f81179"  # Default PowerBI App ID
        )
        
        flow = app.initiate_device_flow(scopes=self.scope)
        print(flow['message'])
        
        # This will block until user completes auth flow
        result = app.acquire_token_by_device_flow(flow)
        
        if "access_token" not in result:
            raise Exception("Could not authenticate")
            
        return result["access_token"]
    
    def create_dataset(self, name, df):
        """Create a new dataset in PowerBI"""
        logger.info(f"Creating dataset: {name}")
        
        # Generate schema from DataFrame
        columns = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            if 'int' in dtype:
                data_type = 'Int64'
            elif 'float' in dtype:
                data_type = 'Double'
            elif 'datetime' in dtype:
                data_type = 'DateTime'
            else:
                data_type = 'String'
            
            columns.append({
                "name": col,
                "dataType": data_type
            })
        
        # Dataset definition
        dataset_def = {
            "name": name,
            "tables": [{
                "name": name,
                "columns": columns
            }]
        }
        
        # Create dataset
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{self.powerbi_url}/groups/{self.workspace_id}/datasets",
            headers=headers,
            json=dataset_def
        )
        
        if response.status_code != 201:
            logger.error(f"Failed to create dataset: {response.text}")
            raise Exception("Dataset creation failed")
            
        dataset_id = response.json()['id']
        logger.info(f"Created dataset with ID: {dataset_id}")
        return dataset_id
    
    def update_dataset(self, dataset_id, name, df):
        """Update existing dataset with new data"""
        logger.info(f"Updating dataset: {name}")
        
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Convert DataFrame to JSON
        data = {
            "rows": df.to_dict('records')
        }
        
        response = requests.post(
            f"{self.powerbi_url}/groups/{self.workspace_id}/datasets/{dataset_id}/tables/{name}/rows",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to update dataset: {response.text}")
            raise Exception("Dataset update failed")
            
        logger.info(f"Successfully updated dataset: {name}")
    
    def process_files(self):
        """Process all CSV files in the powerbi directory"""
        today = datetime.now().strftime('%Y%m%d')
        
        # Find all CSV files from today
        csv_files = list(self.data_dir.glob(f'*_{today}.csv'))
        
        if not csv_files:
            logger.warning(f"No CSV files found for date: {today}")
            return
        
        logger.info(f"Found {len(csv_files)} files to process")
        
        for file_path in csv_files:
            try:
                # Extract name from filename (remove date and extension)
                name = file_path.stem.rsplit('_', 1)[0]
                
                # Read CSV
                df = pd.read_csv(file_path)
                
                # Create or update dataset
                if name not in self.dataset_ids:
                    dataset_id = self.create_dataset(name, df)
                    self.dataset_ids[name] = dataset_id
                    time.sleep(5)  # Wait for dataset creation to complete
                
                self.update_dataset(self.dataset_ids[name], name, df)
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")

def main():
    try:
        uploader = PowerBIUploader()
        uploader.process_files()
        logger.info("Upload process completed successfully")
    except Exception as e:
        logger.error(f"Upload process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()