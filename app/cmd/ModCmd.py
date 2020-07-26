from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton
from comm.macro import *


class ModCmd(CmdBase):
    def __init__(self, cmd):
        super(ModCmd, self).__init__(cmd)

    @classmethod
    def check_mod_para(cls, para_2_val, key_para_lst, all_para_lst):
        for key_para in key_para_lst:
            if key_para not in para_2_val:
                return False
        for para in para_2_val.keys():
            if para not in all_para_lst:
                return False

        return True

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            return False, "ModCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            return False, "ModCmd, Error cmd name...."

        key_para_lst = moc_obj.get_key_para()
        all_para_lst = moc_obj.get_all_para_name()
        if not self.check_mod_para(para_2_val, key_para_lst, all_para_lst):
            return False, "cmd is Mod, input key para should consist with module...."

        ret_flag, error_info = moc_obj.pre_mod_cmd_check(para_2_val)
        if not ret_flag:
            return ret_flag, error_info

        key_dict = {para: val for para, val in para_2_val.items() if para in key_para_lst}
        para_dict = {para: val for para, val in para_2_val.items() if para not in key_para_lst}
        db_obj = DbSingleton.get_instance().get_db_obj()
        return db_obj.execute(DB_ACTION_MOD, moc_name, key_dict, para_dict)