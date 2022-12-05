import datetime
from typing import List, Optional

import pandas as pd
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
    ServerID: Optional[str]
    ChunkNumber: Optional[int]
    FileContents: Optional[str]


class Player(BaseModel):
    PlayerId: str
    DisplayName: str
    PublisherId: str
    Created: datetime.datetime
    LastLogin: datetime.datetime
    LinkedAccounts: List[PlayFabAccountInfo]
    DataFiles: Optional[List[DataFile]]
    ServerID: Optional[str]
    IsResource: Optional[bool]
    TracesRaw: Optional[str]
    TracesPandas: Optional[pd.DataFrame]

    # allow arbitrary types in Config
    class Config:
        arbitrary_types_allowed = True
