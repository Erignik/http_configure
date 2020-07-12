from cmd.CmdBase import CmdBase
from module.MocFactory import MocSingleton
from cmd.CmdTextHandle import CmdTextHandle
from db.DbInterface import DbSingleton


class LstCmd(CmdBase):
    def __init__(self, cmd):
        super(LstCmd, self).__init__(cmd)

    @classmethod
    def __get_format_record(cls, query_dict_lst):
        format_string = 'Lst record is\r\n'
        for query_dict in query_dict_lst:
            for key, val in query_dict.items():
                format_string += "%s=%s;" % (key.decode('utf-8'), val.decode('utf-8'))
            format_string += '\r\n'
        return format_string

    def execute(self):
        is_suc, moc_name, para_2_val = CmdTextHandle.parse_cmd(self.cmd)
        if not is_suc:
            return False, "LstCmd, Error cmd format...."

        moc_ins = MocSingleton.get_instance()
        moc_obj = moc_ins.get_moc(moc_name)
        if moc_obj is None:
            return False, "LstCmd, Error cmd name...."

        db_obj = DbSingleton.get_instance().get_db_obj()
        ret, query_dict_lst = db_obj.query(moc_name)
        if not ret:
            return False, "LstCmd error...."

        if len(query_dict_lst) == 0:
            return True, "No record find...."

        return True, self.__get_format_record(query_dict_lst)