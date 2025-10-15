# AWS Task Manager

## Project Overview
A serverless task management system built on AWS that provides a complete CRUD (Create, Read, Update, Delete) interface for managing tasks. The application features a modern web interface with real-time task management capabilities.

## Features
- **Task Management**: Create, view, update, and delete tasks
- **Task Status Tracking**: Mark tasks as pending, in-progress, or completed
- **Priority Levels**: Set task priority (low, medium, high)
- **Categories**: Organize tasks by category
- **Real-time Updates**: Instant task status updates
- **Responsive Design**: Works on desktop and mobile devices
- **HTTPS Security**: Secure connections with SSL/TLS encryption

## AWS Services Used
- **Amazon S3**: Static website hosting
- **AWS Lambda**: Serverless backend functions
- **Amazon API Gateway**: REST API endpoints with CORS support
- **Amazon DynamoDB**: Task data storage
- **Amazon CloudFront**: Global CDN with HTTPS
- **AWS IAM**: Security and permissions
- **AWS SAM**: Serverless Application Model for deployment

## Architecture
The system follows a serverless architecture pattern with the following components:

1. **Frontend**: Static website hosted on S3 with CloudFront CDN
2. **API Layer**: RESTful APIs via API Gateway with CORS
3. **Processing Layer**: Lambda functions for task operations
4. **Storage Layer**: DynamoDB for task data persistence
5. **Security**: IAM roles with least privilege access
6. **Performance**: CloudFront for global content delivery

## Prerequisites
- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.9+ (for Lambda functions)
- Git (for version control)

## SAM Deployment Instructions

### 1. Clone and Setup
```bash
git clone <repository-url>
cd aws-task-manager
```

### 2. Build the Application
```bash
sam build
```

### 3. Deploy the Application
```bash
sam deploy --guided
```

Follow the guided deployment prompts:
- **Stack Name**: `task-manager-dev`
- **AWS Region**: `us-east-2` (or your preferred region)
- **Parameter Environment**: `dev`
- **Confirm changes**: `Y`
- **Allow SAM CLI IAM role creation**: `Y`
- **Save parameters to configuration file**: `Y`

### 4. Alternative: Direct Deployment
```bash
sam deploy --stack-name task-manager-dev --s3-bucket your-deployment-bucket --capabilities CAPABILITY_IAM --region us-east-2
```

### 5. Get Application URLs
After deployment, get your application URLs:
```bash
aws cloudformation describe-stacks --stack-name task-manager-dev --query 'Stacks[0].Outputs' --output table
```

## Manual Deployment (Alternative)

If you prefer manual deployment:

### 1. Deploy Infrastructure
```bash
aws cloudformation create-stack --stack-name task-manager-dev --template-body file://beginner-project/infrastructure/task-manager-template.yaml --parameters ParameterKey=Environment,ParameterValue=dev --capabilities CAPABILITY_IAM --region us-east-2
```

### 2. Configure API Gateway
- Create REST API in API Gateway console
- Set up resources and methods for `/tasks` and `/tasks/{taskId}`
- Enable CORS for all methods
- Deploy API to `dev` stage

### 3. Deploy Frontend
```bash
aws s3 cp task-manager-simple.html s3://your-bucket-name/index.html
```

## Application URLs
- **HTTPS (Recommended)**: `https://your-cloudfront-domain.cloudfront.net`
- **HTTP**: `http://your-s3-bucket.s3-website.region.amazonaws.com`
- **API Gateway**: `https://your-api-id.execute-api.region.amazonaws.com/dev`

## Testing the Application

### 1. Access the Web Interface
Visit your CloudFront or S3 website URL to access the task manager interface.

### 2. Test Task Operations
- **Create Task**: Fill out the form and click "Add Task"
- **View Tasks**: Tasks appear in the list below the form
- **Mark Complete**: Click "Mark Complete" on any pending task
- **Delete Task**: Click "Delete" to remove a task

### 3. API Testing
Test the API endpoints directly:
```bash
# Get all tasks
curl -X GET "https://your-api-id.execute-api.region.amazonaws.com/dev/tasks?userId=default-user"

# Create a task
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/dev/tasks" \
  -H "Content-Type: application/json" \
  -d '{"userId":"default-user","title":"Test Task","description":"API Test","priority":"medium","category":"general"}'

# Update a task
curl -X PUT "https://your-api-id.execute-api.region.amazonaws.com/dev/tasks/task-id" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Delete a task
curl -X DELETE "https://your-api-id.execute-api.region.amazonaws.com/dev/tasks/task-id"
```

## Cost Estimation
All services are designed to stay within AWS Free Tier limits for the first 12 months:

- **Lambda**: 1M requests/month (free)
- **DynamoDB**: 25GB storage (free)
- **API Gateway**: 1M calls/month (free)
- **S3**: 5GB storage (free)
- **CloudFront**: 1TB data transfer (free)

**Total estimated cost: $0/month** (within Free Tier)

## Security Features
- **HTTPS Encryption**: All data encrypted in transit
- **IAM Roles**: Least privilege access for Lambda functions
- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Server-side validation for all inputs
- **NoSQL Security**: DynamoDB with proper access controls

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure API Gateway has proper CORS configuration
2. **Lambda Timeout**: Check CloudWatch logs for function errors
3. **DynamoDB Access**: Verify IAM permissions for Lambda functions
4. **S3 Website Not Loading**: Check bucket permissions and static website hosting

### Useful Commands
```bash
# Check CloudFormation stack status
aws cloudformation describe-stacks --stack-name task-manager-dev --query 'Stacks[0].StackStatus'

# View Lambda function logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/task-manager

# Test API Gateway
aws apigateway test-invoke-method --rest-api-id your-api-id --resource-id your-resource-id --http-method GET
```

## Project Structure
```
aws-task-manager/
├── lambda_functions/          # Lambda function code
│   ├── create_task.py
│   ├── get_tasks.py
│   ├── update_task.py
│   └── delete_task.py
├── beginner-project/
│   ├── infrastructure/
│   │   └── task-manager-template.yaml
│   └── frontend/
│       └── index.html
├── template.yaml              # SAM template
├── task-manager-simple.html   # Main frontend file
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
