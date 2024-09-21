from ..base import BaseTaskCtx
from ..gameconstants import DEFAULT_ACTION_DELAY
from .constants import TOWN, WILD


class OctopathTaskCtx(BaseTaskCtx):
    def __init__(self, config: dict):
        super().__init__(config)
        self.action_interval = (
            int(config.get("game", {}).get("action_interval", DEFAULT_ACTION_DELAY))
            / 1000.0
        )

        self.battle_count_after_sleep = 0
        self.total_battle_count = 0
        self.cur_town: TOWN = None
        self.cur_wild: WILD = None
