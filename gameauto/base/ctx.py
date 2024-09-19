from .position import TextPosition

class BaseTaskCtx(object):
    """
    任务上下文
    任务执行过程中的上下文信息
    """
    # 最大历史状态记录长度
    max_status_len = 10
    # 最大历史截图记录长度
    max_screenshots_len = 10
    # 最大历史ocr结果记录长度
    max_ocr_results_len = 10

    def __init__(self):
        self.app = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        # 截图
        self.his_screenshots: list[str] = []
        self.cur_screenshot: str | None = None
        self.his_status: list[int] = []
        self.cur_status = -1
        self.cur_ocr_result: list[TextPosition] = []
        self.his_ocr_results: list[list[TextPosition]] = []

    def update_app(self, app):
        self.app = app
        self.x = app.left
        self.y = app.top
        self.width = app.width
        self.height = app.height
        return self

    def update_screenshot(self, screenshot):
        if len(self.his_screenshots) >= self.max_screenshots_len:
            self.his_screenshots.pop(0)
        self.his_screenshots.append(screenshot)
        self.cur_screenshot = screenshot
        return self

    def update_status(self, status: int):
        if len(self.his_status) >= self.max_status_len:
            self.his_status.pop(0)
        self.his_status.append(status)
        self.cur_status = status
        return self

    def get_last_status(self):
        return self.cur_status

    def get_history_status(self, last: int):
        # 获取倒数第last个状态
        # last=0表示最后一个状态 即当前状态
        index = len(self.his_status) - last - 1
        if index < 0:
            index = 0
        return self.his_status[index]

    def update_ocr_result(self, ocr_result):
        if len(self.his_ocr_results) >= self.max_ocr_results_len:
            self.his_ocr_results.pop(0)
        self.cur_ocr_result = ocr_result
        self.his_ocr_results.append(ocr_result)
        return self