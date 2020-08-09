from abc import abstractmethod


class DbBase:
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__connect = None

    def get_db_ip(self):
        return self.__ip

    def get_db_port(self):
        return self.__port

    @abstractmethod
    def query(self, tbl_name):
        pass

    @abstractmethod
    def execute(self, db_op_type, tbl_name, key_dict, para_dict):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
