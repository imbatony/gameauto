from abc import abstractmethod
from ..tuples import Box, Point, TxtBox


class BaseGUI(object):
    """
    GUI基类, 用于实现游戏交互操作如点击、拖拽、截图、OCR等
    单元测试时可以使用MockGUI代替
    """

    def __init__(self):
        pass

    @abstractmethod
    def screenshot(self, filename: str, Box):
        """
        截图
        """
        pass

    def screenshot_cv2(self, region: Box):
        """
        截图, 返回cv2格式的图片, 用于快速截图识别
        """

    @abstractmethod
    def ocr(self, image_path) -> list[TxtBox]:
        """
        OCR识别图片
        """
        pass

    @abstractmethod
    def click(
        self, p: Point, duration: float = 0.2, button: str = "left", tween="linear"
    ):
        """
        点击
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
    def locateCenterOnScreen(
        self,
        image_path: str,
        region: Box,
        confidence=None,
        grayscale: bool | None = None,
        center: bool = False,  # 用于在多个位置中选择最靠近中心的位置
    ) -> Point:
        """
        识别图片位置
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

    @abstractmethod
    def locate(needleImage, haystackImage, **kwargs) -> Point:
        """
        搜索匹配的图片位置

        Args:
            needleImage: 要搜索的图片
            haystackImage: 被搜索的图片
            **kwargs: 传递给pyautogui.locate函数的参数
        """
        pass
