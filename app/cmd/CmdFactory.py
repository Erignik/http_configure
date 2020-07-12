from cmd.CmdTextHandle import CmdTextHandle
from cmd.AddCmd import AddCmd
from cmd.ModCmd import ModCmd
from cmd.RmvCmd import RmvCmd
from cmd.LstCmd import LstCmd
from cmd.macro import *


def get_cmd_obj(cmd):
    cmd_type = CmdTextHandle.get_cmd_type(cmd)
    if cmd_type == CMD_TYPE_ADD:
        return AddCmd(cmd)
    elif cmd_type == CMD_TYPE_MOD:
        return ModCmd(cmd)
    elif cmd_type == CMD_TYPE_RMV:
        return RmvCmd(cmd)
    elif cmd_type == CMD_TYPE_LST:
        return LstCmd(cmd)
    else:
        return None

