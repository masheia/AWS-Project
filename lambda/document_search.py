import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to search documents
    Supports search by text content, metadata, and AI analysis results
    """
    try:
        # Initialize AWS clients
        dynamodb = boto3.resource('dynamodb')
        
        # Get environment variables
        table_name = os.environ['METADATA_TABLE']
        
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        
        user_id = query_params.get('userId', 'anonymous')
        search_text = query_params.get('searchText', '')
        sentiment_filter = query_params.get('sentiment')
        entity_filter = query_params.get('entity')
        limit = int(query_params.get('limit', 20))
        
        table = dynamodb.Table(table_name)
        
        # Build scan parameters
        scan_params = {
            'Limit': limit
        }
        
        # Add filters
        filter_expressions = []
        expression_attribute_values = {}
        
        # Filter by user ID
        if user_id != 'anonymous':
            filter_expressions.append('userId = :user_id')
            expression_attribute_values[':user_id'] = user_id
        
        # Filter by sentiment
        if sentiment_filter:
            filter_expressions.append('sentiment = :sentiment')
            expression_attribute_values[':sentiment'] = sentiment_filter
        
        # Filter by entity
        if entity_filter:
            filter_expressions.append('contains(entities, :entity)')
            expression_attribute_values[':entity'] = {'Text': entity_filter}
        
        # Filter by text content
        if search_text:
            filter_expressions.append('contains(extractedText, :search_text)')
            expression_attribute_values[':search_text'] = search_text
        
        if filter_expressions:
            scan_params['FilterExpression'] = ' AND '.join(filter_expressions)
            scan_params['ExpressionAttributeValues'] = expression_attribute_values
        
        # Perform scan
        response = table.scan(**scan_params)
        
        # Process results
        documents = []
        for item in response.get('Items', []):
            # Format document for response
            document = {
                'documentId': item.get('documentId'),
                'fileName': item.get('fileName'),
                'fileType': item.get('fileType'),
                'fileSize': item.get('fileSize'),
                'uploadDate': item.get('uploadDate'),
                'status': item.get('status'),
                'sentiment': item.get('sentiment'),
                'sentimentScore': item.get('sentimentScore'),
                'entities': item.get('entities', [])[:10],  # Limit to first 10 entities
                'keyPhrases': item.get('keyPhrases', [])[:10],  # Limit to first 10 phrases
                'extractedTextPreview': item.get('extractedText', '')[:500] + '...' if item.get('extractedText') else ''
            }
            documents.append(document)
        
        # Sort by upload date (newest first)
        documents.sort(key=lambda x: x.get('uploadDate', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'documents': documents,
                'count': len(documents),
                'searchParams': {
                    'userId': user_id,
                    'searchText': search_text,
                    'sentiment': sentiment_filter,
                    'entity': entity_filter
                }
            })
        }
        
    except Exception as e:
        print(f"Error in document search: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Search failed',
                'message': str(e)
            })
        }
