from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton
from comm.macro import *
from log.log import logger


class AddCmd(CmdBase):
    def __init__(self, cmd):
        super(AddCmd, self).__init__(cmd)

    @classmethod
    def check_para_consist(cls, moc_obj, para_2_val):
        para_lst = moc_obj.get_all_para_name()
        if len(para_lst) != len(para_2_val):
            logger.error("para_lst[%s] len is not equal to para_2_val[%s]." % (para_lst, para_2_val))
            return False

        for para in para_lst:
            if para not in para_2_val:
                logger.error("para[%s] not in para_2_val[%s]." % (para, para_2_val))
                return False
        return True

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            logger.error("parse_cmd error, cmd is [%s]." % self.cmd)
            return False, "AddCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            logger.error("can not get moc, moc_name is [%s]." % moc_name)
            return False, "AddCmd, Error cmd name...."

        if not self.check_para_consist(moc_obj, para_2_val):
            return False, "cmd is Add, input para should consist with module...."

        ret_flag, error_info = moc_obj.pre_add_cmd_check(para_2_val)
        if not ret_flag:
            logger.error("pre_add_cmd_check fail, error info is [%s]." % error_info)
            return ret_flag, error_info

        key_para_lst = moc_obj.get_key_para()
        key_dict = {para: val for para, val in para_2_val.items() if para in key_para_lst}
        para_dict = {para: val for para, val in para_2_val.items() if para not in key_para_lst}
        db_obj = DbSingleton.get_instance().get_db_obj()
        return db_obj.execute(DB_ACTION_ADD, moc_name, key_dict, para_dict)




