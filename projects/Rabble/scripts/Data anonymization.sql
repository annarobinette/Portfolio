-- 1. Create audit table for deletion requests
CREATE TABLE deletion_requests (
    request_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP,
    status VARCHAR(50),
    justification TEXT
);

-- 2. Anonymize user profile
UPDATE users
SET 
    first_name = 'User',
    last_name = 'Removed',
    email = NULL,
    phone = NULL,
    address = NULL,
    emergency_contact = NULL,
    medical_info = NULL,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = ?;

-- 3. Remove personal data while maintaining attendance records
UPDATE attendance
SET 
    notes = NULL,
    special_requirements = NULL
WHERE user_id = ?;

-- 4. Anonymize comments/feedback
UPDATE comments
SET 
    comment_text = 'Comment removed',
    personal_info = NULL
WHERE user_id = ?;

-- 5. Remove marketing preferences
DELETE FROM marketing_preferences
WHERE user_id = ?;

-- 6. Clear personal data from payments while maintaining records
UPDATE payments
SET 
    payment_method_details = NULL,
    billing_address = NULL,
    contact_email = NULL
WHERE user_id = ? 
AND payment_date < CURRENT_DATE - INTERVAL '7 years';

-- 7. Create anonymization log
INSERT INTO data_deletion_log (
    user_id,
    deletion_date,
    retained_data_justification
)
VALUES (
    ?,
    CURRENT_TIMESTAMP,
    'Financial records retained for 7 years per legal requirement. Anonymized attendance records maintained for statistical purposes.'
);

-- Example Python code for GCS data anonymization
import pandas as pd
from google.cloud import storage

def anonymize_gcs_data(user_id, bucket_name):
    """Anonymize user data in GCS CSV files"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # List relevant blobs
    blobs = bucket.list_blobs(prefix='data/')
    
    for blob in blobs:
        if not blob.name.endswith('.csv'):
            continue
            
        # Download and process file
        df = pd.read_csv(f'gs://{bucket_name}/{blob.name}')
        
        if 'user_id' in df.columns:
            # Anonymize personal columns while keeping user_id
            personal_columns = ['name', 'email', 'phone', 'address']
            for col in personal_columns:
                if col in df.columns:
                    df.loc[df['user_id'] == user_id, col] = 'Removed'
            
            # Upload anonymized file
            df.to_csv(f'gs://{bucket_name}/{blob.name}', index=False)

# Example Cloud Composer task for anonymization
def anonymize_user_data(user_id, **context):
    """Airflow task to anonymize user data"""
    # Execute SQL anonymization
    with get_sql_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET first_name = 'User'...")
    
    # Anonymize GCS data
    anonymize_gcs_data(user_id, 'your-bucket-name')