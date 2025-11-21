# api/index.py
from app import app           # import root app.py ka app object
import awsgi

def handler(event, context):
    # awsgi converts Flask WSGI app to Lambda-compatible response
    return awsgi.response(app, event, context)