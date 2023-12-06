import os, uuid, sys
import time
import json
import requests
import logging
from nosql_connector import NoSQLConnector
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure.cognitiveservices.speech as speechsdk
import swagger_client

from config_params import SUBSCRIPTION_KEY,SERVICE_REGION,NAME, DESCRIPTION, LOCALE,RECORDINGS_BLOB_URI

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#         format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

def create_azure_blob(account_url, default_credential,container_name,local_file_name):
    
    blob_client = None
    container_client = None

    try:
        print("Creating Azure Blob Storage")

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        if not blob_service_client.get_container_client(container=container_name).exists():
             # Create the container
            container_client = blob_service_client.create_container(container_name, public_access='container')
        else:
            container_client = blob_service_client.get_container_client(container_name)
        
        if local_file_name:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)


        print("\nListing blobs...")

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)

        # Download the blob to a local file
        # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
        # download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
        # container_client = blob_service_client.get_container_client(container= container_name) 
        # print("\nDownloading blob to \n\t" + download_file_path)

        # with open(file=download_file_path, mode="wb") as download_file:
        #     download_file.write(container_client.download_blob(blob.name).readall())
        # Clean up
        # print("\nPress the Enter key to begin clean up")
        # input()

        # print("Deleting blob container...")
        # container_client.delete_container()

        # print("Deleting the local source and downloaded files...")
        # os.remove(upload_file_path)
        # os.remove(download_file_path)
        # os.rmdir(local_path)

        print("Done")
    except Exception as ex:
        print('Exception:')
        print(ex)


    return blob_client

def upload_content(account_url, default_credential, path_to_content, container_name):
    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + os.path.split(path_to_content)[1]

    bool_success = False

    blob_client = create_azure_blob(account_url, default_credential,container_name, local_file_name)

    if blob_client:

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(file=path_to_content, mode="rb") as data:
            blob_client.upload_blob(data)
        bool_success = True
    
    response = {
        "account_url": account_url,
        "container": container_name,
        "local_file_name": local_file_name,
        "success": bool_success
    }
    return response

def post_upload_content(param_dict):

    account_url = "https://instructaiblobs.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    path_to_content = param_dict['path']

    container_name = None
    if param_dict['content_type'] == "image":
        container_name = 'instructimages'
    elif param_dict['content_type'] == "videos":
        container_name = 'instructvids'
    elif param_dict['content_type'] == 'audio':
        container_name = 'instructaudio'

    out_dict = upload_content(account_url, default_credential,path_to_content,container_name)

    out_dict['account_url']
    out_dict['container']
    out_dict['local_file_name']


    trans_container_name = 'transcripted-audio'

    blob_client = create_azure_blob(account_url, default_credential, container_name = trans_container_name,local_file_name = None)

    lecture_url = out_dict['account_url'] + '/' +  out_dict['container'] + '/' + out_dict['local_file_name']
    lecture_text_dest_url = "https://instructaiblobs.blob.core.windows.net/transcripted-audio?sp=rw&st=2023-12-05T22:14:49Z&se=2023-12-06T06:14:49Z&skoid=d6c1b579-5967-4c28-aa50-035acebd9864&sktid=723a5a87-f39a-4a22-9247-3fc240c01396&skt=2023-12-05T22:14:49Z&ske=2023-12-06T06:14:49Z&sks=b&skv=2022-11-02&spr=https&sv=2022-11-02&sr=c&sig=DKrhVNcpd9yuTFC0RL0A7w6L0UFJHjHwhCySmL1SvZQ%3D"

    course_code = param_dict['course_code']
    sec_number = param_dict['sec_number']
    sec_semester = param_dict['sec_semester']
    sec_year = param_dict['sec_year']
    lecture_number = param_dict['lecture_number']
    lecture_name = param_dict['lecture_name']

    search_dict = {'course_code':course_code, 'sec_number':sec_number, 'sec_semester':sec_semester, \
                  'sec_year':sec_year,'lecture_number':lecture_number}
    
    write_dict = {'course_code':course_code, 'sec_number':sec_number, 'sec_semester':sec_semester, \
                  'sec_year':sec_year,'lecture_number':lecture_number,'lecture_name':lecture_name, 'lecture_url': lecture_url, 'lecture_transcript_url': ''}

    nosql_connector = NoSQLConnector()

    collection = nosql_connector.connect_to_db()

    nosql_connector.close_connection()

    # try:
    #     collection.insert_one(write_dict)
    # except:
    #     print("Could not insert into collection")

    """Create new document and upsert (create or replace) to collection"""

    # result = collection.update_one(
    #    search_dict, {"$set",write_dict}, upsert=True
    # )
    # print("Upserted document with _id {}\n".format(result.upserted_id))

    # call machine learning algorithm to run on the lecture video and transcript
    # upload the transcript to the text blob, log url into the nosql database (asynchronous)


    transcribe(lecture_url, lecture_text_dest_url)

def test_query():
    nosql_connector = NoSQLConnector()

    collection = nosql_connector.connect_to_db()

    cursor = collection.find({})

    for doc in cursor:
        print(doc)

def test_delete():
    nosql_connector = NoSQLConnector()

    collection = nosql_connector.connect_to_db()

    print(collection.delete_many({"course_code":"ECE457A"}))



def transcribe_from_single_blob(uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = swagger_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition

def _paginate(api, paginated_object):
    """
    The autogenerated client does not support pagination. This function returns a generator over
    all items of the array that the paginated object `paginated_object` is part of.
    """
    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["api_key"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
            response_type=typename, auth_settings=auth_settings)

        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(f"could not receive paginated data: status {status}")

def transcribe(lecture_url,lecture_text_dest_url):
    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = swagger_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.1"

    # create the client object and authenticate
    client = swagger_client.ApiClient(configuration)

    # create an instance of the transcription api class
    api = swagger_client.CustomSpeechTranscriptionsApi(api_client=client)

    # Specify transcription properties by passing a dict to the properties parameter. See
    # https://learn.microsoft.com/azure/cognitive-services/speech-service/batch-transcription-create?pivots=rest-api#request-configuration-options
    # for supported parameters.
    properties = swagger_client.TranscriptionProperties()
    # properties.word_level_timestamps_enabled = True
    # properties.display_form_word_level_timestamps_enabled = True
    # properties.punctuation_mode = "DictatedAndAutomatic"
    # properties.profanity_filter_mode = "Masked"
    properties.destination_container_url = lecture_text_dest_url
    # properties.time_to_live = "PT1H"

    # uncomment the following block to enable and configure speaker separation
    # properties.diarization_enabled = True
    # properties.diarization = swagger_client.DiarizationProperties(
    #     swagger_client.DiarizationSpeakersProperties(min_count=1, max_count=5))

    # properties.language_identification = swagger_client.LanguageIdentificationProperties(["en-US", "ja-JP"])

    # Use base models for transcription. Comment this block if you are using a custom model.
    transcription_definition = transcribe_from_single_blob(lecture_url, properties)

    # Uncomment this block to use custom models for transcription.
    # transcription_definition = transcribe_with_custom_model(client, RECORDINGS_BLOB_URI, properties)

    # uncomment the following block to enable and configure language identification prior to transcription
    # Uncomment this block to transcribe all files from a container.
    # transcription_definition = transcribe_from_container(RECORDINGS_CONTAINER_URI, properties)

    created_transcription, status, headers = api.transcriptions_create_with_http_info(transcription=transcription_definition)

    # get the transcription Id from the location URI
    transcription_id = headers["location"].split("/")[-1]

    # Log information about the created transcription. If you should ask for support, please
    # include this information.
    logging.info(f"Created new transcription with id '{transcription_id}' in region {SERVICE_REGION}")

    logging.info("Checking status.")

    completed = False

    while not completed:
        # wait for 5 seconds before refreshing the transcription status
        time.sleep(5)

        transcription = api.transcriptions_get(transcription_id)
        logging.info(f"Transcriptions status: {transcription.status}")

        if transcription.status in ("Failed", "Succeeded"):
            completed = True

        if transcription.status == "Succeeded":
            pag_files = api.transcriptions_list_files(transcription_id)
            for file_data in _paginate(api, pag_files):
                if file_data.kind != "Transcription":
                    continue

                audiofilename = file_data.name
                results_url = file_data.links.content_url
                results = requests.get(results_url)
                logging.info(f"Results for {audiofilename}:\n{results.content.decode('utf-8')}")
        elif transcription.status == "Failed":
            logging.info(f"Transcription failed: {transcription.properties.error.message}")


if __name__ == "__main__":
    # upload an image to one container
    input_param = {
        "user_id": "bbed4a53-d988-472d-a5db-9a3c4519774e",
        "user_type": "instructor",
        "course_code": "ECE457A",
        "course_name": "Cooperative and Adaptive Algos",
        "sec_number": 1,
        "sec_semester": "Spring",
        "sec_year": 2023,
        "lecture_number": 1,
        "lecture_name": 'Introduction',
        "content_type": "audio",
        "path": "content_uploads/SmartCities_Evs_slide4.m4a"
    }


    post_upload_content(input_param)
    # test_query()
    # test_delete()

    # input_param = {
    #     'content_type': "pdfs",
    #     'path': '',

    # }
    # # upload a pdf to another container
    # container_name = "instructpdfs"
    # path_to_image = 'content_uploads/mltsd-employment-standards-poster-en-2020-09-08.pdf'
    # upload_content(account_url, default_credential, path_to_image, container_name)


