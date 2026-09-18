# lambda_handler.py
import json
from orchestrator import run_review


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        code = body["code"]
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Request body must be JSON with a 'code' field."}),
        }

    result = run_review(code)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }