from module.MocFactory import MocSingleton
from db.DbInterface import DbSingleton
from cmd.CmdFactory import get_cmd_obj
from log.log import logger


def get_para_lst_db(moc_name):
    db_obj = DbSingleton.get_instance().get_db_obj()
    ret, query_dict_lst = db_obj.query(moc_name)
    if not ret:
        logger.error("query moc name %s fail. info is %s." % (moc_name, query_dict_lst))
        return False, []

    para_lst = []
    for query_dict in query_dict_lst:
        for key, _ in query_dict.items():
            para_lst.append(key)
    return True, list(set(para_lst))


def get_para_lst_configure(moc_name):
    moc_ins = MocSingleton.get_instance()
    moc_obj = moc_ins.get_moc(moc_name)
    if moc_obj is None:
        logger.error("moc name %s not in moc single ton." % moc_name)
        return False, []

    return True, moc_obj.get_all_para_name()


def compare_result(title, para_lst):
    info = ""
    if len(para_lst) != 0:
        info += title
        info += '&'.join(para_lst)
        info += '_'
    return info


def is_record_exist(moc_name):
    cmd = 'LST MOCEXTRAINFO:NAME=%s;' % (moc_name)
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is None:
        logger.error("can not get moc obj from cmd %s." % cmd)
        return False

    ret, info = cmd_obj.execute()
    if not ret:
        logger.error("cmd[%s] execute fail, info is %s." % (cmd, info))
        return False
    logger.info("cmd[%s] lst info is %s" % (cmd, info))
    if 'No record find' in info:
        return False
    else:
        return True


def persist_compare_result(moc_name, db_not_in_configure_para, configure_not_in_db_para):
    if is_record_exist(moc_name):
        cmd = 'RMV MOCEXTRAINFO:NAME=%s;' % moc_name
        cmd_obj = get_cmd_obj(cmd)
        if cmd_obj is not None:
            ret, info = cmd_obj.execute()
            logger.info('persist_compare_result result is %s, extra info is %s...' % (ret, info))

    info = ""
    info += compare_result("This_para_is_in_db_but_not_in_xml:", db_not_in_configure_para)
    info += compare_result("This_para_is_in_xml_but_not_in_DB:", configure_not_in_db_para)
    if len(info) == 0:
        logger.info("moc_name %s not need to update moc extra info." % moc_name)
        return

    cmd = 'ADD MOCEXTRAINFO:NAME=%s, INFO=%s;' % (moc_name.upper(), info.upper())
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is None:
        logger.error("cmd[%s] get None obj." % cmd)
        return

    ret, info = cmd_obj.execute()
    logger.info('persist_compare_result result is %s, extra info is %s...' % (ret, info))


def check_default_value():
    logger.info("start to check_default_value...")
    moc_ins = MocSingleton.get_instance()
    for moc_name in moc_ins.moc_object_list:
        ret, db_para_lst = get_para_lst_db(moc_name)
        if not ret or len(db_para_lst) == 0:
            continue
        logger.info("moc_name:%s, db_para_lst is %s." % (moc_name, db_para_lst))
        ret, configure_para_lst = get_para_lst_configure(moc_name)
        if not ret:
            continue
        logger.info("moc_name:%s, configure_para_lst is %s." % (moc_name, configure_para_lst))

        db_para_set = set(db_para_lst)
        configure_para_set = set(configure_para_lst)
        db_not_in_configure_para = db_para_set - configure_para_set
        configure_not_in_db_para = configure_para_set - db_para_set
        logger.info("moc_name:%s, configure_not_in_db_para is %s, db_not_in_configure_para is %s."
                    % (moc_name, configure_not_in_db_para, db_not_in_configure_para))
        persist_compare_result(moc_name, db_not_in_configure_para, configure_not_in_db_para)
    logger.info("check_default_value end...")

