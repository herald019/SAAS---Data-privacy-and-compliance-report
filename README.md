#SAAS - Data Privacy and Compliance Report

Overview

This project is a SaaS-based Data Privacy and Compliance Monitoring Tool that checks user-provided data against PII (Personally Identifiable Information) regulations, CCPA (California Consumer Privacy Act), and GDPR (General Data Protection Regulation) guidelines. The system leverages AWS services to automate the compliance check and generate actionable reports.

Features

Static Frontend: Hosted on AWS EC2 for seamless user interaction.

File Upload: Users upload a CSV file via the frontend, which is then stored in an AWS S3 bucket.

Automated Scanning: AWS Macie is triggered using an AWS Lambda function whenever new data enters the S3 bucket.

Privacy Compliance Check: AWS Macie scans the uploaded data for CCPA/GDPR violations.

Report Generation: Compliance results are returned in JSON format to the S3 bucket.

PDF and Visualization: The compliance report is converted into a PDF, with simple visual representations for better understanding.

System Workflow

User uploads a CSV file via the web interface.

The file is stored in a dedicated AWS S3 bucket.

AWS Lambda detects the new file and triggers AWS Macie.

AWS Macie scans the data for sensitive information and compliance violations.

The compliance report is generated in JSON format and saved back to the S3 bucket.

The JSON report is processed and converted into a PDF, with additional visual insights if needed.

Tech Stack

Frontend: Static HTML, CSS, JavaScript (hosted on AWS EC2)

Backend Services: AWS Lambda, AWS Macie, AWS S3

Storage: AWS S3 for file storage and report retrieval

Report Processing: JSON report conversion to PDF and visualization

Installation & Deployment

Deploy the static frontend on an AWS EC2 instance.

Set up an AWS S3 bucket to store uploaded files and reports.

Configure AWS Lambda to trigger on new file uploads.

Integrate AWS Macie for scanning and compliance checks.

Implement a service to process JSON reports into PDFs and visual representations.

Future Enhancements

Support for additional file formats beyond CSV.

More advanced data visualizations for compliance reports.

Integration with third-party compliance tools for extended monitoring.

Real-time notifications and alerts for detected violations.

License

This project is open-source under the MIT License.
