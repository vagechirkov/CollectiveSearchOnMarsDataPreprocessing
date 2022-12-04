import logging
from logging import StreamHandler
import os
from typing import List

from dotenv import load_dotenv
from playfab import PlayFabAdminAPI, PlayFabSettings, PlayFabAuthenticationAPI, PlayFabErrors

from playfab_manager.models.player import Player, TitlePlayerAccount

# Create a Logger instance
logger = logging.getLogger("PlayFabManager")
logger.setLevel(logging.INFO)

handler = StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def _check_entity_token_callback(result, error):
    if result:
        logger.info("Entity token is valid")
    else:
        logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))
        PlayFabAuthenticationAPI.GetEntityToken(request={}, callback=_get_entity_token_callback)


def _get_entity_token_callback(result, error):
    if result:
        logger.info("Entity token is created")
    else:
        logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))


class PlayFabManager:

    def __init__(self):
        load_dotenv()

        # Get the value of the TITLE_ID environment variable
        PlayFabSettings.TitleId = os.getenv("TITLE_ID")
        # Get the value of the API_KEY environment variable
        PlayFabSettings.DeveloperSecretKey = os.getenv("API_KEY")

        if PlayFabSettings._internalSettings.EntityToken:
            PlayFabAuthenticationAPI.ValidateEntityToken(
                request={'EntityToken': PlayFabSettings._internalSettings.EntityToken},
                callback=_check_entity_token_callback)
        else:
            PlayFabAuthenticationAPI.GetEntityToken(request={}, callback=_get_entity_token_callback)

        self.all_players = None

    def get_all_players(self, segment_id=None):
        if not segment_id:
            segment_id = os.getenv("SEGMENT_ID")
        PlayFabAdminAPI.GetPlayersInSegment(request={"SegmentID": segment_id}, callback=self._get_all_players)
        # log info about the players
        logger.info(f"Found {len(self.all_players)} players")

    def _get_all_players(self, result, error):
        if result:
            self.all_players = [Player.parse_obj(player) for player in result["PlayerProfiles"]]
        else:
            logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))

    def get_player_title_account_id(self, players: List[Player]):
        for player in players:
            PlayFabAdminAPI.GetUserAccountInfo(
                request={"PlayFabId": player.PlayerId},
                callback=self._get_player_title_account_id)

    def _get_player_title_account_id(self, result, error):
        if result:
            # get the player index
            player_index = self.all_players.index(Player(PlayerId=result["data"]["UserInfo"]["PlayFabId"]))
            player_title_id = result["UserInfo"]["TitleInfo"]["TitlePlayerAccount"]["Id"]

            self.all_players[player_index].PlayFabAccountInfo.TitleAccountId = TitlePlayerAccount(Id=player_title_id)
        else:
            logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))

    def download_player_file(self, players: List[Player]):
        self.get_player_title_account_id(players)



