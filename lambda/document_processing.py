import json
import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Lambda function to process uploaded documents
    Uses Textract for OCR and Comprehend for AI analysis
    """
    try:
        # Initialize AWS clients
        textract_client = boto3.client('textract')
        comprehend_client = boto3.client('comprehend')
        dynamodb = boto3.resource('dynamodb')
        
        # Get environment variables
        bucket_name = os.environ['DOCUMENT_BUCKET']
        table_name = os.environ['METADATA_TABLE']
        
        # Parse S3 event or direct invocation
        if 'Records' in event:
            # S3 trigger event
            record = event['Records'][0]
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
        else:
            # Direct invocation
            bucket = event.get('bucket', bucket_name)
            key = event.get('key')
        
        if not key:
            raise ValueError("No document key provided")
        
        # Extract document ID from S3 key
        document_id = key.split('/')[-2] if '/' in key else key.split('/')[-1]
        
        print(f"Processing document: {key}")
        
        # Update status to processing
        table = dynamodb.Table(table_name)
        table.update_item(
            Key={'documentId': document_id},
            UpdateExpression='SET #status = :status, processingStartedAt = :started_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'processing',
                ':started_at': datetime.utcnow().isoformat()
            }
        )
        
        extracted_text = ""
        sentiment_result = None
        entities_result = None
        key_phrases_result = None
        
        # Extract text using Textract
        try:
            textract_response = textract_client.detect_document_text(
                Document={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                }
            )
            
            # Extract text from Textract response
            extracted_text = ""
            for block in textract_response['Blocks']:
                if block['BlockType'] == 'LINE':
                    extracted_text += block['Text'] + '\n'
            
            print(f"Extracted text length: {len(extracted_text)}")
            
        except ClientError as e:
            print(f"Textract error: {str(e)}")
            # If Textract fails, try to read as text file
            try:
                s3_client = boto3.client('s3')
                response = s3_client.get_object(Bucket=bucket, Key=key)
                extracted_text = response['Body'].read().decode('utf-8')
            except:
                extracted_text = "Unable to extract text from document"
        
        # Analyze text with Comprehend if text was extracted
        if extracted_text and len(extracted_text.strip()) > 0:
            try:
                # Limit text to 5000 characters for Comprehend
                text_for_analysis = extracted_text[:5000]
                
                # Detect sentiment
                sentiment_result = comprehend_client.detect_sentiment(
                    Text=text_for_analysis,
                    LanguageCode='en'
                )
                
                # Detect entities
                entities_result = comprehend_client.detect_entities(
                    Text=text_for_analysis,
                    LanguageCode='en'
                )
                
                # Detect key phrases
                key_phrases_result = comprehend_client.detect_key_phrases(
                    Text=text_for_analysis,
                    LanguageCode='en'
                )
                
            except ClientError as e:
                print(f"Comprehend error: {str(e)}")
                sentiment_result = {'Sentiment': 'UNKNOWN', 'SentimentScore': {}}
                entities_result = {'Entities': []}
                key_phrases_result = {'KeyPhrases': []}
        
        # Update document metadata with processing results
        update_expression = 'SET #status = :status, processedAt = :processed_at, extractedText = :text'
        expression_attribute_names = {'#status': 'status'}
        expression_attribute_values = {
            ':status': 'completed',
            ':processed_at': datetime.utcnow().isoformat(),
            ':text': extracted_text
        }
        
        if sentiment_result:
            update_expression += ', sentiment = :sentiment, sentimentScore = :sentiment_score'
            expression_attribute_values[':sentiment'] = sentiment_result.get('Sentiment', 'UNKNOWN')
            expression_attribute_values[':sentiment_score'] = sentiment_result.get('SentimentScore', {})
        
        if entities_result:
            update_expression += ', entities = :entities'
            expression_attribute_values[':entities'] = entities_result.get('Entities', [])
        
        if key_phrases_result:
            update_expression += ', keyPhrases = :key_phrases'
            expression_attribute_values[':key_phrases'] = key_phrases_result.get('KeyPhrases', [])
        
        table.update_item(
            Key={'documentId': document_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Document processed successfully',
                'documentId': document_id,
                'extractedTextLength': len(extracted_text),
                'sentiment': sentiment_result.get('Sentiment', 'UNKNOWN') if sentiment_result else None
            })
        }
        
    except Exception as e:
        print(f"Error in document processing: {str(e)}")
        
        # Update document status to failed
        try:
            if 'document_id' in locals():
                table.update_item(
                    Key={'documentId': document_id},
                    UpdateExpression='SET #status = :status, errorMessage = :error',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':status': 'failed',
                        ':error': str(e)
                    }
                )
        except:
            pass
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Document processing failed',
                'message': str(e)
            })
        }
