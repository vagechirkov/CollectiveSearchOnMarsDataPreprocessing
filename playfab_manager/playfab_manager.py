import logging
from logging import StreamHandler
import os
import io
from typing import List

import pandas as pd
import requests as requests
from dotenv import load_dotenv
from playfab import PlayFabAdminAPI, PlayFabSettings, PlayFabAuthenticationAPI, PlayFabErrors, PlayFabDataAPI

from playfab_manager.models.player import Player, TitlePlayerAccount, DataFile

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

            # sort players by last login time
            self.all_players.sort(key=lambda x: x.LastLogin, reverse=True)
        else:
            logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))

    def get_player_title_account_id(self, playfab_player_id: str):
        PlayFabAdminAPI.GetUserAccountInfo(
            request={"PlayFabId": playfab_player_id},
            callback=self._get_player_title_account_id)

    def _get_player_title_account_id(self, result, error):
        if result:
            # get the player index
            player_index = self._find_player_index(player_id=result["UserInfo"]["PlayFabId"])
            player_title_id = result["UserInfo"]["TitleInfo"]["TitlePlayerAccount"]["Id"]
            self.all_players[player_index].LinkedAccounts[0].TitlePlayerAccount = TitlePlayerAccount(Id=player_title_id)
        else:
            logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))

    def get_player_data_file(self, playfab_player_title_id: str):
        PlayFabDataAPI.GetFiles(
            request={"Entity": {"Id": playfab_player_title_id, "Type": "title_player_account"}},
            callback=self._get_player_data_file)

    def _get_player_data_file(self, result, error):
        if result:
            player_index = self._find_player_index(player_title_id=result["Entity"]["Id"])
            self.all_players[player_index].DataFiles = [DataFile.parse_obj(data) for filename, data in
                                                        result["Metadata"].items()]
            # download the file using the URL
            for data_file in self.all_players[player_index].DataFiles:
                data_file.FileContents = requests.get(data_file.DownloadUrl).content.decode("utf-8")

            for data_file in self.all_players[player_index].DataFiles:
                # server ID is the second part of the filename
                data_file.ServerID = data_file.FileName.split("-")[1]

                # chunk number is the last part of the filename
                data_file.ChunkNumber = data_file.FileName.split("-")[-1]

            # Set server ID to the player
            self.all_players[player_index].ServerID = self.all_players[player_index].DataFiles[0].ServerID

            # Check if the player is a resource
            username = self.all_players[player_index].LinkedAccounts[0].Username
            if username == self.all_players[player_index].ServerID[:20]:
                self.all_players[player_index].IsResource = True

            # sort data chunks by index (the last number)
            self.all_players[player_index].DataFiles.sort(key=lambda x: x.ChunkNumber)

            # merge the chunks into one string
            self.all_players[player_index].TracesRaw = "".join(
                [data_file.FileContents for data_file in self.all_players[player_index].DataFiles])

            # convert string to the pandas dataframe
            output = io.StringIO()
            output.write(self.all_players[player_index].TracesRaw)
            output.seek(0)
            df = pd.read_csv(
                output,
                sep=" ",
                header=None,
                index_col=None,
            )
            # set column names
            df.columns = ["timestamp", "x", "z", "rotation", "signaling", "score"]
            self.all_players[player_index].TracesPandas = df

            logger.info(f"Found {len(self.all_players[player_index].DataFiles)} files for player "
                        f"{self.all_players[player_index].PlayerId}")

        else:
            logger.error(PlayFabErrors.PlayFabError.GenerateErrorReport(error))

    def download_player_files(self, playfab_player_ids: List[str]):
        for i in playfab_player_ids:
            player_index = self._find_player_index(player_id=i)

            self.get_player_title_account_id(i)

            player_title_id = self.all_players[player_index].LinkedAccounts[0].TitlePlayerAccount.Id

            self.get_player_data_file(player_title_id)

    def _find_player_index(self, player_id: str = None, player_title_id: str = None):
        if player_id:
            return self.all_players.index([p for p in self.all_players if p.PlayerId == player_id][0])
        elif player_title_id:
            return self.all_players.index(
                [i for i in self.all_players if
                 i.LinkedAccounts and i.LinkedAccounts[0].TitlePlayerAccount.Id == player_title_id][0])
