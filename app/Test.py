from cmd.CmdFactory import get_cmd_obj


def add_moc():
    cmd = 'add MocAudio:AUDIOID=1,AUDIOMSG="你好啊";'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        cmd_obj.execute()

def lst_moc():
    cmd = 'lst MocAudio:;'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        print(cmd_obj.execute())


if __name__ == "__main__":
    cmd = 'Mod MocAudio:AUDIOID=1,AUDIOMSG="金小笨";'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        cmd_obj.execute()
    lst_moc()
    cmd = 'rmv MocAudio:AUDIOID=1;'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        cmd_obj.execute()
    lst_moc()