SERVERLESS URL SHORTENER WITH PYTHON CDK + GITLAB CI
=====================================================
About:
This project is a serverless URL shortener built using Python and deployed with AWS CDK. It is designed to be deployed using GitLab CI/CD pipelines.

Features:
- Infrastructure as Code (IaC) with AWS CDK (to provision resources like Lambda, API Gateway, DynamoDB) 
- Serverless architecture using AWS Lambda
- URL shortening functionality mapped to a DynamoDB table
- API Gateway for handling HTTP requests
- GitLab CI/CD integration for automated deployments
- Cloudwatch for monitoring and logging
- Easy to extend and customize

Requirements:
- AWS Account
- AWS CLI configured
- Python 3.8 or higher
- AWS CDK installed
- GitLab account for CI/CD
- GitLab Runner configured
- Docker (for local testing)

Installation:
1. Clone the repository:
   ```bash
   git clone https://gitlab.com/yourusername/serverless-url-shortener.git
   cd serverless-url-shortener
   ```
2. Install the dependencies:
   Make sure AWS Cli, npm are installed by downloading the MSI installers. Then install aws-cdk.
   ```bash
   npm install -g aws-cdk
   ```
3. Create CDK app in Python from library template
   ```bash
   cdk init app --language=python
   # this creates the new CDK project from the template
   ```
