from module.ObjectBase import ObjectBase
from module.macro import *
from module.ParaObject import build_para
from abc import abstractmethod


class MocObject(ObjectBase):
    def __init__(self, obj_name):
        super(MocObject, self).__init__(obj_name)
        self.__para_lst = []

    def add_para(self, para_type, para_name, is_key, default_value):
        para_obj = build_para(para_type, para_name, is_key, default_value)
        if para_obj is None:
            return
        self.__para_lst.append(para_obj)

    def get_key_para(self):
        key_para = []
        for para in self.__para_lst:
            if para.is_key_para():
                key_para.append(para.get_obj_name())
        return key_para

    def get_all_para_name(self):
        para_lst_name = []
        for para in self.__para_lst:
            para_lst_name.append(para.get_obj_name())
        return para_lst_name

    def pre_add_cmd_check(self, para_2_val):
        self.__para_lst = self.__para_lst
        return True, ""

    def pre_mod_cmd_check(self, para_2_val):
        self.__para_lst = self.__para_lst
        return True, ""

    def pre_rmv_cmd_check(self, para_2_val):
        self.__para_lst = self.__para_lst
        return True, ""

    def post_lst_handle(self, query_dict_lst):
        self.__para_lst = self.__para_lst
        return query_dict_lst


def build_origin_moc(moc_name):
    exec('from module.%s import %s' % (moc_name, moc_name))
    for sc in MocObject.__subclasses__():
        if moc_name == sc.__name__:
            return eval("%s(%s)" % (sc.__name__, sc.__name__))
    return None


def build_moc(moc_type, moc_name):
    if moc_type == MOC_TYPE_ORIGIN:
        return build_origin_moc(moc_name)
    else:
        return None
