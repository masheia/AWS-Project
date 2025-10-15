# AWS Task Manager - Deployment Guide

## Prerequisites
1. **AWS Account**: Create an AWS account if you don't have one
2. **AWS CLI**: Install and configure AWS CLI (optional but recommended)
3. **Basic Knowledge**: Understanding of AWS services (Lambda, DynamoDB, S3, API Gateway)

## Step 1: Deploy Infrastructure

### Option A: Using AWS Console (Recommended for Beginners)
1. Go to AWS CloudFormation console
2. Click "Create Stack" → "With new resources"
3. Upload the `task-manager-template.yaml` file
4. Click "Next" and fill in:
   - Stack name: `task-manager-dev`
   - Environment: `dev`
5. Click "Next" → "Next" → "Create Stack"
6. Wait for stack creation to complete (5-10 minutes)

### Option B: Using AWS CLI
```bash
aws cloudformation create-stack \
  --stack-name task-manager-dev \
  --template-body file://task-manager-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_IAM
```

## Step 2: Configure API Gateway

1. Go to API Gateway console
2. Create a new REST API
3. Create resources and methods:
   - `GET /tasks` → Connect to GetTasksFunction
   - `POST /tasks` → Connect to CreateTaskFunction
   - `PUT /tasks/{taskId}` → Connect to UpdateTaskFunction
   - `DELETE /tasks/{taskId}` → Connect to DeleteTaskFunction
4. Enable CORS for all methods
5. Deploy the API to a stage (e.g., `dev`)
6. Note the API Gateway URL

## Step 3: Update Lambda Functions

The Lambda functions are already embedded in the CloudFormation template, but you can update them with the full code from the `lambda/` directory if needed.

## Step 4: Deploy Frontend

1. Go to S3 console
2. Find the website bucket created by CloudFormation
3. Upload the `index.html` file
4. Make sure the bucket is configured for static website hosting
5. Note the website URL

## Step 5: Configure Frontend

1. Open the `index.html` file
2. Replace `YOUR_API_GATEWAY_URL_HERE` with your actual API Gateway URL
3. Upload the updated file to S3

## Step 6: Test the Application

1. Visit your S3 website URL
2. Try adding a new task
3. Verify that tasks are saved to DynamoDB
4. Test filtering and status updates
5. Test task deletion

## Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Ensure CORS is enabled in API Gateway
   - Check that Lambda functions return proper CORS headers

2. **Lambda Function Errors**
   - Check CloudWatch logs for Lambda functions
   - Verify IAM permissions

3. **DynamoDB Access Issues**
   - Ensure Lambda execution role has DynamoDB permissions
   - Check table names match environment variables

4. **API Gateway 500 Errors**
   - Check Lambda function logs
   - Verify function ARNs in API Gateway

### Monitoring:
- Check CloudWatch logs for each Lambda function
- Monitor DynamoDB metrics
- Check API Gateway metrics

## Cost Monitoring

This project is designed to stay within AWS Free Tier limits:
- Lambda: 1M requests/month free
- DynamoDB: 25GB storage free
- API Gateway: 1M API calls/month free
- S3: 5GB storage free

## Next Steps

Once deployed successfully, consider these enhancements:
1. Add user authentication with AWS Cognito
2. Implement real-time updates with WebSockets
3. Add file attachments to tasks
4. Create mobile app version
5. Add advanced analytics and reporting

## Cleanup

To avoid charges, delete resources when done:
1. Delete CloudFormation stack
2. Empty and delete S3 buckets
3. Delete any remaining resources manually

## Support

For issues or questions:
1. Check AWS documentation
2. Review CloudWatch logs
3. Use AWS Support (if you have a support plan)
