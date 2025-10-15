import json
import boto3
import os
from datetime import datetime

def handler(event, context):
    """
    Lambda function to update an existing task
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        # Parse request body and path parameters
        body = json.loads(event['body'])
        task_id = event['pathParameters']['taskId']
        
        # Build update expression
        update_expression = "SET updatedAt = :updated_at"
        expression_attribute_values = {
            ':updated_at': datetime.utcnow().isoformat()
        }
        
        # Add fields to update
        if 'title' in body:
            update_expression += ", title = :title"
            expression_attribute_values[':title'] = body['title']
        
        if 'description' in body:
            update_expression += ", description = :description"
            expression_attribute_values[':description'] = body['description']
        
        if 'status' in body:
            update_expression += ", status = :status"
            expression_attribute_values[':status'] = body['status']
        
        if 'priority' in body:
            update_expression += ", priority = :priority"
            expression_attribute_values[':priority'] = body['priority']
        
        if 'category' in body:
            update_expression += ", category = :category"
            expression_attribute_values[':category'] = body['category']
        
        if 'dueDate' in body:
            update_expression += ", dueDate = :due_date"
            expression_attribute_values[':due_date'] = body['dueDate']
        
        # Update item in DynamoDB
        table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'message': 'Task updated successfully',
                'taskId': task_id
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

