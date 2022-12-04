import os

from playfab import PlayFabAdminAPI, PlayFabSettings, PlayFabAuthenticationAPI, PlayFabErrors
from dotenv import load_dotenv


class PlayFabManager:

    def __init__(self):
        load_dotenv()

        # Get the value of the TITLE_ID environment variable
        PlayFabSettings.TitleId = os.getenv("TITLE_ID")
        # Get the value of the API_KEY environment variable
        PlayFabSettings.DeveloperSecretKey = os.getenv("API_KEY")

        if PlayFabSettings._internalSettings.EntityToken:
            PlayFabAuthenticationAPI.ValidateEntityToken({}, self.get_entity_token)
        else:
            PlayFabAuthenticationAPI.GetEntityToken(request={}, callback=None)

        self.all_players = None

    @staticmethod
    def get_entity_token(result, error):
        if result:
            print(result)
        else:
            print(error)
            PlayFabAuthenticationAPI.GetEntityToken(request={}, callback=None)

    def get_all_players(self, segment_id=None):
        if not segment_id:
            segment_id = os.getenv("SEGMENT_ID")
        PlayFabAdminAPI.GetPlayersInSegment(request={"SegmentID": segment_id}, callback=self._get_all_players)

    def _get_all_players(self, result, error):
        if result:
            self.all_players = result
        else:
            print(error)


