import boto3, json
from decimal import Decimal

def createDb(dynamodb,dbTblName):
    table = dynamodb.create_table(
        TableName=dbTblName,
        KeySchema=[
            {
                'AttributeName': 'Date',
                'KeyType': 'HASH'
                },
            {
                'AttributeName': 'Time',
                'KeyType': 'RANGE'
                },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait until the table exists, then print status
    table.meta.client.get_waiter('table_exists').wait(TableName=dbTblName)
    print("Table Status: " + table.table_status)


def populateTbl(dynamodb,dbTblName,fileIn):
    table = dynamodb.Table(dbTblName)
    print("Table Status: " + table.table_status)
    with open(fileIn) as json_file:
        songs = json.load(json_file, parse_float=Decimal)
    # Batch write all the songs, this speeds up process
    with table.batch_writer() as batch:
        for song in songs:
            SongName = song['SongName']
            Artist = song['Artist']
            Album = song['Album']
            ArtistTopTags = song['ArtistTopTags']
            Date = song['Date']
            Time = song['Time']
            TimeOfDay = song['TimeOfDay']
            durationSec = int(song['durationSec'])
            batch.put_item(Item=song)
 
def deleteTbl(dynamodb,dbTblName):
    table = dynamodb.Table(dbTblName)
    table.delete()


if __name__ == "__main__":
    dbTblName = 'spotifyTbl'
    formattedFile = 'outputLastFm.json'

    # Establishing DynamoDb Connection
    dynamodb = boto3.resource('dynamodb')
    # createDb(dynamodb,dbTblName)
    # deleteTbl(dynamodb,dbTblName)
    populateTbl(dynamodb,dbTblName,formattedFile)