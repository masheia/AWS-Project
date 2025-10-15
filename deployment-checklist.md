# AWS Task Manager - Deployment Checklist

## ✅ Prerequisites Checklist

### 1. AWS Account Setup
- [ ] AWS Account created (if not already done)
- [ ] AWS Free Tier eligibility confirmed
- [ ] AWS Console access working
- [ ] Payment method added (required even for Free Tier)

### 2. AWS CLI Setup (Optional but Recommended)
- [ ] AWS CLI installed on your computer
- [ ] AWS credentials configured (`aws configure`)
- [ ] Default region set (recommend: us-east-1 or us-west-2)

### 3. Required AWS Services Access
Make sure you have access to these services in your AWS Console:
- [ ] CloudFormation
- [ ] Lambda
- [ ] API Gateway
- [ ] DynamoDB
- [ ] S3
- [ ] IAM
- [ ] CloudWatch

## 🚀 Deployment Steps

### Step 1: Deploy Infrastructure (CloudFormation)
**Estimated time: 10-15 minutes**

1. Go to AWS CloudFormation Console
2. Click "Create Stack" → "With new resources"
3. Upload the `task-manager-template.yaml` file
4. Fill in parameters and create stack

### Step 2: Configure API Gateway
**Estimated time: 15-20 minutes**

1. Create new REST API in API Gateway
2. Set up resources and methods
3. Connect to Lambda functions
4. Enable CORS
5. Deploy API

### Step 3: Deploy Frontend
**Estimated time: 5-10 minutes**

1. Upload `index.html` to S3 bucket
2. Configure static website hosting
3. Update API URL in frontend code

### Step 4: Test Application
**Estimated time: 10 minutes**

1. Visit your S3 website URL
2. Test creating tasks
3. Test updating task status
4. Test deleting tasks
5. Test filtering functionality

## ⚠️ Important Notes

### Cost Monitoring
- All services designed to stay within Free Tier
- Monitor your AWS billing dashboard
- Set up billing alerts if desired

### Security Notes
- Lambda functions have minimal required permissions
- S3 bucket configured for public read access (static website)
- API Gateway has CORS enabled

### Troubleshooting
- Check CloudWatch logs for Lambda function errors
- Verify IAM permissions if functions fail
- Ensure API Gateway is deployed to a stage

## 📞 Need Help?

### Common Issues:
1. **CloudFormation fails**: Check IAM permissions
2. **Lambda errors**: Check CloudWatch logs
3. **CORS errors**: Verify API Gateway CORS settings
4. **Frontend not loading**: Check S3 bucket permissions

### Resources:
- AWS Documentation: https://docs.aws.amazon.com/
- AWS Free Tier: https://aws.amazon.com/free/
- CloudFormation Docs: https://docs.aws.amazon.com/cloudformation/

## ✅ Success Criteria

Your deployment is successful when:
- [ ] CloudFormation stack shows "CREATE_COMPLETE"
- [ ] Lambda functions are created and testable
- [ ] API Gateway is deployed and accessible
- [ ] S3 website loads without errors
- [ ] You can create, read, update, and delete tasks
- [ ] All functionality works in the web interface
