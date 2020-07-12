from db.macro import *
from db.DbRedis import DbRedis


def build_db_obj(obj_type, ip, port):
    if obj_type == DB_TYPE_REDIS:
        return DbRedis(ip, port)
    else:
        return None
