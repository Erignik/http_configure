from log.log import logger
from db.DbInterface import DbSingleton
from module.MocDbFileBackupInfo import MocDbFileBackupInfo
import os
import time
import shutil


def do_local_backup(query_dict):
    src = query_dict['SRC']
    dst = query_dict['DST']
    if not os.listdir(src):
        logger.error("SRC %s dir is empty..." % src)
        return

    time_now = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    dst_abs = os.path.join(dst, time_now)
    if os.path.exists(dst_abs):
        shutil.rmtree(dst_abs)

    shutil.copytree(src, dst_abs)


def do_ftp_backup(query_dict):
    pass


def backup_db_file():
    logger.info("start to backup_db_file...")
    db_obj = DbSingleton.get_instance().get_db_obj()
    ret, query_dict_lst = db_obj.query('MOCDBFILEBACKUPINFO')
    if not ret:
        logger.error("query moc name MOCDBFILEBACKUPINFO fail. info is %s." % query_dict_lst)
        return

    for query_dict in query_dict_lst:
        ret, info = MocDbFileBackupInfo.check_para(query_dict)
        if not ret:
            logger.error("check_para fail. info is %s." % info)
            continue

        if MocDbFileBackupInfo.is_local_backup(query_dict['TYPE']):
            do_local_backup(query_dict)

        if MocDbFileBackupInfo.is_ftp_backup(query_dict['TYPE']):
            do_ftp_backup(query_dict)

    logger.info("done to backup_db_file...")