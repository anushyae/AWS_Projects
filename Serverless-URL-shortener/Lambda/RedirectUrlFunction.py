import os
import boto3

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)

def handler(event, context):
    short_code = event.get("pathParameters", {}).get("shortcode")

    if not short_code:
        return {
            "statusCode": 400,
            "body": "Missing shortcode in request"
        }

    response = table.get_item(Key={"shortCode": short_code})
    item = response.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": "Short URL not found"
        }

    return {
        "statusCode": 301,
        "headers": {
            "Location": item["longUrl"]
        }
    }
