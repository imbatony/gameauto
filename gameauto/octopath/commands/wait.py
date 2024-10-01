import asyncio
import queue
import threading
from time import sleep
from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..constants import getIconNameByName, getIconPathByIconName, IconName
from ..actions import DragLeftRightAction, ACTION, ClickAction, ClickIconAction
from ..status import OctopathStatus


class WaitCommand(BaseOctopathCommand):
    __alternate_names__ = ["等待", "Wait"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, seconds_str: str) -> CommandReturnCode:
        """
        等待, 单位: 秒 用于添加等待时间

        :param seconds: 等待时间
        :return: 执行结果
        """
        seconds = int(seconds_str)
        ctx.logger.info("等待 %d 秒", seconds)
        sleep(seconds)
        return CommandReturnCode.SUCCESS


class WaitUntilIconFoundCommand(BaseOctopathCommand):
    __alternate_names__ = ["等待图标出现", "WaitUntilIconFound"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, icon_name_str: str, max_wait_str: str = "1", wait_interval_str: str = "0.5") -> CommandReturnCode:
        """
        等待图标出现

        :param icon_name: 图标名称
        :param max_wait_str: 最大等待时间

        :return: 执行结果
        """
        ctx.logger.info("等待图标 %s 出现", icon_name_str)
        icon_name = getIconNameByName(icon_name_str)
        if icon_name is None:
            ctx.logger.error(f"未找到图标: {icon_name_str}")
            return CommandReturnCode.FAILED

        wait = float(max_wait_str)
        wait_interval = float(wait_interval_str)
        start = ctx.getCurTime()
        image = getIconPathByIconName(icon_name)
        while ctx.getCurTime() - start < wait:
            if ctx.findImageInScreen(image) is not None:
                return CommandReturnCode.SUCCESS
            sleep(wait_interval)

        ctx.logger.error(f"等待图标 {icon_name_str} 超时")
        return CommandReturnCode.FAILED


class WalkAroundWaitBattleCommnad(BaseOctopathCommand):
    __alternate_names__ = ["行走触敌", "WalkAroundWaitBattle"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, max_wait_str: str = "16", detect_interval_str: str = "4") -> CommandReturnCode:
        """
        行走触敌

        :param
        max_wait_str: 最大等待时间
        detect_interval_str: 检测间隔
        """

        ctx.logger.info("原地走动, 等待战斗")
        wait = float(max_wait_str)
        detect_interval = float(detect_interval_str)
        # TODO:需要改成多进程来实现, 一个进程负责行走, 一个进程负责检测战斗
        data_queue = queue.Queue(maxsize=1)

        def walkAround(max_wait: float) -> bool:
            """
            行走触敌
            """
            start = ctx.getCurTime()
            while ctx.getCurTime() - start < max_wait:
                code = cls.runAction(ctx, ACTION("左右移动", DragLeftRightAction, [1 / 8, 2]))
                if code != CommandReturnCode.SUCCESS:
                    return False
                try:
                    status = data_queue.get_nowait()
                    if OctopathStatus.is_combat(status):
                        ctx.logger.info("检测到战斗")
                        return True
                except queue.Empty:
                    continue

            return False

        def detectUntilInCombat(max_wait: float, detect_interval: float) -> bool:
            """
            检测是否进入战斗
            """
            detect_start = ctx.getCurTime()
            while ctx.getCurTime() - detect_start < max_wait:
                detect_start_time = ctx.getCurTime()
                if ctx.isInCombat(renew=True):
                    data_queue.put(ctx.cur_status)
                    return True
                if ctx.getCurTime() - detect_start_time < detect_interval:
                    sleep(detect_interval - (ctx.getCurTime() - detect_start_time))

        thread1 = threading.Thread(target=walkAround, args=(wait,))
        thread2 = threading.Thread(target=detectUntilInCombat, args=(wait, detect_interval))
        thread1.start()
        thread2.start()
        thread1.join()

        return CommandReturnCode.SUCCESS if ctx.isInCombat() else CommandReturnCode.FAILED


class LongClickWaitEnterBattleCommand(BaseOctopathCommand):
    __alternate_names__ = ["长按等待进入战斗", "LongClickWaitEnterBattle"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, max_wait_str: str = "12", wait_interval_str: str = "0.5") -> CommandReturnCode:
        """
        长按等待进入战斗

        :param max_wait_str: 最大等待时间

        :return: 执行结果
        """
        ctx.logger.info("长按等待进入战斗")
        wait = float(max_wait_str)
        wait_interval = float(wait_interval_str)
        cls.runAction(ctx, ACTION("长按进入战斗", ClickAction, [None, 5]))

        start = ctx.getCurTime()
        while ctx.getCurTime() - start < wait:
            if ctx.isInCombat(renew=True):
                ctx.logger.info("进入战斗")
                return CommandReturnCode.SUCCESS
            sleep(wait_interval)

        return CommandReturnCode.FAILED


class LongClickAndExitFightCommand(BaseOctopathCommand):
    __alternate_names__ = ["长按退出竞技场", "LongClickAndExitFight"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx) -> CommandReturnCode:
        """
        长按退出竞技场

        :param max_wait_str: 最大等待时间

        :return: 执行结果
        """
        ctx.logger.info("长按退出竞技场")
        # 需要增加战斗异常时强制退出的逻辑
        return cls.runActionChain(
            ctx,
            ACTION("长按退出竞技场", ClickAction, [None, 5], 4),
            ACTION("点击退出竞技场", ClickIconAction, [IconName.ARENA_EXIT_CONFIRM], 2),
            ACTION("点击退出竞技场", ClickIconAction, [IconName.ARENA_EXIT_CLOSE], 4),
        )


class WaitBattleEndCommand(BaseOctopathCommand):
    __alternate_names__ = ["等待战斗结束", "WaitBattleEnd"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, max_wait_str: str = "60", wait_interval_str: str = "0.5") -> CommandReturnCode:
        """
        等待战斗结束

        :param max_wait_str: 最大等待时间

        :return: 执行结果
        """
        ctx.logger.info("等待战斗结束")
        wait = float(max_wait_str)
        wait_interval = float(wait_interval_str)

        start = ctx.getCurTime()
        while ctx.getCurTime() - start < wait:
            if not ctx.isInCombat(renew=True):
                ctx.logger.info("战斗结束,点击退出战斗")
                code = cls.runActionChain(ctx, ACTION("点击退出战斗", ClickAction, [], 0.5), ACTION("点击退出战斗", ClickAction, []))
                return code
            sleep(wait_interval)

        return CommandReturnCode.FAILED
