# 1. serializeImageData Lambda function 1
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event["s3_key"] ## TODO: fill in
    bucket = 'p2-ngandn18' ## TODO: fill in

    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return (
        {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    )

# 2.predictlbda lambda function 2

import json
import base64
import boto3

# Fill this in with the name of your deployed model
## TODO: fill in
ENDPOINT_NAME = 'image-classification-2021-11-21-03-39-30-277'
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    """
    Use sagemaker runtime.invoke_endpoint to predict an image
    """

    # Decode the image data
    payload = base64.b64decode(event["image_data"])## TODO: fill in

    # Instantiate a Predictor
    # predictor = ## TODO: 
    # endpoint_name='image-classification-2021-11-21-03-39-30-277'
    # For this model the IdentitySerializer needs to be "image/png"
    try:
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='image/png',
            Body=payload
            )
        result = json.loads(response['Body'].read().decode())
        # event["inferences"] = response.decode('utf-8')
        # Make a prediction:
        # inferences = ## TODO: fill in
        inferences = result
        # We need only inferences[0], we can have inferences[1] from inferences[0] 
        event["inferences"] = inferences[0]

    except Exception as e:
        print(f'Inference Error: {e}')


    # We return the data back to the Step Function    
    return json.dumps(event)    
    
# 3.checkthreshold lambda function 3

import json

THRESHOLD = .93

def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event["inferences"]## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = inferences > THRESHOLD or (1 - inferences) > THRESHOLD ## TODO: fill in
    event["meets_threshold"] = meets_threshold
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    try:
        if meets_threshold:
            pass
        else:
            raise("THRESHOLD_CONFIDENCE_NOT_MET")
    except Exception as e:
        print(f'Inference Error: {e}')

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
