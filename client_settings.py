import os
import googleapiclient.discovery


# Required settings and setup to use the Google Developers Youtube Data API
def setup_YTClient():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    developer_api_key = 'YOUR_API_KEY'

     # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_api_key)

    return youtube
