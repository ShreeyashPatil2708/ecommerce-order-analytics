# src/lambda/data-processor/lambda_function.py
# OPTIMIZED for low cost - simple and fast processing

import json
import csv
import boto3
from datetime import datetime
from io import StringIO
import re

# Initialize AWS clients (reused across invocations)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Process CSV orders from S3
    Optimized for speed and low memory usage
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        # Extract S3 info from EventBridge event
        detail = event['detail']
        bucket = detail['bucket']['name']
        key = detail['object']['key']
        
        print(f"Processing: s3://{bucket}/{key}")
        
        # Extract date from filename (orders_20251014.csv)
        file_date = extract_date_from_filename(key)
        print(f"📅 File date: {file_date}")
        
        # Download CSV
        response = s3.get_object(Bucket=bucket, Key=key)
        csv_data = response['Body'].read().decode('utf-8')
        
        # Process orders
        valid_orders = []
        errors = []
        
        for i, row in enumerate(csv.DictReader(StringIO(csv_data)), start=2):
            try:
                # Quick validation and transformation
                order = {
                    'order_id': row['order_id'].strip(),
                    'customer_name': row['customer_name'].strip(),
                    'customer_email': row['customer_email'].strip(),
                    'product': row['product'].strip(),
                    'category': row['category'].strip(),
                    'quantity': int(row['quantity']),
                    'price': float(row['price']),
                    'order_date': row['order_date'].strip(),
                    'order_time': row.get('order_time', '00:00:00').strip(),
                    'payment_method': row['payment_method'].strip(),
                    'shipping_city': row['shipping_city'].strip(),
                    'total': round(int(row['quantity']) * float(row['price']), 2),
                    'processed_at': datetime.utcnow().isoformat()
                }
                
                # Simple validation
                if order['quantity'] <= 0 or order['price'] <= 0:
                    raise ValueError("Invalid quantity or price")
                
                valid_orders.append(order)
                
            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")
        
        print(f"Valid: {len(valid_orders)}, Errors: {len(errors)}")
        
        if not valid_orders:
            return {'statusCode': 400, 'body': 'No valid orders'}
        
        # Upload to processed bucket (using FILE date, not today)
        processed_bucket = bucket.replace('raw-data', 'processed')
        date_path = file_date.strftime('%Y/%m/%d')  # Use file date here!
        timestamp = datetime.utcnow().strftime('%H%M%S')
        filename = key.split('/')[-1].replace('.csv', '')
        output_key = f"processed/{date_path}/{filename}_{timestamp}.json"
        
        s3.put_object(
            Bucket=processed_bucket,
            Key=output_key,
            Body=json.dumps(valid_orders),
            ContentType='application/json',
            Metadata={
                'original-file': key,
                'file-date': str(file_date),
                'processed-at': datetime.utcnow().isoformat(),
                'order-count': str(len(valid_orders))
            }
        )
        
        print(f"Saved to: s3://{processed_bucket}/{output_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed': len(valid_orders),
                'errors': len(errors),
                'output': output_key,
                'file_date': str(file_date)
            })
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise

def extract_date_from_filename(key):
    """
    Extract date from filename like 'incoming/orders_20251014.csv'
    Returns date object for the file's date (not today)
    """
    try:
        # Extract filename from path
        filename = key.split('/')[-1]  # 'orders_20251014.csv'
        
        # Try to find date pattern YYYYMMDD in filename
        match = re.search(r'(\d{8})', filename)
        if match:
            date_str = match.group(1)
            file_date = datetime.strptime(date_str, '%Y%m%d').date()
            print(f"📅 Date extracted from filename: {file_date}")
            return file_date
        else:
            # Fallback: use today
            print(f"⚠️ No date found in filename '{filename}', using today")
            return datetime.utcnow().date()
        
    except Exception as e:
        print(f"⚠️ Could not extract date from filename: {e}")
        print(f"⚠️ Falling back to today's date")
        return datetime.utcnow().date()