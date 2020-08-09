from module.MocObject import MocObject
from db.DbInterface import DbSingleton
from log.log import logger
import os
import re


class MocDbFileBackupInfo(MocObject):
    def __init__(self, obj_name):
        super(MocDbFileBackupInfo, self).__init__(obj_name)

    @classmethod
    def is_local_backup(cls, val):
        return val == '1'

    @classmethod
    def is_ftp_backup(cls, val):
        return val == '2'

    @classmethod
    def check_para(cls, para_2_val):
        if 'DST' not in para_2_val or 'TYPE' not in para_2_val or 'SRC' not in para_2_val:
            return False, "para error, now is %s..." % para_2_val

        if not os.path.exists(para_2_val['SRC']):
            return False, 'SRC %s is not exist...' % para_2_val['SRC']

        # means backup to local path.
        if cls.is_local_backup(para_2_val['TYPE']):
            if not os.path.exists(para_2_val['DST']):
                return False, 'DST %s is not exist...' % para_2_val['DST']
        # means backup to ftp path.
        elif cls.is_ftp_backup(para_2_val['TYPE']):
            if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", para_2_val['DST']) is None:
                return False, 'IP %s is invalid...' % para_2_val['DST']
        else:
            return False, "para type %s is not local path nor ftp path..." % para_2_val['TYPE']
        return True, ""

    def pre_add_cmd_check(self, para_2_val):
        ret, info = self.check_para(para_2_val)
        if not ret:
            logger.error("check_para fail. info is %s..." % info)
            return False, info

        db_obj = DbSingleton.get_instance().get_db_obj()
        ret, query_dict_lst = db_obj.query('MOCDBFILEBACKUPINFO')
        if not ret:
            logger.error("query moc name MOCDBFILEBACKUPINFO fail.")
            return False, "query moc info error..."

        if len(query_dict_lst) >= 1:
            return False, "moc MOCDBFILEBACKUPINFO should be unique..."

        return True, ""

    def pre_mod_cmd_check(self, para_2_val):
        return self.check_para(para_2_val)

