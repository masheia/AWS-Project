import json
import boto3
import os
import uuid
from datetime import datetime

def handler(event, context):
    """
    Lambda function to create a new task
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        # Parse request body
        body = json.loads(event['body'])
        
        task_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        # Create task item
        task = {
            'taskId': task_id,
            'userId': body.get('userId', 'default-user'),
            'title': body.get('title'),
            'description': body.get('description', ''),
            'status': 'pending',
            'priority': body.get('priority', 'medium'),
            'category': body.get('category', 'general'),
            'dueDate': body.get('dueDate'),
            'createdAt': created_at,
            'updatedAt': created_at
        }
        
        # Save to DynamoDB
        table.put_item(Item=task)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'message': 'Task created successfully',
                'task': task
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

