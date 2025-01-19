import subprocess
import time
import logging
from datetime import datetime
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DailyAnalysisRunner:
    def __init__(self):
        self.scripts = [
            "01_collect_bestsellers.py",  # ~1 hour
            "02_data_cleaning.py",        # Data cleaning and standardization
            "03_price_analysis.py",       # Price analysis and exports
            "04_genre_analysis.py",       # Genre analysis and exports
            "05_seasonal_analysis.py"     # Seasonal analysis and exports
        ]
        
        # Create required directories
        self.directories = [
            '../data/raw/daily_bestsellers',
            '../data/processed',
            '../data/powerbi',
            '../logs'
        ]
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in self.directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Checked/created directory: {directory}")

    def run_script(self, script_name, timeout=7200):  # 2 hour timeout
        """Run a single script with timeout and output capture"""
        start_time = time.time()
        logger.info(f"Starting {script_name}")
        
        try:
            # Run the script with timeout
            process = subprocess.Popen(
                [sys.executable, script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Stream output in real-time
            while True:
                if process.poll() is not None:
                    break
                    
                # Check timeout
                if time.time() - start_time > timeout:
                    process.kill()
                    logger.error(f"{script_name} timed out after {timeout} seconds")
                    return False
                
                # Read output
                output = process.stdout.readline()
                if output:
                    logger.info(output.strip())
                
                time.sleep(0.1)
            
            # Get final return code
            return_code = process.poll()
            
            if return_code == 0:
                duration = time.time() - start_time
                logger.info(f"Successfully completed {script_name} in {duration:.2f} seconds")
                return True
            else:
                _, stderr = process.communicate()
                logger.error(f"Script {script_name} failed with return code {return_code}")
                logger.error(f"Error output: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running {script_name}: {str(e)}")
            return False

    def run_daily_analysis(self):
        """Run all scripts in sequence"""
        start_time = time.time()
        success = True
        
        logger.info(f"Starting daily analysis run at {datetime.now()}")
        
        for script in self.scripts:
            if not self.run_script(script):
                logger.error(f"Pipeline failed at {script}")
                success = False
                break
            
            # Add delay between scripts
            time.sleep(10)
        
        duration = time.time() - start_time
        status = "completed successfully" if success else "failed"
        logger.info(f"Daily analysis {status} in {duration:.2f} seconds")
        
        # Write completion status file
        status_file = Path('../data/processed/last_run_status.txt')
        with open(status_file, 'w') as f:
            f.write(f"Last run: {datetime.now()}\nStatus: {status}\nDuration: {duration:.2f} seconds")
        
        return success

if __name__ == "__main__":
    runner = DailyAnalysisRunner()
    runner.run_daily_analysis()