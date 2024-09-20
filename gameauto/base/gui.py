from abc import abstractmethod
import time
import pyautogui
from .tuples import TxtBox
from ..ocr import cnocr
from ..utils import get_logger
from pyscreeze import center, pixel, pixelMatchesColor, screenshot


class BaseGUI(object):
    """
    GUI基类, 用于实现游戏交互操作如点击、拖拽、截图、OCR等
    单元测试时可以使用MockGUI代替
    """

    def __init__(self):
        pass

    @abstractmethod
    def screenshot(self, filename: str, region: tuple[int, int, int, int]):
        """
        截图
        """
        pass

    @abstractmethod
    def ocr(self, image_path) -> list[TxtBox]:
        """
        OCR识别图片
        """
        pass


def ocr_result_to_txt_box(ocr_result_line: dict) -> TxtBox:
    position = ocr_result_line["position"]
    text = ocr_result_line["text"]
    leftTop: list[float, float] = position[0]
    rightBottom: list[float, float] = position[2]
    return TxtBox(
        text=text,
        left=int(leftTop[0]),
        top=int(leftTop[1]),
        width=int(rightBottom[0] - leftTop[0]),
        height=int(rightBottom[1] - leftTop[1]),
    )


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

    def screenshot(self, filename: str, region: tuple[int, int, int, int]):
        """
        截图
        """
        screenshot(filename, region)

    def ocr(self, image_path) -> list[TxtBox]:
        """
        OCR识别图片
        """
        self.logger.debug(f"OCR识别图片: {image_path}")
        start_time = time.time()
        result = cnocr.ocr(image_path)
        ret = []
        for idx in range(len(result)):
            line = result[idx]
            txt_box = ocr_result_to_txt_box(line)
            self.logger.debug(f"识别结果{idx}: {txt_box}")
            ret.append(txt_box)
        self.logger.debug(f"OCR识别耗时: {time.time() - start_time}")
        return ret
