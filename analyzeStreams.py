import boto3, json
from decimal import Decimal

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

if __name__ == "__main__":
    dbTblName = 'spotifyTbl'
    streams = boto3.client('dynamodbstreams')
    response = streams.list_streams(
        TableName = dbTblName
    )
    # jprint(response['Streams'])
    streamArn = response['Streams'][0]['StreamArn']
    responseStream = streams.describe_stream(
        StreamArn = streamArn
    )
    print(responseStream['StreamDescription']['Shards'][0]['ShardId'])