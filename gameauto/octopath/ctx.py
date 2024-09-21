from ..base import BaseTaskCtx
from ..gameconstants import DEFAULT_ACTION_DELAY


class OctopathTaskCtx(BaseTaskCtx):
    def __init__(self, config: dict):
        super().__init__(config)
        self.action_interval = (
            int(config.get("game", {}).get("action_interval", DEFAULT_ACTION_DELAY))
            / 1000.0
        )
