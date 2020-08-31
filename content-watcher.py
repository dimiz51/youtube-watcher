import json
from datetime import datetime
from client_settings import setup_YTClient
# pylint:disable=E1101


# Youtube Channels monitoring class for new video content
class content_watcher():

    # Watcher class initialization -  Load/Create existing/new youtube channels watcher object
    # Using client setup module for the Youtube Data API
    def __init__(self,create: bool,channels_ids = None) -> None:
        self.client = setup_YTClient()
        self.new_content = []
        if create:
            if channels_ids:
                watcher = {'watcher': channels_ids}
                with open('watcher_data/channels.json', 'w') as outfile:
                    json.dump(watcher, outfile)

    # Function implementing search/HTTP GET requests for today's new video content,
    # for all the channels selected by the user.
    def channels_monitoring(self) -> None:      
        with open('watcher_data/channels.json', 'r') as resource:
            watcher = json.load(resource)['watcher']
        for channel in watcher:
            current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            request = self.client.search().list(
                part="snippet",
                channelId=channel,
                maxResults=5,
                order="date",
                publishedAfter=current_date,
                type = 'video'
            )
            res = request.execute()
            if len(res['items']) > 0:
                self.parse_response(res['items'])
        with open(f'{current_date.strftime("%Y-%m-%d")}.json', 'w') as outfile:
                if len(self.new_content) > 0 :
                    json.dump(self.new_content, outfile)
                else:
                    json.dump('Nothing new',outfile)

    # JSON response data-parsing function
    def parse_response(self, res: dict) -> None:
        core_video_url = 'https://www.youtube.com/watch?v='
        for item in res:
            try:
                vid = core_video_url + item['id']['videoId']
                self.new_content.append(vid)
            except:
                continue
            

if __name__ == "__main__":
    watcher = content_watcher(create=True,channels_ids=['UCd8sdpZhDOqoBiwvsSrwrkg',
                               'UCaBqRxHEMomgFU-AkSfodCw',
                               'UC1CVzH-XVr3E-kTT6D8hhfg',
                               'UCP8wqLAt5qYMmOwMB7-mvTQ'])
    watcher.channels_monitoring()


