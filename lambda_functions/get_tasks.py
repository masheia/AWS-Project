import json
import boto3
import os

def handler(event, context):
    """
    Lambda function to get all tasks with optional filtering
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        user_id = query_params.get('userId', 'default-user')
        status = query_params.get('status')
        
        # Scan table with optional filters
        if status:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('userId').eq(user_id) & 
                              boto3.dynamodb.conditions.Attr('status').eq(status)
            )
        else:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('userId').eq(user_id)
            )
        
        tasks = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({
                'tasks': tasks,
                'count': len(tasks)
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

