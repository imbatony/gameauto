from time import sleep
import time
from typing import Union
from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..actions import ClickIconAction, ACTION, ClickAction, ChangeSkillAction, DragLeftRightAction, BaseOctAction, KACTION, ClickExchangeAction
from ..constants import getIconNameByName, getFighterIconNameByNumber, getSkillIconByNumber, IconName, getTeammateIconNameByNumber, getIconPathByIconName
from ...base.tuples import Point
from ..status import OctopathStatus


class DetailAttackCommnadline(object):

    def __init__(self, cmd: str, enmery_positions: list[Point]) -> None:
        self.cmd = cmd
        self.enmery_positions = enmery_positions
        #
        # 一般cmd 由1到4个字符组成，第一个字符为攻击位置，第二个字符为攻击技能，第三个字符为攻击段数，第四个字符为攻击目标
        # 若cmd为1个字符，则表示该回合不改变攻击目标以及技能, 段数将自动变为1
        # 若cmd为2个字符，则表示该回合不改变攻击目标, 段数将自动变为1
        # 若cmd为3个字符，则表示该回合不改变攻击目标, 段数将自动变为对应的值
        # 若cmd为4个字符，则表示该回合改变攻击目标以及技能, 段数将自动变为对应的值

        if len(cmd) == 1:
            self.attack_position = int(cmd[0])
            self.attack_skill = 0
            self.attack_round = 1
            self.attack_target = 0

        elif len(cmd) == 2:
            self.attack_position = int(cmd[0])
            self.attack_skill = int(cmd[1])
            self.attack_round = 0
            self.attack_target = 0

        elif len(cmd) == 3:
            self.attack_position = int(cmd[0])
            self.attack_skill = int(cmd[1])
            self.attack_round = int(cmd[2])
            self.attack_target = 0

        elif len(cmd) == 4:
            self.attack_position = int(cmd[0])
            self.attack_skill = int(cmd[1])
            self.attack_round = int(cmd[2])
            if cmd[3] == "a":
                self.attack_target = -1
            elif cmd[3] == "b":
                self.attack_target = -2
            elif cmd[3] == "c":
                self.attack_target = -3
            elif cmd[3] == "d":
                self.attack_target = -4
            else:
                self.attack_target = int(cmd[3])

        else:
            raise ValueError("技能指令错误")
        if self.attack_position < 1 or self.attack_position > 8:
            raise ValueError("攻击位置错误")
        if self.attack_skill < -1 or self.attack_skill > 5:
            raise ValueError("攻击技能错误")
        if self.attack_round < 0 or self.attack_round > 4:
            raise ValueError("攻击段数错误")
        if self.attack_target < -4 or self.attack_target > 8:
            # 需要处理目标为队友的情况，比如治疗技能
            raise ValueError("攻击目标错误")

    def need_change_skill(self):
        return self.attack_skill != -1

    def need_change_target(self):
        return self.attack_target > 0

    def need_extra_fire(self):
        # 发动大招时，需要额外点击一次
        return self.attack_skill == 0

    def is_skill_to_teammate(self):
        return self.attack_target < 0

    def get_actions(self, ctx: OctopathTaskCtx) -> list[Union[ACTION, KACTION]]:
        actions = []

        if self.need_change_skill():
            person_icon = getFighterIconNameByNumber(self.attack_position)
            actions.append(ACTION(f"点击人物{self.attack_position}", ClickIconAction, [person_icon], 1))
            if ctx.need_exchange(self.attack_position):
                actions.append(ACTION("交换前后排", ClickExchangeAction, [self.attack_position], 1))
            if self.need_change_target():
                target_pos = ctx.get_enemy_pos(self.attack_target)
                actions.append(ACTION(f"点击敌人{self.attack_target}", ClickAction, [target_pos, 0.4], 1))
            skill_icon = getSkillIconByNumber(self.attack_skill)
            actions.append(ACTION(f"点击技能{self.attack_skill}", ChangeSkillAction, [skill_icon.relative_pos, self.attack_round], 1))
            if self.need_extra_fire():
                actions.append(ACTION("点击确认", ClickIconAction, [IconName.SKILL_ENABLE], 0.5))
            if self.is_skill_to_teammate():
                teammateIconName = getTeammateIconNameByNumber(self.attack_target)
                actions.append(ACTION(f"点击第{-self.attack_target}行队友", ClickIconAction, [teammateIconName], 0.5))
        return actions


class ManualAttackSingleRoundCommand(BaseOctopathCommand):
    __alternate_names__ = ["手动攻击单回合", "ManualAttackSingleRound"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, attackActions: str, wait_str="true", wait_max_str="30", isAllMaxStr="false") -> CommandReturnCode:
        """
        手动攻击单回合

        :return: 执行结果
        """
        ctx.logger.info("手动攻击单回合")
        wait_for_next_round = wait_str.lower() == "true"
        isAllMaxStr = isAllMaxStr.lower() == "true"
        # 解析攻击动作
        attackAction = attackActions.split(",")
        if len(attackAction) <= 0 or len(attackAction) > 4:
            ctx.logger.error("手动攻击单回合失败, 攻击指令错误")
            return CommandReturnCode.FAILED

        detailAttackCommnadline: list[DetailAttackCommnadline] = []
        for i in range(len(attackAction)):
            detailAttackCommnadline.append(DetailAttackCommnadline(attackAction[i], ctx.enemy_positions))
        actions: list[Union[ACTION, KACTION]] = []
        for i in range(len(detailAttackCommnadline)):
            actions.extend(detailAttackCommnadline[i].get_actions(ctx))
        if isAllMaxStr:
            actions.append(ACTION("点击最大攻击", ClickIconAction, [IconName.BATTLE_ALL_MAX], 1))
        ret = cls.runActionChain(ctx, *actions)
        if ret != CommandReturnCode.SUCCESS:
            ctx.logger.error("手动攻击单回合失败")
            return ret
        sleep(0.5)
        ret = cls.runAction(ctx, ACTION("点击攻击", ClickIconAction, [IconName.ATTACK], 2))
        if ret != CommandReturnCode.SUCCESS:
            ctx.logger.error("手动攻击单回合失败")
            return ret
        if not wait_for_next_round:
            return CommandReturnCode.SUCCESS

        wait_for_next_round = int(wait_max_str)
        start_time = time.time()
        sleep(10)
        while time.time() - start_time < wait_for_next_round:
            ctx.renew_current_screen()
            status = ctx.detect_status()
            if OctopathStatus.is_can_attack(status):
                ctx.logger.debug("手动攻击单回合成功, 进入下一回合")
                return CommandReturnCode.SUCCESS
            elif not OctopathStatus.is_combat(status):
                ctx.logger.debug("手动攻击单回合成功, 战斗结束")
                return CommandReturnCode.SUCCESS
            sleep(1)
        ctx.logger.error("手动攻击单回合超时")
        return CommandReturnCode.FAILED


class ManualAttackCommand(BaseOctopathCommand):
    __alternate_names__ = ["手动攻击", "ManualAttack"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, attackActions: str) -> CommandReturnCode:
        # 先使用OCR识别敌人数量

        # 将每个回合的攻击动作分割
        singleRoundCode = attackActions.split(";")

        # 敌人位置替换成坐标
        # 逐个执行每个回合的攻击动作

        for i in range(len(singleRoundCode)):
            code = ManualAttackSingleRoundCommand.run(ctx, singleRoundCode[i])
            if code != CommandReturnCode.SUCCESS:
                ctx.logger.error("手动攻击失败")
                return code


class ForceSetEnemyCommand(BaseOctopathCommand):
    __alternate_names__ = ["强制设置敌人", "ForceSetEnemy"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, enemyPositions: str) -> CommandReturnCode:
        """
        强制设置敌人

        :return: 执行结果
        """
        ctx.logger.info("强制设置敌人")
        # 解析敌人位置
        enemyPositionList = enemyPositions.split(";")

        ctx.reset_enemy()

        for enemyPosition in enemyPositionList:
            pos = enemyPosition.split(",")
            if len(pos) != 2:
                ctx.logger.error("强制设置敌人失败, 位置错误")
                return CommandReturnCode.FAILED
            ctx.add_enemy_pos(Point(int(pos[0]), int(pos[1])))

        ctx.logger.debug(f"强制设置敌人成功, 位置: {enemyPositions}")
        return CommandReturnCode.SUCCESS


class AutoAttackCommand(BaseOctopathCommand):
    __alternate_names__ = ["委托战斗", "AutoAttack"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, max_wait_time_str="30") -> CommandReturnCode:
        """
        委托战斗

        :return: 执行结果
        """
        ctx.logger.info("委托战斗")
        max_wait_time = int(max_wait_time_str)
        # 检查是否已经进入战斗
        start_time = time.time()
        cls.runActionChain(ctx, ACTION("点击委托", ClickIconAction, [IconName.BATTLE_DELEGATE], 1), ACTION("点击委托", ClickIconAction, [IconName.ATTACK], 1))
        sleep(10)
        while time.time() - start_time < max_wait_time:
            ctx.renew_current_screen()
            status = ctx.detect_status()
            if not OctopathStatus.is_combat(status):
                ctx.logger.debug("手动攻击单回合成功, 战斗结束")
                return CommandReturnCode.SUCCESS
            sleep(1)
        ctx.logger.error("手动攻击单回合超时")
        return CommandReturnCode.FAILED
