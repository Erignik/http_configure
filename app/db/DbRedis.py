from db.DbBase import DbBase
from redis import StrictRedis
from comm.macro import *


def connect_wrapper(func):
    def wrapper(self, *args, **kwargs):
        self.connect()
        u = func(self, *args, **kwargs)
        self.close()
        return u
    return wrapper


class DbRedis(DbBase):
    def __init__(self, ip, port):
        super(DbRedis, self).__init__(ip, port)

    @connect_wrapper
    def query(self, tbl_name):
        try:
            query_result = []
            keys = self.__connect.keys("%s_*" % tbl_name)
            for key in keys:
                info_dict = self.__connect.hgetall(key)
                query_result.append(info_dict)
            return True, query_result
        except Exception as e:
            return False, str(e)

    @classmethod
    def _get_table_key(cls, tbl_name, key_dict):
        return tbl_name + "_" + "_".join(list(key_dict.values()))

    @connect_wrapper
    def _execute_add(self, tbl_name, key_dict, para_dict):
        try:
            tbl_key = self._get_table_key(tbl_name, key_dict)
            if self.__connect.exists(tbl_key) != 0:
                return False, "add table %s already exist...."
            para_dict.update(key_dict)
            self.__connect.hmset(tbl_key, para_dict)
            return True, "add success...."
        except Exception as e:
            return False, str(e)

    @connect_wrapper
    def _execute_mod(self, tbl_name, key_dict, para_dict):
        try:
            tbl_key = self._get_table_key(tbl_name, key_dict)
            if self.__connect.exists(tbl_key) == 0:
                return False, "mod table %s not exist...."
            for key, val in para_dict.items():
                self.__connect.hset(tbl_key, key, val)
            return True, "mod success...."
        except Exception as e:
            return False, str(e)

    @connect_wrapper
    def _execute_rmv(self, tbl_name, key_dict):
        try:
            tbl_key = self._get_table_key(tbl_name, key_dict)
            if self.__connect.exists(tbl_key) == 0:
                return False, "rmv table %s not exist...."

            self.__connect.delete(tbl_key)
            return True, "rmv success...."
        except Exception as e:
            return False, str(e)

    def execute(self, db_op_type, tbl_name, key_dict, para_dict):
        if db_op_type == DB_ACTION_ADD:
            return self._execute_add(tbl_name, key_dict, para_dict)
        elif db_op_type == DB_ACTION_MOD:
            return self._execute_mod(tbl_name, key_dict, para_dict)
        elif db_op_type == DB_ACTION_RMV:
            return self._execute_rmv(tbl_name, key_dict)
        else:
            return False, "Error op type...."

    def connect(self):
        self.__connect = StrictRedis(host=self.get_db_ip(), port=self.get_db_port(), db=0, socket_connect_timeout=0.1)

    def close(self):
        self.__connect.close()
