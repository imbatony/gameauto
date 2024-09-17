import argparse
import sys
import time

if __package__ is None and not getattr(sys, "frozen", False):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from gameauto import GameAuto


def init():
    print("初始化OCR模型...")
    import paddle
    import paddlehub as hub
    paddle.utils.run_check()  # 检查PaddleOCR是否安装成功
    # 加载移动端预训练模型
    ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    # 服务端可以加载大模型，效果更好
    # ocr = hub.Module(name="chinese_ocr_db_crnn_server")
    print("初始化完成")

def main():
    # 解析命令
    parser = argparse.ArgumentParser(prog="GameAuto")
    parser.add_argument("game", type=str, help="游戏名称,如octopath")
    parser.add_argument("action", type=str, help="操作名称,如start")
    parser.add_argument(
        "--config", default=None, help="JSON配置文件路径,默认为gameauto.json"
    )
    args = parser.parse_args()

    game = args.game
    action = args.action
    config = args.config
    try:
        gameauto = GameAuto(game, config)
    except ModuleNotFoundError as e:
        print(e)
        return
    if not gameauto.support_action(action):
        print(f"游戏{game}不支持操作{action}")
        return
    init()
    try:
        print(f"开始执行操作{action}")
        start_time = time.time()  # 记录开始时间
        gameauto.run(action)
        end_time = time.time()  # 记录结束时间
        print(f"操作{action}执行完成,耗时{end_time - start_time:.2f}秒")
    except KeyboardInterrupt:  # 捕捉 Ctrl + C 中断信号
        print("中断操作")
        end_time = time.time()  # 记录结束时间
        print(f"操作{action}执行中断,耗时{end_time - start_time:.2f}秒")
        exit(0)

if __name__ == "__main__":
    main()
