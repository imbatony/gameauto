import os
from time import sleep
import pyautogui
import paddle
import paddlehub as hub
import cv2
import logging
from gameconstants import ANDROID_EMULATOR_NAME

def _get_center(box, offset_x=0, offset_y=0)-> tuple[int, int]:
    p1 = box[0]
    p2 = box[3]
    return (p1[0] + p2[0]) // 2 + offset_x, (p1[1] + p2[1]) // 2 + offset_y


class BaseCommand:
    def __init__(self, debug: bool = False, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
        self.step_interval = 0.5
        self.logger = logging.getLogger(__name__)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.app = None

    def find_text_and_click(self, image_path, text, click=True, step_interval = -1, clean_file = True)-> bool:
        if step_interval == -1:
            step_interval = self.step_interval
        # 识别图片中的文字
        img = cv2.imread(image_path)
        self.logger.debug(f"识别图片中的文字: {text}")
        result = self.ocr.recognize_text(images=[img], use_gpu=False)[0]
        if clean_file:
            os.remove(image_path)
        self.logger.debug(f"识别结果: {result}")
        for line in result['data']:
            if text in line['text']:
                self.logger.debug(f"找到文字: {text}")
                if click:
                    self.logger.debug(f"点击文字: {text}")
                    self.logger.debug(f"文字位置: {line['text_box_position']}")
                    x, y = _get_center(line['text_box_position'], offset_x=self.app.left, offset_y=self.app.top)
                    pyautogui.click(x, y)
                if clean_file:
                    os.remove(image_path)
                return True
        return False

    def app_screenshot(self, path: str)-> None:
        # 截取app窗口的屏幕截图
        self.logger.debug(f"截取app窗口的屏幕截图: {path}")
        app_x, app_y, app_width, app_height = self.relocate_and_active_app(False)
        region = (app_x, app_y, app_width, app_height)
        pyautogui.screenshot(path, region=region)

    def ocr_get_txt_pos(self, img_path, txt, printResult=True):
        # 识别图片中的文字
        result = pyautogui.locateCenterOnScreen(img_path, confidence=0.8)
        if printResult:
            print(f"识别结果: {result}")
        return result

    def relocate_and_active_app(self, is_actvie)->tuple:
        # Find the app window
        apps = pyautogui.getWindowsWithTitle(ANDROID_EMULATOR_NAME)
        
        # 如果找不到app，抛出异常
        if not apps:
            raise Exception(f"找不到应用程序 {ANDROID_EMULATOR_NAME}, 请确保应用程序已经打开, 或者添加正确的应用程序名称到环境变量 GAMEAUTO_ANDROID_EMULATOR_NAME")
        
        # Get the first app window
        app = apps[0]
        self.app = app
        # Activate the app window
        if is_actvie:
            app.activate()
        # Get the app window position
        app_x, app_y, app_width, app_height = app.left, app.top, app.width, app.height
        # 打印app窗口的位置
        self.logger.debug(f"app窗口位置: x={app_x}, y={app_y}, width={app_width}, height={app_height}")
        return app_x, app_y, app_width, app_height

if __name__ == '__main__':
    command = BaseCommand(debug=True)
    command.relocate_and_active_app(True)

    # 获取临时文件夹
    temp_dir = os.environ.get("TEMP")

    #获得当前时间戳
    import time
    timestamp = int(time.time())
    image_path = os.path.join(temp_dir, f"{timestamp}.png")
    command.app_screenshot(image_path)
    print(f"截图保存到: {image_path}")
    command.find_text_and_click(image_path, "大陆地图" , click=True)
