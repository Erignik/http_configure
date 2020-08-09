from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton
from log.log import logger


class LstCmd(CmdBase):
    def __init__(self, cmd):
        super(LstCmd, self).__init__(cmd)

    @classmethod
    def check_lst_para(cls, para_2_val, key_para_lst):
        for para in para_2_val.keys():
            if para not in key_para_lst:
                logger.error("para %s is not in key_para_lst %s." % (para, key_para_lst))
                return False
        return True

    @classmethod
    def __check_query_con(cls, query_dict, para_2_val):
        if len(para_2_val) == 0:
            return True

        for key, val in query_dict.items():
            for wanted_key, wanted_val in para_2_val.items():
                if wanted_key == key and val != wanted_val:
                    return False
        return True

    @classmethod
    def __get_format_record(cls, query_dict_lst, para_2_val):
        record_info = 'Lst record is\r\n'
        is_one_record_exist = False
        for query_dict in query_dict_lst:
            if not cls.__check_query_con(query_dict, para_2_val):
                continue

            is_one_record_exist = True
            for key, val in query_dict.items():
                record_info += "%s=%s;" % (key, val)
            record_info += '\r\n'
        return is_one_record_exist, record_info

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            logger.error("parse_cmd error, cmd is [%s]." % self.cmd)
            return False, "LstCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            logger.error("can not get moc, moc_name is [%s]." % moc_name)
            return False, "LstCmd, Error cmd name...."

        key_para_lst = moc_obj.get_key_para()
        if not self.check_lst_para(para_2_val, key_para_lst):
            return False, "LstCmd, Error para name...."

        db_obj = DbSingleton.get_instance().get_db_obj()
        ret, query_dict_lst = db_obj.query(moc_name)
        if not ret:
            logger.error("db_obj.query fail. ret is %s, query_dict_lst is %s." % (ret, query_dict_lst))
            return False, "LstCmd error...."

        ret, record_info = self.__get_format_record(query_dict_lst, para_2_val)
        if not ret:
            return True, "No record find...."
        else:
            return True, record_info
