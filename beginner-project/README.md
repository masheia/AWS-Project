# AWS Beginner Project: Smart Task Manager

## Project Overview
A simple yet comprehensive serverless task management application that demonstrates core AWS services. This project is perfect for AWS beginners and covers all the essential concepts.

## Why This Project?
- **Simple but complete**: Covers all major AWS services
- **Real-world application**: Solves actual problems
- **Progressive learning**: Build complexity gradually
- **Cost-effective**: Stays within free tier limits
- **Great for presentations**: Clear architecture and functionality

## Features
- Create, read, update, delete tasks
- User authentication (simple)
- Task categorization and priorities
- Due date tracking
- Search and filter functionality
- Real-time updates

## AWS Services Used
1. **AWS Lambda** - Serverless compute
2. **Amazon API Gateway** - REST API endpoints
3. **Amazon DynamoDB** - NoSQL database
4. **Amazon S3** - Static website hosting
5. **Amazon CloudWatch** - Monitoring and logging
6. **AWS IAM** - Security and permissions

## Architecture
```
Frontend (S3) → API Gateway → Lambda Functions → DynamoDB
                      ↓
                 CloudWatch (Logs)
```

## Learning Objectives
- Understand serverless architecture
- Learn AWS Lambda function development
- Master DynamoDB operations
- Implement RESTful APIs
- Deploy static websites on S3
- Monitor applications with CloudWatch

## Cost Estimation
All services stay within AWS Free Tier limits:
- Lambda: 1M requests/month free
- DynamoDB: 25GB storage free
- API Gateway: 1M API calls/month free
- S3: 5GB storage free
- CloudWatch: 10 custom metrics free

## Prerequisites
- AWS Account (Free Tier eligible)
- Basic programming knowledge (Python/JavaScript)
- AWS CLI installed (optional but recommended)

## Deployment Steps
1. Deploy infrastructure with CloudFormation
2. Create and deploy Lambda functions
3. Configure API Gateway
4. Upload frontend to S3
5. Test the complete application

## Next Steps After This Project
- Add user authentication with Cognito
- Implement real-time updates with WebSockets
- Add file upload functionality
- Integrate with external APIs
- Add advanced monitoring and alerting
