import time
from .base import BaseGUI
from ...utils import get_logger
import pyautogui
from ...ocr import cnocr
from ..tuples import TxtBox, Point, Box


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
    TODO: 未来可以支持通过adb实现手机端的操作以及与模拟器的交互
    """

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.logger = get_logger("RealGUI", config)

    def screenshot(self, filename: str, region: tuple[int, int, int, int]):
        """
        截图
        """
        self.logger.debug(f"截图: {filename}, {region}")
        pyautogui.screenshot(filename, region)

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

    def click(self, p: Point, duration: float = 0.2, button: str = "left"):
        """
        点击
        """
        self.logger.debug(f"点击: {p}")
        pyautogui.click(p.x, p.y, duration=duration, button=button)

    def touch(self, p: Point, duration: float = 0.2):
        """
        触摸, 与click的区别在于不需要指定button,并且按键有持续时间
        """
        self.logger.debug(f"触摸: {p}")
        # 先移动到目标位置
        pyautogui.moveTo(x=p.x, y=p.y, duration=duration)
        # 再按下
        pyautogui.mouseDown(duration=duration)
        # 再抬起
        pyautogui.mouseUp()

    def locateCenterOnScreen(
        self,
        image_path: str,
        region: Box,
        confidence,
        grayscale: bool | None,
        center: bool = False,  # 用于在多个位置中选择最靠近中心的位置
    ) -> Point:
        """
        识别图片位置
        """
        self.logger.debug(f"识别图片位置: {image_path}")
        try:
            pos = None
            if not center:
                pos = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region,
                    confidence=confidence,
                    grayscale=grayscale,
                )
            else:
                # 找到所有位置
                pos_generator = pyautogui.locateAllOnScreen(
                    image_path,
                    region=region,
                    confidence=confidence,
                    grayscale=grayscale,
                )
                if pos_generator is None:
                    return None
                # 选择最靠近中心的位置
                center_pos = Point(region[0] + region[2] / 2, region[1] + region[3] / 2)
                min_distance = 999999
                for p in pos_generator:
                    # 计算距离
                    distance = (p[0] - center_pos.x) ** 2 + (p[1] - center_pos.y) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        pos = p
            if pos is None:
                self.logger.debug(f"找不到图片{image_path}")
                return None
            else:
                self.logger.debug(f"找到图片{image_path}位置: {pos}")
                return Point(pos[0], pos[1])
        except Exception:
            self.logger.exception(f"识别图片位置异常")
            return None

    def dragLeftRight(
        self,
        start: Point,
        left: Point,
        right: Point,
        duration: float = 0.8,
        single_duration=0.2,
    ):
        """
        来回拖拽
        """
        pyautogui.moveTo(start)
        pyautogui.mouseDown()
        d_sum = 0
        while d_sum < duration:
            d_sum += single_duration * 4
            pyautogui.moveTo(left, duration=single_duration)
            pyautogui.moveTo(start, duration=single_duration)
            pyautogui.moveTo(right, duration=single_duration)
            pyautogui.moveTo(start, duration=single_duration)
        pyautogui.mouseUp()

    def locate(needleImage, haystackImage, **kwargs) -> Point:
        """
        搜索匹配的图片位置
        """
        box: Box = pyautogui.locate(needleImage, haystackImage, kwargs)
        if box is None:
            return None
        else:
            return box.center
