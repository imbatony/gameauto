import adbutils
from adbutils import AdbDevice, AppInfo
from .base import BaseGUI, BaseApp
from ..tuples import Box, Point
from ...gameconstants import ADB_HOST, ADB_PORT, ANDRIOD_GAME_PACKAGE_NAME, ANDRIOD_GAME_ACTIVITY_NAME, DEFAULT_ANDROID_SERIAL
from PIL import Image


class AndriodApp(BaseApp):
    def __init__(self, device: AdbDevice, appInfo: AppInfo):
        super().__init__()
        self.device = device
        self.appInfo = appInfo

    def app_position(self) -> Box:
        # 获取应用位置和长宽信息
        (width, height) = self.device.window_size(landscape=True)  # force landscape mode
        # Android的坐标原点在左上角, 所以top是0, left是0
        return Box(0, 0, width, height)

    def __str__(self) -> str:
        return super().__str__() + f"({self.appInfo.package})" + f"({self.app_position()})"


class ADBGUI(BaseGUI):
    def __init__(self, config: dict):
        super().__init__(config=config)
        adb_config = config.get("game", {}).get("adb", {})
        adb_host = adb_config.get("host", ADB_HOST)
        adb_port = adb_config.get("port", ADB_PORT)
        adb_serial = adb_config.get("serial", DEFAULT_ANDROID_SERIAL)
        self.adb_package = adb_config.get("package", ANDRIOD_GAME_PACKAGE_NAME)
        self.package_activity = adb_config.get("activity", ANDRIOD_GAME_ACTIVITY_NAME)
        self.device_addr = adb_config.get("device_addr", None)

        try:
            # Set socket timeout to 10 (default None)
            self.adb = adb = adbutils.AdbClient(host=adb_host, port=adb_port, socket_timeout=10)

            if self.device_addr:
                self.logger.info(f"尝试连接ADB设备: {self.device_addr}")
                result = adb.connect(self.device_addr, 10)
                self.logger.info(f"连接ADB设备结果: {result}")

            if adb_serial:
                self.device = adb.device(serial=adb_serial)
            else:
                self.device = adb.device()
        except Exception as e:
            self.logger.error(f"连接ADB失败: {adb_host}:{adb_port}, {e}")
            raise e

        self.logger.info(f"连接ADB成功: {adb_host}:{adb_port}, 设备: {self.device.serial}, 应用: {self.adb_package}, 分辨率: {self.device.window_size()}")

    def active_app(self):
        # 如果处于息屏状态,先唤醒设备
        if not self.device.is_screen_on():
            self.logger.info("设备处于息屏状态,请手动解锁设备")
            self.device.keyevent("KEYCODE_POWER")
            return None

        app_info = self.device.app_current()
        if app_info:
            self.logger.info(f"当前应用: {app_info.package}")

        if app_info and app_info.package == self.adb_package:
            return AndriodApp(self.device, self.adb_package)

        self.logger.info("当前应用不是游戏应用, 启动游戏应用")
        # 如果当前应用不是游戏应用,先确认应用是否安装
        app_info = self.device.app_info(self.adb_package)
        if not app_info:
            self.logger.error(f"应用未安装: {self.adb_package}")
            return None

        # 启动游戏应用
        self.logger.info(f"应用已经安装,启动游戏应用: {self.adb_package}")

        self.device.app_start(self.adb_package, self.package_activity)

        self.logger.info(f"启动游戏应用成功: {self.adb_package}")

        return AndriodApp(self.device, app_info)

    def __str__(self) -> str:
        return super().__str__() + f"({self.device.serial})"

    def screenshot(self, filename: str = None, region: Box = None) -> Image.Image:
        image: Image.Image = self.device.screenshot()
        image = image.crop(region)
        if filename:
            image.save(filename)
        return image

    def touch(self, p: Point, duration: float = 0.2):
        """
        点击屏幕
        """
        self.logger.debug(f"点击坐标: {p}")
        if duration > 0:
            self.device.swipe(p.x, p.y, p.x, p.y, duration)
        else:
            self.device.click(p.x, p.y)

    def dragLeftRight(
        self,
        start: Point,
        left: Point,
        right: Point,
        duration: float = 0.8,
        single_duration=0.2,
    ):
        """
        左右滑动
        """
        d_sum = 0
        while d_sum < duration:
            d_sum += single_duration * 4
            self.device.swipe(start.x, start.y, left.x, left.y, single_duration)
            self.device.swipe(left.x, left.y, start.x, start.y, single_duration)
            self.device.swipe(start.x, start.y, right.x, right.y, single_duration)
            self.device.swipe(right.x, right.y, start.x, start.y, single_duration)
            # self.device.click(start.x, start.y)
