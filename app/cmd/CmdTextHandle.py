import re
from cmd.macro import *
from log.log import logger


class CmdTextHandle:
    @classmethod
    def get_raw_cmd(cls, cmd):
        cmd = cmd.upper()
        if cmd.count(':') < 1:
            logger.error('cmd has not :, cmd is %s.' % cmd)
            return None
        m = cmd.find(':')
        cmd_name = cmd[:m]
        para_info = cmd[m:].strip(':')
        cmd_name = re.sub(' +', ' ', cmd_name.strip())
        para_info = para_info.replace(' ', '')
        return cmd_name + ":" + para_info

    @classmethod
    def is_cmd_valid(cls, cmd):
        raw_cmd = cls.get_raw_cmd(cmd)
        pattern1 = re.compile(r"[A-Z]{3} [A-Z]+:([A-Z]+=[/\\.:&_A-Z0-9\u4E00-\u9FA5']+,)*[A-Z]+=[/\\.:&_A-Z0-9\u4E00-\u9FA5']+;")
        # maybe lst xxx:;
        pattern2 = re.compile(r"[A-Z]{3} [A-Z]+:([A-Z]+=[/\\.:&_A-Z0-9\u4E00-\u9FA5']+,)*;")
        m1 = pattern1.match(raw_cmd)
        m2 = pattern2.match(raw_cmd)
        return m1 is not None or m2 is not None

    @classmethod
    def get_cmd_type(cls, cmd):
        raw_cmd = cls.get_raw_cmd(cmd)
        if raw_cmd is None:
            logger.error('get raw cmd fail, cmd is %s.' % cmd)
            return CMD_TYPE_BUTT

        if not cls.is_cmd_valid(raw_cmd):
            logger.error('raw cmd %s is invalid.' % raw_cmd)
            return CMD_TYPE_BUTT

        m = raw_cmd.find(':')
        cmd_name = raw_cmd[:m]
        if "ADD" in cmd_name:
            return CMD_TYPE_ADD
        elif "MOD" in cmd_name:
            return CMD_TYPE_MOD
        elif "RMV" in cmd_name:
            return CMD_TYPE_RMV
        elif "LST" in cmd_name:
            return CMD_TYPE_LST
        else:
            return CMD_TYPE_BUTT

    @classmethod
    def parse_cmd(cls, cmd):
        m = cmd.find(':')
        cmd_name = cmd[:m]
        para_info = cmd[m:].strip(':')
        if " " not in cmd_name:
            logger.error('cmd_name format error, cmd_name is %s.' % cmd_name)
            return False, '', {}
        moc_name = cmd_name.split(' ')[1]

        para_2_val = {}
        raw_para_lst = para_info.split(',')
        for raw_para in raw_para_lst:
            raw_para = raw_para.strip(';')
            if len(raw_para) == 0:
                continue

            if '=' not in raw_para:
                logger.error('para format error, raw_para is %s.' % raw_para)
                return False, moc_name, {}

            para, value = raw_para.split('=')
            para_2_val[para] = value
        return True, moc_name, para_2_val
