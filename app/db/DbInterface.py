import configparser
import os
from db.DbFactory import build_db_obj


class DbSingleton:
    __instance = None

    def __init__(self):
        parse = configparser.ConfigParser()
        parse.read(os.path.join('conf', 'db.ini'), encoding='gbk')
        ip = parse.get('DB', 'IP')
        port = parse.getint('DB', 'PORT')
        db_type = parse.get('DB', 'TYPE')
        self.__db_obj = build_db_obj(db_type, ip, port)
        self.__db_obj.connect()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = DbSingleton()
        return cls.__instance

    def get_db_obj(self):
        return self.__db_obj


if __name__ == "__main__":
    ins = DbSingleton.get_instance()
