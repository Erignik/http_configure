from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton
from comm.macro import *
from log.log import logger


class RmvCmd(CmdBase):
    def __init__(self, cmd):
        super(RmvCmd, self).__init__(cmd)

    @classmethod
    def check_key_para_consist(cls, para_2_val, key_para_lst):
        if len(para_2_val) != len(key_para_lst):
            logger.error("para_2_val[%s] len is not equal to key_para_lst[%s]." % (para_2_val, key_para_lst))
            return False

        for key_para in key_para_lst:
            if key_para not in para_2_val:
                logger.error("key_para %s not in para_2_val %s." % (key_para, para_2_val))
                return False
        return True

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            logger.error("parse_cmd error, cmd is [%s]." % self.cmd)
            return False, "RmvCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            logger.error("can not get moc, moc_name is [%s]." % moc_name)
            return False, "RmvCmd, Error cmd name...."

        key_para_lst = moc_obj.get_key_para()
        if not self.check_key_para_consist(para_2_val, key_para_lst):
            return False, "cmd is Rmv, input key para should consist with module...."

        ret_flag, error_info = moc_obj.pre_rmv_cmd_check(para_2_val)
        if not ret_flag:
            logger.error("pre_rmv_cmd_check fail. ret is %s, error info is %s." % (ret_flag, error_info))
            return ret_flag, error_info

        key_dict = {para: val for para, val in para_2_val.items() if para in key_para_lst}
        para_dict = {para: val for para, val in para_2_val.items() if para not in key_para_lst}
        db_obj = DbSingleton.get_instance().get_db_obj()
        return db_obj.execute(DB_ACTION_RMV, moc_name, key_dict, para_dict)
