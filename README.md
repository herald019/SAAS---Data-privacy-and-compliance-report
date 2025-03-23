SAAS - Data Privacy and Compliance Report
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
graph TD;
    A[User Uploads CSV] -->|Stored in S3| B[AWS S3 Bucket];
    B -->|Triggers Lambda| C[AWS Lambda Function];
    C -->|Starts Scan| D[AWS Macie];
    D -->|Scans for Compliance| E[Generates JSON Report];
    E -->|Stores in S3| F[AWS S3 Bucket];
    F -->|Converts JSON to PDF| G[PDF & Visualization Generation];
Tech Stack

    Frontend: Static HTML, CSS, JavaScript (hosted on AWS EC2)

    Backend Services: AWS Lambda, AWS Macie, AWS S3

    Storage: AWS S3 for file storage and report retrieval

    Report Processing: JSON report conversion to PDF and visualization

Installation & Deployment
# Clone the repository
git clone https://github.com/your-repo/SAAS-Data-Privacy-Compliance.git
cd SAAS-Data-Privacy-Compliance

# Deploy frontend on EC2
scp -r frontend/* user@your-ec2-instance:/var/www/html/

# Set up AWS S3 Bucket
aws s3 mb s3://your-bucket-name

# Deploy AWS Lambda function
zip lambda_function.zip lambda_function.py
aws lambda create-function --function-name complianceCheck \
  --runtime python3.x --role arn:aws:iam::your-account-id:role/lambda-role \
  --handler lambda_function.lambda_handler --zip-file fileb://lambda_function.zip
Future Enhancements

    Support for additional file formats beyond CSV.

    More advanced data visualizations for compliance reports.

    Integration with third-party compliance tools for extended monitoring.

    Real-time notifications and alerts for detected violations.

License

This project is open-source under the MIT License.
