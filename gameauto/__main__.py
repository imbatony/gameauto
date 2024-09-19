import argparse
import sys
import time

if __package__ is None and not getattr(sys, "frozen", False):
    # direct call of __main__.py
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from gameauto import GameAuto


def main():
    # 解析命令
    parser = argparse.ArgumentParser(prog="GameAuto")
    parser.add_argument("game", type=str, help="游戏名称,如octopath")
    parser.add_argument(
        "task", type=str, help="内建任务名称或者自定义脚本,如farming 或者 myscript.txt"
    )
    parser.add_argument(
        "--config", default=None, help="JSON配置文件路径,默认为gameauto.json"
    )
    args = parser.parse_args()

    game = args.game
    task = args.task
    # 检查task是否是自定义脚本文件
    custom_script = False
    if task.endswith(".txt"):
        custom_script = True
    # 检查文件是否存在
    if custom_script and not os.path.exists(task):
        print(f"自定义脚本文件{task}不存在")
        return

    config = args.config
    try:
        gameauto = GameAuto(game, config)
    except ModuleNotFoundError as e:
        print("初始化GameAuto失败,请检查游戏名称是否正确")
        return

    if not custom_script and not gameauto.support_task(task):
        print(f"游戏{game}不支持内建任务:{task}")
        return
    from .ocr import dummy

    # 初始化OCR, 避免第一次调用OCR耗时过长
    dummy()
    try:
        if not custom_script:
            print(f"开始执行任务{task}")
        else:
            print(f"开始执行自定义脚本{task}")
        start_time = time.time()  # 记录开始时间

        if not custom_script:
            gameauto.run(task)
        else:
            gameauto.run_script(task)
        end_time = time.time()  # 记录结束时间
        print(f"任务{task}执行完成,耗时{end_time - start_time:.2f}秒")
    except KeyboardInterrupt:  # 捕捉 Ctrl + C 中断信号
        print("中断任务")
        end_time = time.time()  # 记录结束时间
        print(f"任务{task}执行中断,耗时{end_time - start_time:.2f}秒")
        exit(0)


if __name__ == "__main__":
    main()
