import json
import os
import hashlib
import base64
from datetime import datetime
import boto3

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
secretsmanager = boto3.client("secretsmanager")

# Read environment variables
table_name = os.environ["TABLE_NAME"]
secret_arn = os.environ.get("SECRET_ARN")

table = dynamodb.Table(table_name)

def generate_short_code(url: str) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(url.encode()).digest())[:6].decode()

def get_secret():
    if not secret_arn:
        return None
    response = secretsmanager.get_secret_value(SecretId=secret_arn)
    secret = json.loads(response["SecretString"])
    return secret.get("key")  # Optional, depends on your secret format

def handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response["Body"].read().decode("utf-8")
            data = json.loads(content)
            long_url = data.get("url")

            if not long_url:
                print(f"❌ Missing 'url' key in file: {key}")
                continue

            short_code = generate_short_code(long_url)

            # Check if already exists
            existing = table.get_item(Key={"shortCode": short_code}).get("Item")
            if not existing:
                table.put_item(Item={
                    "shortCode": short_code,
                    "longUrl": long_url,
                    "createdAt": datetime.utcnow().isoformat()
                })
                print(f"✅ New short URL created: {short_code}")
            else:
                print(f"ℹ️ Short URL already exists: {short_code}")

            # Optional secret usage
            secret_val = get_secret()
            if secret_val:
                print(f"🔐 Using secret value: {secret_val}")

        except Exception as e:
            print(f"❌ Error processing {key}: {e}")
