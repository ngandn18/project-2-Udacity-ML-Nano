# predictlbda lambda function

import json
import base64
import boto3

# Fill this in with the name of your deployed model
## TODO: fill in
ENDPOINT_NAME = 'image-classification-2021-11-21-03-39-30-277'
runtime= boto3.client('runtime.sagemaker')

# The notebook' guide shows the impossible import sagemaker. 
# Mentor shows a simple way to call runtime.invoke_runtime to run this lambda function. Pls read the following link.
# https://aws.amazon.com/blogs/machine-learning/call-an-amazon-sagemaker-model-endpoint-using-amazon-api-gateway-and-aws-lambda/

def lambda_handler(event, context):
    # Decode the image data
    payload = base64.b64decode(event["image_data"])## TODO: fill in
    # Instantiate a Predictor
    endpoint_name='image-classification-2021-11-21-03-39-30-277'
    # For this model the IdentitySerializer needs to be "image/png"
    try:
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='image/png',
            Body=payload
            )
        result = json.loads(response['Body'].read().decode())
        # event["inferences"] = response.decode('utf-8')

        inferences = result
        event["inferences"] = inferences[0]

    except Exception as e:
        print(f'Inference Error: {e}')

    # We return the data back to the Step Function    
    return json.dumps(event)    
    
