import datetime
from typing import List

from pydantic import BaseModel


class PlayFabAccountInfo(BaseModel):
    Platform: str
    PlatformUserId: str
    Username: str


class Player(BaseModel):
    PlayerId: str
    DisplayName: str
    PublisherId: str
    Created: datetime.datetime
    LastLogin: datetime.datetime
    LinkedAccounts: List[PlayFabAccountInfo]
