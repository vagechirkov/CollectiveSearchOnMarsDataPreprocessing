import datetime
from typing import List, Optional

from pydantic import BaseModel


class TitlePlayerAccount(BaseModel):
    """TitlePlayerAccount model."""
    Id: str
    Type: str = "title_player_account"
    TypeString: str = "title_player_account"


class PlayFabAccountInfo(BaseModel):
    Platform: str
    PlatformUserId: str
    Username: str
    TitlePlayerAccount: TitlePlayerAccount = TitlePlayerAccount(Id="")


class DataFile(BaseModel):
    FileName: str
    DownloadUrl: str
    FileContents: Optional[str]


class Player(BaseModel):
    PlayerId: str
    DisplayName: str
    PublisherId: str
    Created: datetime.datetime
    LastLogin: datetime.datetime
    LinkedAccounts: List[PlayFabAccountInfo]
    Traces: Optional[List[DataFile]]
