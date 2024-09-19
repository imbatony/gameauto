from abc import abstractmethod
import time
import pyautogui
from .position import TextPosition
from ..ocr import cnocr
from ..utils import get_logger


class BaseGUI(object):
    """
    GUI基类, 用于实现游戏交互操作如点击、拖拽、截图、OCR等
    单元测试时可以使用MockGUI代替
    """

    def __init__(self):
        pass

    @abstractmethod
    def active_app(self):
        """
        激活游戏应用
        """
        pass

    @abstractmethod
    def screenshot(self, filename: str, region: tuple[int, int, int, int]):
        """
        截图
        """
        pass

    @abstractmethod
    def ocr(self, image_path) -> list[TextPosition]:
        """
        OCR识别图片
        """
        pass


def ocr_result_to_text_position(line):
    # 识别结果转换为文本中心位置
    txt = line["text"]
    p1 = line["position"][0]
    p2 = line["position"][2]
    x = (p1[0] + p2[0]) / 2
    y = (p1[1] + p2[1]) / 2
    return TextPosition(txt, x, y)


class RealGUI(BaseGUI):
    """
    真实GUI类,用于实现真实的游戏交互操作
    通过pyautogui实现点击、拖拽、截图
    通过cnocr实现OCR识别
    """

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.logger = get_logger("RealGUI", config)

    def active_app(self, appname):
        """
        激活游戏应用
        """
        # Find the app window
        apps = pyautogui.getWindowsWithTitle(appname)

        # 如果找不到app，抛出异常
        if not apps or len(apps) == 0:
            raise Exception(
                f"找不到应用程序 {appname}, 请确保应用程序已经打开, 或者添加正确的应用程序名称到环境变量 GAMEAUTO_ANDROID_EMULATOR_NAME"
            )

        # Get the first app window
        app = apps[0]
        # Activate the app window
        app.activate()
        # Get the app window position
        app_x, app_y, app_width, app_height = app.left, app.top, app.width, app.height
        # 打印app窗口的位置
        self.logger.debug(
            f"app窗口位置: x={app_x}, y={app_y}, width={app_width}, height={app_height}"
        )
        return app

    def screenshot(self, filename: str, region: tuple[int, int, int, int]):
        """
        截图
        """
        pyautogui.screenshot(filename, region)

    def ocr(self, image_path) -> list[TextPosition]:
        """
        OCR识别图片
        """
        self.logger.debug(f"OCR识别图片: {image_path}")
        start_time = time.time()
        result = cnocr.ocr(image_path)
        ret = []
        for idx in range(len(result)):
            line = result[idx]
            txt_position = ocr_result_to_text_position(line)
            self.logger.debug(
                f"识别结果{idx}: {txt_position.text} {txt_position.x} {txt_position.y}"
            )
            ret.append(txt_position)
        self.logger.debug(f"OCR识别耗时: {time.time() - start_time}")
        return ret
