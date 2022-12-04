import json
import os
from datetime import datetime
from pathlib import Path

from playfab_manager.playfab_manager import PlayFabManager


if __name__ == '__main__':
    # Initialize PlayFab manager
    playfab = PlayFabManager()

    # make results directory
    folder_name = Path("data-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    os.mkdir(folder_name)

    # Get all players
    playfab.get_all_players()

    # all players to a file
    if playfab.all_players:
        with open(folder_name / "players.json", "w") as f:
            # dump all players to a file
            json.dump(playfab.all_players, f)
