from app import app as application

# Vercel needs "handler" name
def handler(event, context):
    return application