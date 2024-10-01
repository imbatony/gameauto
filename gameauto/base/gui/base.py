from abc import abstractmethod
import os
from pathlib import Path
import time
from typing import Union, Optional, Generator
from ..tuples import Box, Point, TxtBox
from PIL import Image
import numpy as np
from ...utils import get_logger
import pyautogui
import cv2
from pyautogui import ImageNotFoundException


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


class BaseApp(object):
    """
    App基类
    用于获取应用位置等信息
    """

    def __init__(self):
        pass

    @abstractmethod
    def app_position(self) -> Box:
        """
        获取应用位置
        """
        pass

    @property
    def left(self) -> int:
        return self.app_position().left

    @property
    def top(self) -> int:
        return self.app_position().top

    @property
    def width(self) -> int:
        return self.app_position().width

    @property
    def height(self) -> int:
        return self.app_position().height


class BaseGUI(object):
    """
    GUI基类, 用于实现游戏交互操作如点击、拖拽、截图、OCR等
    单元测试时可以使用MockGUI代替
    """

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)

    @abstractmethod
    def screenshot(self, filename: str = None, region: Box = None) -> Image.Image:
        """
        截图
        """
        pass

    @abstractmethod
    def touch(self, p: Point, duration: float = 0.2):
        """
        触摸, 与click相比点击释放有延迟
        更适用于模拟触摸屏幕
        """
        pass

    @abstractmethod
    def drag(self, start: Point, end: Point, duration: float = 0.8):
        """
        拖拽
        """
        pass

    @abstractmethod
    def active_app(self, **kwargs) -> BaseApp:
        """
        激活应用
        """
        pass

    @abstractmethod
    def dragLeftRight(
        self,
        start: Point,
        left: Point,
        right: Point,
        duration: float = 0.8,
        single_duration: float = 0.2,
    ):
        """
        拖拽
        """
        pass

    def locate(self, needleImage: Union[str, Image.Image, Path], haystackImage: Union[str, Image.Image, Path], **kwargs) -> Optional[Box]:
        """
        搜索匹配的图片位置, 返回中心点
        Args:
            needleImage: 要搜索的图片
            haystackImage: 被搜索的图片
            **kwargs: 传递给pyautogui.locate函数的参数
        """
        if needleImage is None or haystackImage is None:
            self.logger.debug("图片为空")
            return None
        # pyautogui只支持str类型的路径
        needleImage = self._preprocess_images(needleImage)
        haystackImage = self._preprocess_images(haystackImage)
        try:
            box = pyautogui.locate(needleImage, haystackImage, **kwargs)
        except ImageNotFoundException as e:
            return None
        if box is None:
            return None
        else:
            return Box(box[0], box[1], box[2], box[3])

    @classmethod
    def _preprocess_images(cls, img: Union[str, Path, Image.Image, np.ndarray]) -> np.ndarray:
        """

        Args:
            img ():

        Returns:
            BGR format ndarray: [H, W, 3]

        """
        if isinstance(img, (str, Path)):
            if not os.path.isfile(img):
                raise FileNotFoundError(img)
            return cv2.imread(img, cv2.IMREAD_COLOR)
        elif isinstance(img, Image.Image):
            img = np.asarray(img.convert("RGB"), dtype="float32")
        if isinstance(img, np.ndarray):
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            raise TypeError("type %s is not supported now" % str(type(img)))

    def locateAll(self, needleImage: Union[str, Image.Image, Path], haystackImage: Union[str, Image.Image, Path], **kwargs) -> Generator[Box, None, None]:
        """
        搜索匹配的图片位置, 返回矩形框
        Args:
            needleImage: 要搜索的图片
            haystackImage: 被搜索的图片
            **kwargs: 传递给pyautogui.locate函数的参数
        """
        # pyautogui只支持str类型的路径
        if isinstance(needleImage, Path):
            needleImage = str(needleImage)
        if isinstance(haystackImage, Path):
            haystackImage = str(haystackImage)
        self.logger.debug(f"搜索图片位置: {needleImage} in {haystackImage}")
        try:
            genertor = pyautogui.locateAll(needleImage, haystackImage, **kwargs)
            if genertor is None:
                yield None
                return None
            for box in genertor:
                yield Box(box[0], box[1], box[2], box[3])
        except ImageNotFoundException as e:
            yield None

    def ocr(
        self,
        image_fp: Union[str, Path, Image.Image, np.ndarray],
    ) -> list[TxtBox]:
        """
        OCR识别图片
        """
        self.logger.debug("OCR识别图片")
        start_time = time.time()
        from ...ocr import cnocr

        result = cnocr.ocr(image_fp)
        ret = []
        for idx in range(len(result)):
            line = result[idx]
            txt_box = ocr_result_to_txt_box(line)
            self.logger.debug(f"识别结果{idx}: {txt_box}")
            ret.append(txt_box)
        self.logger.debug(f"OCR识别耗时: {time.time() - start_time}")
        return ret
