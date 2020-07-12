from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton
from comm.macro import *


class AddCmd(CmdBase):
    def __init__(self, cmd):
        super(AddCmd, self).__init__(cmd)

    @classmethod
    def check_para_consist(cls, moc_obj, para_2_val):
        para_lst = moc_obj.get_all_para()
        if len(para_lst) != len(para_2_val):
            return False

        for para in para_lst:
            if para not in para_2_val:
                return False
        return True

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            return False, "AddCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            return False, "AddCmd, Error cmd name...."

        if not self.check_para_consist(moc_obj, para_2_val):
            return False, "cmd is Add, input para should consist with module...."

        ret_flag, error_info = moc_obj.pre_add_cmd_check(para_2_val)
        if not ret_flag:
            return ret_flag, error_info

        key_para_lst = moc_obj.get_key_para()
        key_dict = {para: val for para, val in para_2_val.items() if para in key_para_lst}
        para_dict = {para: val for para, val in para_2_val.items() if para not in key_para_lst}
        db_obj = DbSingleton.get_instance().get_db_obj()
        return db_obj.execute(DB_ACTION_ADD, moc_name, key_dict, para_dict)




