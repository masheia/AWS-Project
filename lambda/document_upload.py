import json
import boto3
import uuid
from datetime import datetime
import os

def lambda_handler(event, context):
    """
    Lambda function to handle document upload requests
    Generates presigned URLs for secure S3 uploads
    """
    try:
        # Initialize AWS clients
        s3_client = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        
        # Get bucket name from environment variable
        bucket_name = os.environ['DOCUMENT_BUCKET']
        
        # Parse request body
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']
        
        user_id = body.get('userId', 'anonymous')
        file_name = body.get('fileName', 'unknown')
        file_type = body.get('fileType', 'application/octet-stream')
        file_size = body.get('fileSize', 0)
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Create S3 key
        s3_key = f"documents/{user_id}/{document_id}/{file_name}"
        
        # Generate presigned URL for upload
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': s3_key,
                'ContentType': file_type
            },
            ExpiresIn=3600  # 1 hour
        )
        
        # Store document metadata in DynamoDB
        table = dynamodb.Table(os.environ['METADATA_TABLE'])
        table.put_item(
            Item={
                'documentId': document_id,
                'userId': user_id,
                'fileName': file_name,
                'fileType': file_type,
                'fileSize': file_size,
                's3Key': s3_key,
                'uploadDate': datetime.utcnow().isoformat(),
                'status': 'uploading',
                'processedAt': None,
                'extractedText': None,
                'sentiment': None,
                'entities': [],
                'keyPhrases': []
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'documentId': document_id,
                'uploadUrl': presigned_url,
                'message': 'Upload URL generated successfully'
            })
        }
        
    except Exception as e:
        print(f"Error in document upload: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }
