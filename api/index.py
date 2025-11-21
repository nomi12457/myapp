# api/index.py
from app import app    # import your Flask app object from root app.py
import awsgi

def handler(event, context):
    # awsgi turns the Flask WSGI app into a Lambda/APIGW-compatible response
    return awsgi.response(app, event, context)