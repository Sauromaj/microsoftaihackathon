import os
import mysql.connector

mysql_local_config = {
    'host':'localhost',
    'user':'root',
    'database':'instructai'
}

azure_config = {
  'host':'testmicrosoftaiserver.mysql.database.azure.com',
  'user':'saurodeepmajumdar',
  'password':os.environ['AZURE_SQL_CRED'],
  'database':'instructai',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
}

LOCAL_MONGO_URL = "mongodb://localhost:27017"

COSMOS_CONNECTION_STRING =  os.environ['COSMOS_CONNECTION_STRING']
DB_NAME = "instructaimongo"
COLLECTION_NAME = "Lectures"

# Your subscription key and region for the speech service
SUBSCRIPTION_KEY = os.environ['SUBSCRIPTION_KEY']
SERVICE_REGION = "eastus"

NAME = "test_transcription"
DESCRIPTION = "Simple transcription description"

LOCALE = "en-US"
RECORDINGS_BLOB_URI = "<Your SAS Uri to the recording>"

