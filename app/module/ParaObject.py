from module.ObjectBase import ObjectBase
from module.macro import *


class ParaObject(ObjectBase):
    def __init__(self, obj_name, is_key):
        super(ParaObject, self).__init__(obj_name)
        self.__is_key = is_key

    def is_key_para(self):
        return self.__is_key == '1'


def build_para(para_type, para_name, is_key):
    if para_type == PARA_TYPE_ORIGIN:
        return ParaObject(para_name, is_key)
    else:
        return None
