# AWS Task Manager - Step-by-Step Deployment Guide

## 🎯 Goal: Deploy a Complete Serverless Task Management System

**Total Time: 45-60 minutes**
**Cost: $0 (Free Tier)**

---

## Step 1: Deploy Infrastructure with CloudFormation (15 minutes)

### 1.1 Open AWS Console
1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Sign in to your account
3. Make sure you're in the correct region (recommend: US East 1 or US West 2)

### 1.2 Create CloudFormation Stack
1. In the AWS Console, search for "CloudFormation"
2. Click "Create Stack" → "With new resources (standard)"
3. Choose "Upload a template file"
4. Click "Choose file" and select `beginner-project/infrastructure/task-manager-template.yaml`
5. Click "Next"

### 1.3 Configure Stack Parameters
**Stack Name**: `task-manager-dev`
**Parameters**:
- Environment: `dev`
- Click "Next"

### 1.4 Configure Stack Options
1. Leave all defaults
2. Scroll down and check "I acknowledge that AWS CloudFormation might create IAM resources"
3. Click "Next"

### 1.5 Review and Create
1. Review all settings
2. Click "Create Stack"
3. Wait 10-15 minutes for stack creation to complete
4. Status should show "CREATE_COMPLETE"

**✅ Checkpoint**: CloudFormation stack created successfully

---

## Step 2: Configure API Gateway (20 minutes)

### 2.1 Create REST API
1. Go to API Gateway console
2. Click "Create API"
3. Choose "REST API" → "Build"
4. Select "New API"
5. **API Name**: `TaskManagerAPI`
6. **Description**: `API for Task Management System`
7. Click "Create API"

### 2.2 Create Resources and Methods

#### Create `/tasks` Resource
1. Select the root resource (/) in the Resources panel
2. Click "Actions" → "Create Resource"
3. **Resource Name**: `tasks`
4. **Resource Path**: `/tasks`
5. Click "Create Resource"

#### Create `/tasks/{taskId}` Resource
1. Select `/tasks` resource
2. Click "Actions" → "Create Resource"
3. **Resource Name**: `taskId`
4. **Resource Path**: `/tasks/{taskId}`
5. Check "Enable API Gateway CORS"
6. Click "Create Resource"

### 2.3 Create Methods

#### GET /tasks
1. Select `/tasks` resource
2. Click "Actions" → "Create Method"
3. Choose "GET" from dropdown
4. Click the checkmark
5. **Integration Type**: Lambda Function
6. **Lambda Function**: `GetTasks-dev` (select from dropdown)
7. **Use Default Timeout**: Checked
8. Click "Save" → "OK"

#### POST /tasks
1. Select `/tasks` resource
2. Click "Actions" → "Create Method"
3. Choose "POST" from dropdown
4. Click the checkmark
5. **Integration Type**: Lambda Function
6. **Lambda Function**: `CreateTask-dev`
7. Click "Save" → "OK"

#### PUT /tasks/{taskId}
1. Select `/tasks/{taskId}` resource
2. Click "Actions" → "Create Method"
3. Choose "PUT" from dropdown
4. Click the checkmark
5. **Integration Type**: Lambda Function
6. **Lambda Function**: `UpdateTask-dev`
7. Click "Save" → "OK"

#### DELETE /tasks/{taskId}
1. Select `/tasks/{taskId}` resource
2. Click "Actions" → "Create Method"
3. Choose "DELETE" from dropdown
4. Click the checkmark
5. **Integration Type**: Lambda Function
6. **Lambda Function**: `DeleteTask-dev`
7. Click "Save" → "OK"

### 2.4 Enable CORS
1. Select `/tasks` resource
2. Click "Actions" → "Enable CORS"
3. **Access-Control-Allow-Origin**: `*`
4. **Access-Control-Allow-Headers**: `Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token`
5. **Access-Control-Allow-Methods**: `GET,POST,PUT,DELETE,OPTIONS`
6. Click "Enable CORS and replace existing CORS headers"

### 2.5 Deploy API
1. Click "Actions" → "Deploy API"
2. **Deployment Stage**: `[New Stage]`
3. **Stage Name**: `dev`
4. **Stage Description**: `Development stage`
5. Click "Deploy"
6. **Copy the Invoke URL** (you'll need this for the frontend)

**✅ Checkpoint**: API Gateway deployed with all endpoints

---

## Step 3: Deploy Frontend (10 minutes)

### 3.1 Find Your S3 Bucket
1. Go to S3 console
2. Look for bucket named: `task-manager-website-dev-[your-account-id]`
3. Click on the bucket name

### 3.2 Upload Frontend Files
1. Click "Upload" → "Add files"
2. Select `beginner-project/frontend/index.html`
3. Click "Upload"

### 3.3 Update API URL in Frontend
1. Download the uploaded `index.html` file
2. Open it in a text editor
3. Find line with: `const API_BASE_URL = 'YOUR_API_GATEWAY_URL_HERE';`
4. Replace `YOUR_API_GATEWAY_URL_HERE` with your API Gateway URL from Step 2.5
5. Save the file
6. Upload the updated file to S3 (replace the existing one)

### 3.4 Configure Static Website Hosting
1. In your S3 bucket, go to "Properties" tab
2. Scroll to "Static website hosting"
3. Click "Edit"
4. **Static website hosting**: Enable
5. **Index document**: `index.html`
6. **Error document**: `index.html`
7. Click "Save changes"
8. **Copy the Website endpoint URL**

**✅ Checkpoint**: Frontend deployed and accessible

---

## Step 4: Test Your Application (15 minutes)

### 4.1 Access Your Application
1. Open the Website endpoint URL from Step 3.4
2. You should see the Task Manager interface

### 4.2 Test All Functionality

#### Test 1: Create a Task
1. Fill in the "Add New Task" form
2. Click "Add Task"
3. Verify the task appears in the task list

#### Test 2: Update Task Status
1. Change the status dropdown on a task
2. Verify the change is saved

#### Test 3: Filter Tasks
1. Use the filter dropdowns (Status, Priority, Category)
2. Click "Refresh"
3. Verify filtering works correctly

#### Test 4: Delete a Task
1. Click "Delete" on a task
2. Confirm deletion
3. Verify task is removed from list

### 4.3 Check Backend
1. Go to DynamoDB console
2. Find table: `Tasks-dev`
3. Click "Explore table items"
4. Verify your tasks are stored in the database

**✅ Checkpoint**: All functionality working correctly

---

## 🎉 Congratulations!

You now have a fully functional, serverless task management system running on AWS!

### What You've Built:
- ✅ Serverless backend with 4 Lambda functions
- ✅ RESTful API with API Gateway
- ✅ NoSQL database with DynamoDB
- ✅ Static website hosted on S3
- ✅ Complete CRUD functionality
- ✅ Modern, responsive user interface

### Next Steps:
1. **Prepare your presentation** using the provided slides
2. **Write your report** using the detailed template
3. **Practice your demo** for the presentation
4. **Document any challenges** you faced during deployment

### For Your Presentation:
- Show the live application
- Demonstrate all features
- Explain the architecture
- Discuss the AWS services used
- Highlight the cost benefits (Free Tier)

---

## 🆘 Troubleshooting

### Common Issues:

**CloudFormation fails to create:**
- Check your IAM permissions
- Ensure you have permission to create IAM roles
- Try a different AWS region

**Lambda functions not working:**
- Check CloudWatch logs
- Verify DynamoDB table exists
- Check environment variables

**API Gateway returns 500 errors:**
- Check Lambda function logs
- Verify function ARNs in API Gateway
- Test Lambda functions directly

**Frontend shows CORS errors:**
- Verify CORS is enabled in API Gateway
- Check Lambda function response headers
- Ensure API Gateway is deployed

**S3 website not loading:**
- Check bucket permissions
- Verify static website hosting is enabled
- Check that index.html is in the root of the bucket

### Getting Help:
- AWS Documentation: https://docs.aws.amazon.com/
- AWS Support Forums
- CloudFormation Troubleshooting Guide
- Lambda Troubleshooting Guide

---

**Ready to start? Let's deploy your AWS Task Manager! 🚀**
