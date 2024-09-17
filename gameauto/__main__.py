import argparse
  
parser = argparse.ArgumentParser(description='GameAuto')
parser.add_argument('--game', type=str, default='game', help='game name')
parser.add_argument('--command', type=str, default='1.0', help='game command')

args = parser.parse_args()

def init():
    import paddle
    import paddlehub as hub

    print("初始化OCR模型...")
    paddle.utils.run_check()  # 检查PaddleOCR是否安装成功
    # 加载移动端预训练模型
    ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    # 服务端可以加载大模型，效果更好 
    # ocr = hub.Module(name="chinese_ocr_db_crnn_server")

    print("初始化完成")

if args.game == 'octpath':
    import octpath
    init()
    octpath.main(args.command)
else:
    print(f"找不到游戏{args.game}")