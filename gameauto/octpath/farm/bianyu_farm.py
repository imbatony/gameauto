import pyautogui as gui
from ..basic.base_command import BaseOctCommand

class BianyuFarm(BaseOctCommand):
    def __init__(self):
        super().__init__("bianyu_farm", "边域打怪", "边域打怪")

    def execute(self, args):
        print("边域打怪，开始...")
        # 找到app窗口并激活
        print("激活app窗口")
        self.relocate_and_active_app(True)
