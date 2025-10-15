# 🚀 SAM Deployment Guide - AWS Task Manager

## Prerequisites

### 1. Install AWS SAM CLI
```bash
# Windows (using pip)
pip install aws-sam-cli

# Or download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

### 2. Configure AWS CLI
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter your default output format (json)
```

## 🚀 Deployment Steps

### Step 1: Build the Application
```bash
sam build
```

### Step 2: Deploy to AWS
```bash
sam deploy --guided
```

**During guided deployment, you'll be asked:**
- **Stack Name**: `task-manager-sam`
- **AWS Region**: `us-east-1` (or your preferred region)
- **Parameter Environment**: `dev`
- **Allow SAM CLI IAM role creation**: `Y`
- **Save parameters to configuration file**: `Y`
- **SAM configuration file**: `samconfig.toml`
- **SAM configuration environment**: `default`

### Step 3: Upload Frontend
After deployment completes, SAM will output:
- **WebsiteURL**: Your S3 bucket website URL
- **ApiGatewayURL**: Your API Gateway URL

**Upload your frontend:**
1. Go to S3 console
2. Find your bucket (task-manager-website-dev-[account-id])
3. Upload `task-manager-simple.html`
4. Rename to `index.html`

### Step 4: Configure S3 Permissions
1. Go to S3 bucket → Permissions
2. Block public access settings → Edit
3. Uncheck ALL 4 boxes
4. Save changes (type "confirm")

### Step 5: Test Your Application
1. Visit your S3 website URL
2. Enter your API Gateway URL
3. Test all functionality

## 🎯 Quick Deployment Commands

```bash
# Build
sam build

# Deploy (guided)
sam deploy --guided

# Deploy (using saved config)
sam deploy

# Delete stack
sam delete
```

## 📊 What SAM Creates

- ✅ **4 Lambda Functions** (GetTasks, CreateTask, UpdateTask, DeleteTask)
- ✅ **1 DynamoDB Table** (Tasks-dev)
- ✅ **1 API Gateway** (with CORS enabled)
- ✅ **1 S3 Bucket** (for static website hosting)
- ✅ **IAM Roles** (with least privilege access)

## 🔧 Troubleshooting

### If SAM build fails:
```bash
# Clean and rebuild
sam build --use-container
```

### If deployment fails:
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check region
aws configure get region
```

### If S3 website shows access denied:
1. Check bucket permissions (all 4 boxes unchecked)
2. Verify bucket policy is applied

## 📋 File Structure

```
AWS Project/
├── template.yaml                 # SAM template
├── lambda_functions/
│   ├── get_tasks.py             # GET /tasks
│   ├── create_task.py           # POST /tasks
│   ├── update_task.py           # PUT /tasks/{taskId}
│   └── delete_task.py           # DELETE /tasks/{taskId}
├── task-manager-simple.html     # Frontend
└── samconfig.toml               # SAM configuration (created after deploy)
```

## 🎉 Benefits of SAM

- ✅ **Automated API Gateway setup** (no manual configuration)
- ✅ **Built-in CORS support**
- ✅ **Automatic IAM role creation**
- ✅ **Easy local testing**
- ✅ **One-command deployment**
- ✅ **Infrastructure as Code**

## 💰 Cost

All resources stay within AWS Free Tier:
- Lambda: 1M requests/month
- DynamoDB: 25GB storage
- API Gateway: 1M calls/month
- S3: 5GB storage

**Total: $0/month**

---

## 🚀 Ready to Deploy?

1. **Install SAM CLI** (if not already installed)
2. **Run**: `sam build`
3. **Run**: `sam deploy --guided`
4. **Follow the prompts**
5. **Upload frontend to S3**
6. **Test your application**

**Your AWS Task Manager will be fully deployed and ready for presentation! 🎯**

