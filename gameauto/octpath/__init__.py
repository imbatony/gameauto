def main(command):
    if command == 'bianyu_farm':
        from .farm.bianyu_farm import BianyuFarm
        farm = BianyuFarm()
        farm.execute(None)