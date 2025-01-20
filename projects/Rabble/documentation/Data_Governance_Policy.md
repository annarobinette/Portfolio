# Data Governance Policy
*Last Updated: January*
## 1. Introduction

This document outlines our commitment to responsible data management and protection of personal information for all our members, leaders, and staff. As a UK-based sports organization, we adhere to GDPR requirements and maintain high standards of data protection.

## 2. Data Collection Overview

### 2.1 Types of Data Collected
We collect and process the following categories of data:
- Personal identification information
- Event attendance records
- Transaction information (but not payment/banking details)
- Leader and attendee information
- Club usage statistics
- Member feedback
- Marketing preferences
- Membership passes and access informatio (peoplepasses)

### 2.2 Purpose of Data Collection
- To manage membership and attendance
- To process payments and maintain financial records
- To communicate with members about events and services
- To analyze participation patterns for service improvement
- To maintain safety and security during sports activities
- To comply with legal obligations

## 3. Data Storage and Security

### 3.1 Data Infrastructure

### 3.1.1 Data Collection and Storage
- Primary data collection through MakeSweat platform (third-party service)
- Scheduled extractions twice weekly and quarterly
- Cloud storage in Google Cloud Storage (europe-west2 region)
  - `/data/` folder for current extractions
  - `/backup/` folder for historical extractions
- Direct transfer to BigQuery without local storage
- Separate datasets in BigQuery for current and historical data

#### 3.1.2 Data Flow
1. Data collection in MakeSweat platform
2. Scheduled automated extraction
3. Secure transfer to Google Cloud Storage
4. Automated data quality validation
5. Archival and retention management

##### Data Transfer Schedules
###### Current Data Transfers
- Schedule: Every Monday and Friday at 09:45
- Destination: RabbleIngest dataset
- Write disposition: MIRROR
- File pattern matching: `[reportname]_club[clubid]_*.csv`

###### Historical Data Transfers
- Schedule: Quarterly at 09:45 (every 3 months)
- Destination: RabbleIngest_Historical dataset
- Write disposition: MIRROR
- File pattern matching: `[reportname]_club[clubid]_*.csv`

##### Transfer Configuration
- Maximum bad records per transfer: 10
- CSV parsing settings:
  - Skip header row
  - UTF-8 encoding
  - Allow jagged rows
  - Allow quoted newlines
  - Standard CSV delimiter (,)
  - Double quote character (")
- Error handling: Transfers stop after 10 bad records
- Dataset location: europe-west2 (London)

#### 3.1.3 Platform Security
- MakeSweat platform security controls and compliance
- Google Cloud Platform enterprise-grade security
- Automated pipeline monitoring and alerting
- Regular security audits of infrastructure

### 3.2 Technical Security Measures

#### 3.2.1 Authentication and Access
- Multi-factor authentication (MFA) requirement for all administrative access
- Regular password rotation policy (every 90 days)
- Password complexity requirements enforced
- Session timeout after 30 minutes of inactivity
- IP-based access restrictions for administrative functions
- Audit logging of all access attempts

#### 3.2.2 Data Encryption
- TLS 1.3 for all data in transit
- AES-256 encryption for data at rest in Google Cloud Storage
- Secure key management using Google Cloud KMS
- End-to-end encryption for sensitive data transfers
- Regular encryption protocol reviews and updates

#### 3.2.3 Infrastructure Security
- Regular automated security scanning
- Vulnerability assessments conducted quarterly
- Network segmentation between public and private resources
- Web Application Firewall (WAF) implementation
- DDoS protection
- Regular security patches and updates

#### 3.2.4 Backup and Recovery
- Daily incremental backups
- Weekly full backups
- Monthly backup restoration tests
- Geographical redundancy of backup storage
- 90-day backup retention
- Encrypted backup storage

#### 3.2.5 Monitoring and Alerts
- Real-time security event monitoring
- Automated alerts for suspicious activities
- Performance monitoring and anomaly detection
- Regular security log reviews
- Incident response team notifications
- Monthly security metrics reporting

## 4. Data Processing and Handling

### 4.1 Data Pipeline Operations

#### 4.1.1 Automated Data Collection
- Daily automated data extraction from MakeSweat
- Scheduled execution via Cloud Composer
- Automated validation and quality checks
- Error detection and notification system
- Audit logging of all data movements

#### 4.1.2 Pipeline Monitoring
- Real-time pipeline status monitoring
- Automated failure notifications
- Data quality metrics tracking
- Volume and pattern monitoring
- Performance metrics collection

#### 4.1.3 Operational Procedures
- Pipeline maintenance windows
- Version control for pipeline code
- Change management process
- Disaster recovery procedures
- Business continuity planning

### 4.2 Access Control
- Role-based access control
- Authenticated admin access
- Secure credential management
- Regular access review and monitoring

## 5. GDPR Compliance

### 5.1 Member Rights
Members have the right to:
- Access their personal data
- Request data correction
- Request data deletion
- Object to data processing
- Export their data
- Withdraw consent for optional processing

### 5.2 Data Protection Measures
- Privacy by design approach
- Data minimization principle
- Regular privacy impact assessments
- Documented data retention periods
- Clear consent management
- Regular staff training on data protection

## 6. Areas for Improvement

### 6.1 Technical Controls and Improvements

#### 6.1.1 Current Technical Controls
- Automated data pipeline using Cloud Composer
- Scheduled data extraction and processing
- Built-in error handling and retries
- Automated monitoring and alerting
- Secure cloud storage implementation

#### 6.1.2 Planned Improvements
- Enhanced data quality validation rules
- Advanced anomaly detection
- Automated data lineage tracking
- Real-time compliance monitoring
- Advanced encryption key management
- Improved audit logging and analysis

#### 6.1.3 Pipeline Security
- Service account management
- Least privilege access principles
- Regular security configuration reviews
- Automated secret rotation
- Infrastructure as Code security scanning

### 6.2 Process Improvements
- Regular data accuracy audits
- Enhanced documentation of data flows
- More detailed data processing agreements
- Regular privacy policy reviews
- Improved incident response procedures

## 7. Data Retention and Deletion

### 7.1 Data Retention Schedule

#### 7.1.1 Member Data
 **Active Member Profiles**
  - Basic profile: Duration of membership + 2 years
  - Contact details: Duration of membership + 2 years
  - Emergency contacts: Duration of membership + 6 months
  - Health information: Duration of membership + 1 year
  - Photos/media: Duration of membership + 1 year unless explicitly permitted for longer

**Inactive Member Data**
  - Basic profile: 2 years post-last activity
  - Contact details: 1 year post-last activity
  - All other personal data: 6 months post-last activity

#### 7.1.2 Financial Records
- Payment records: 7 years (legal requirement)
- Membership fee records: 7 years
- Refund records: 7 years
- Payment dispute records: 7 years from resolution
- Financial reports: 7 years

#### 7.1.3 Attendance and Activity Data
- Event attendance: 3 years
- Class bookings: 2 years
- Participation statistics: 3 years (anonymized)
- Leader attendance: 3 years
- Session feedback: 2 years

#### 7.1.4 Communication Records
- Marketing preferences: Until consent withdrawal
- Email communication history: 2 years
- Support tickets: 3 years
- Complaints: 5 years from resolution

#### 7.1.5 Technical Data
- Login records: 1 year
- System logs: 1 year
- Security event logs: 3 years
- Access logs: 2 years

#### 7.1.6 Special Categories
- Safeguarding records: 25 years or as required by law
- Accident reports: 5 years
- Medical incidents: 5 years
- Legal dispute records: 7 years from resolution

### 7.2 Deletion Procedures
- Automated removal of expired data
- Secure deletion protocols
- Documented deletion verification
- Regular deletion audits

## 8. Incident Response

### 8.1 Data Breach Response Plan
- Immediate containment procedures
- Assessment and documentation
- Notification to affected individuals
- ICO reporting if required
- Post-incident analysis and improvement

### 8.2 Contact Information
- Data Protection Officer contact details
- Incident reporting procedures
- Member support contact information

## 9. Regular Review

This policy is reviewed:
- Annually for general updates
- When significant changes occur to data processing
- After any security incidents
- When new regulations come into effect

## 11. Data Subject Rights and Requests

### 11.1 Subject Access Requests (SAR)

#### 11.1.1 Information to Include
When a member requests their personal data, provide:
- Personal profile information from peopleinfo
- Attendance history from eventattendance
- Payment records from clubpayments
- Leadership/attendance records from leadersattendees
- Club usage data from assocclubusage
- Comments/feedback from clubcomments
- Marketing preferences from gdproptin
- Membership pass information from peoplepasses
- Any email communications history
- Incident reports involving the member
- Health/safety information provided
- Emergency contact details

#### 11.1.2 Format and Delivery
- Provide data in a commonly used, machine-readable format (e.g., CSV, PDF)
- Deliver within 30 days of request
- Verify identity before sharing data
- Include explanation of data categories
- Provide context for data usage

### 11.2 Right to Erasure (Right to be Forgotten)

#### 11.2.1 Data to be Removed
- All personal identifying information
- Contact details
- Health and safety information
- Emergency contacts
- Photos and media
- Comments and feedback
- Marketing preferences
- Payment details (except where required for legal obligations)

#### 11.2.2 Data to be Retained
The following may be retained with justification:
- Anonymized attendance records (UserID replaced with 'User Removed')
- Payment records required for tax purposes (7 years)
- Safeguarding incident records (as required by law)
- Accident reports (legal requirement)
- Aggregate statistics (fully anonymized)

#### 11.2.3 Anonymization Process
1. Replace name with 'User Removed'
2. Generate anonymized identifier
3. Remove all contact information
4. Remove all personal identifiers
5. Maintain minimal record structure for integrity
6. Document anonymization process

#### 11.2.4 Legal Bases for Retention
- Legal obligation (tax records, safety records)
- Legitimate business interest (anonymized statistics)
- Public interest (safeguarding records)
- Defense of legal claims

### 11.3 Request Processing

#### 11.3.1 Verification Process
1. Confirm identity through:
   - Account login
   - Government ID
   - Email verification
   - Security questions

#### 11.3.2 Timeline
- Acknowledge request within 48 hours
- Process request within 30 days
- Communicate any delays
- Document all actions taken

#### 11.3.3 Documentation
Maintain records of:
- Request receipt date
- Identity verification
- Actions taken
- Data provided/deleted
- Completion date
- Staff member responsible