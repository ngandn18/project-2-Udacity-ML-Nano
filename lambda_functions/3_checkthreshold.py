# checkthreshold lambda function

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
