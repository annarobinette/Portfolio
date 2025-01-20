import os
from datetime import datetime, timedelta
import requests
from google.cloud import storage, secretmanager
import logging
from typing import Dict, List, Tuple
import tempfile
import json

class MakeSweatPipeline:
    def __init__(self, is_historical: bool = False):
        """
        Initialize pipeline
        :param is_historical: If True, uses the backup folder for storage
        """
        self.is_historical = is_historical
        self.bucket_name = os.environ.get('GCS_BUCKET_NAME')
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        
        # Set target folder based on whether this is historical or weekly
        self.gcs_folder = 'backup' if is_historical else 'data'
        
        self.storage_client = storage.Client()
        self.secret_client = secretmanager.SecretManagerServiceClient()
        self.bucket = self.storage_client.bucket(self.bucket_name)
        
        # Load configuration from secrets
        self.config = self._load_configuration()
        
        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging"""
        log_name = 'historical_pipeline.log' if self.is_historical else 'weekly_pipeline.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_name),
                logging.StreamHandler()
            ]
        )

    def get_secret(self, secret_name: str) -> str:
        """Retrieve secret from Google Secret Manager"""
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = self.secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def _load_configuration(self) -> Dict:
        """Load all configuration from secrets"""
        try:
            # Get club IDs
            club_ids = self.get_secret('makesweat_club_ids').split(',')
            
            # Get shared credentials
            credentials = json.loads(self.get_secret('makesweat_credentials'))
            
            # Get report names
            report_names = self.get_secret('makesweat_report_names').split(',')
            
            # Get userident
            userident = self.get_secret('makesweat_userident')
            
            return {
                'club_ids': club_ids,
                'credentials': credentials,
                'report_names': report_names,
                'userident': userident
            }
        except Exception as e:
            logging.error(f"Failed to load configuration: {str(e)}")
            raise

    def get_date_range(self) -> Tuple[str, str]:
        """Get date range based on pipeline type"""
        if self.is_historical:
            # Historical data starts from 2015
            start_date = "2015-01-01"
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # Weekly data is last 7 days
            today = datetime.now()
            seven_days_ago = today - timedelta(days=7)
            start_date = seven_days_ago.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        
        return start_date, end_date

    def fetch_and_upload_report(self, club_id: str, report_name: str, 
                              start_date: str, end_date: str) -> None:
        """Fetch report and upload directly to GCS"""
        try:
            # Construct URL
            url = (f"https://makesweat.com/reports/{report_name}.php"
                  f"?clubid={club_id}&starttime={start_date}%2023:00:00"
                  f"&endtime={end_date}%2023:00:00&format=csv"
                  f"&makesweatuserident={self.config['userident']}")

            # Create session with default TLS settings
            session = requests.Session()
            
            response = session.get(url)
            response.raise_for_status()

            # Generate clean filename without any special characters
            timestamp = datetime.now().strftime('%Y%m%d')
            clean_report_name = report_name.strip()
            clean_club_id = str(club_id).strip()
            filename = f"{clean_report_name}_club{clean_club_id}_{timestamp}.csv"
            gcs_blob_name = os.path.join(self.gcs_folder, filename).replace('\\', '/')
            
            # Upload directly to GCS using a temporary file
            with tempfile.NamedTemporaryFile(mode='wb', delete=True) as temp_file:
                temp_file.write(response.content)
                temp_file.flush()
                
                # Upload to appropriate folder using clean path
                blob = self.bucket.blob(gcs_blob_name)
                blob.upload_from_filename(temp_file.name)

            logging.info(f"Successfully processed {filename}")
            
        except Exception as e:
            logging.error(f"Error processing {report_name} for club {club_id}: {str(e)}")
            raise

    def run(self):
        """Run the pipeline"""
        try:
            start_date, end_date = self.get_date_range()
            
            for club_id in self.config['club_ids']:
                logging.info(f"Processing club {club_id}")
                for report_name in self.config['report_names']:
                    self.fetch_and_upload_report(club_id, report_name, 
                                              start_date, end_date)
                    
            logging.info("Pipeline completed successfully")
            
        except Exception as e:
            logging.error(f"Pipeline failed: {str(e)}")
            raise

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run MakeSweat data pipeline')
    parser.add_argument('--historical', action='store_true', 
                       help='Run historical data pipeline')
    args = parser.parse_args()
    
    # Validate environment
    required_env_vars = [
        'GCS_BUCKET_NAME',
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    missing_vars = [var for var in required_env_vars 
                   if not os.environ.get(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    # Run pipeline
    pipeline = MakeSweatPipeline(is_historical=args.historical)
    pipeline.run()

if __name__ == "__main__":
    main()