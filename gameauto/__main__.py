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
    from .ocr import cnocr
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

# if __name__ == "__main__":
#     img_fp = 'C:\\code\\gameauto\\test\\testdata\\image\\octopath\\main.png'
#     print(f"加载ocr模型")
#     start_time = time.time()
#     from cnocr import CnOcr
#     # 所有参数都使用默认值
#     ocr = CnOcr(rec_model_name='densenet_lite_136-gru', det_model_name='db_shufflenet_v2_small', det_more_configs={'rotated_bbox': False})
#     ellipsis = time.time() - start_time
#     print(f"加载完成,耗时{ellipsis:.2f}秒")
#     start_time = time.time()
#     out = ocr.ocr(img_fp)
#     ellipsis = time.time() - start_time
#     print(f"识别完成,耗时{ellipsis:.2f}秒")
#     for line in out:
#         text = line["text"]
#         p1 = line["position"][0]
#         p2 = line["position"][2]
#         x,y = p1[0], p1[1]
#         x1,y1 = p2[0], p2[1]
#         print(f"识别结果: {text},位置:({x},{y})-({x1},{y1})")
