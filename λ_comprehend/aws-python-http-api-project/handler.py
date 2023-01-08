import json
import boto3

client = boto3.client('comprehend')

# body
# {
#     "frase": "frase"
# }

# retorna
# {

# }


# response = client.detect_sentiment(
#     Text='hola me llamo sebastian',
#     LanguageCode='es'
# )
#     body = {
#         'response': response
#     }
#     return {
#         'statusCode': 200,
#         'body': json.dumps(body)
#     }

def get_sentiment(event, context):
    config = json.loads(event['body'])
    frase = config['frase']

    response_aws = client.detect_sentiment(
    Text=frase,
    LanguageCode='es'
    )

    print(response_aws)
    body = {
        "sentiment": response_aws['Sentiment'],
        "score": response_aws['SentimentScore'],
    }

    print(body)
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
    
def get_entities(event, context):
    config = json.loads(event['body'])
    frase = config['frase']

    response_aws = client.detect_entities(
    Text=frase,
    LanguageCode='es'
    )

    print(response_aws)
    body = {
        "Entities": response_aws['Entities'],
    }

    print(body)
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


