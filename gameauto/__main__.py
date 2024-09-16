# 解析命令
import argparse
import sys
if __package__ is None and not getattr(sys, 'frozen', False):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from gameauto import GameAuto

def main():
    parser = argparse.ArgumentParser(prog='GameAuto')
    parser.add_argument('game', help='game name')
    parser.add_argument('action', help='action name')
    parser.add_argument('--config', default=None, help='config file')
    args = parser.parse_args()

    game = args.game
    action = args.action
    config = args.config
    gameauto = GameAuto(game, config)
    gameauto.run(action)


if __name__ == '__main__':
    main()
