from flask import Flask, render_template, request, redirect
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)


# AWS SQS configuration
region = os.environ.get('AWS_REGION')
queue_url = os.environ.get('QUEUE_URL')

# Create an SQS client
sqs = boto3.client('sqs', region_name=region)

# Function to store data in SQS
def store_data_in_sqs(name, email, additional_data):
    data = {
        'name': name,
        'email': email,
        'additionalData': additional_data
    }

    message_body = json.dumps(data)

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )

    return response

# Function to retrieve messages from SQS
def retrieve_messages_from_sqs():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )

    messages = response.get('Messages', [])

    return messages

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Store data route
@app.route('/store_data', methods=['POST'])
def store_data():
    name = request.form.get('name')
    email = request.form.get('email')
    additional_data = request.form.get('additional_data')

    response = store_data_in_sqs(name, email, additional_data)
    print("data insert sucessfully")

    return ("successfull")

# # View SQS data route
# @app.route('/view_data')
# def view_data():
#     messages = retrieve_messages_from_sqs()

#     data = []
#     for message in messages:
#         body = json.loads(message['Body'])
#         name = body['name']
#         email = body['email']
#         additional_data = body['additionalData']
#         data.append({'name': name, 'email': email, 'additional_data': additional_data})

#     return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)