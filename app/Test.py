from cmd.CmdFactory import get_cmd_obj


def add_moc():
    cmd = 'add MocAudio:AUDIOID=1,AUDIOMSG="你好啊";'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        cmd_obj.execute()

def lst_moc():
    #cmd = 'LST MOCAUDIO:;'
    cmd = 'LST MOCHELP:;'
    cmd_obj = get_cmd_obj(cmd)
    if cmd_obj is not None:
        print(cmd_obj.execute())


if __name__ == "__main__":
    #cmd = 'ADD MOCEXTRAINFO:NAME=%s, INFO=%s;' % ('moc_name'.upper(), 'This_para_is_in_db_but_not_in_xml:audiosss&audiosss1_This_para_is_in_db_but_not_in_xml:audiosss&audiosss1'.upper())
    #cmd_obj = get_cmd_obj(cmd)
    #cmd = 'Mod MocAudio:AUDIOID=1,AUDIOMSG="金小笨";'
    #cmd_obj = get_cmd_obj(cmd)
    #if cmd_obj is not None:
    #    cmd_obj.execute()
    lst_moc()

    #cmd = 'ADD MOCDBFILEBACKUPINFO:SRC=D:/src, DST=D:/dst, TYPE=1;'
    #cmd = 'ADD MOCDBFILEBACKUPINFO:SRC=D:/src, DST=10.50.64.122, TYPE=2;'
    cmd = 'RMV MOCDBFILEBACKUPINFO:SRC=D:/src, DST=D:/dst, TYPE=1;'
    #cmd = 'ADD MOCDBFILEBACKUPINFO:SRC=/data/configure/redis_for_configure/data, DST=/home/king/docker_data/http_configure/db, TYPE=1;'
    #cmd_obj = get_cmd_obj(cmd)
    #if cmd_obj is not None:
    #    m, n = cmd_obj.execute()
    #    print("info is %s, %s" % (m, n))


    #cmd = 'rmv MocAudio:AUDIOID=1;'
    #cmd_obj = get_cmd_obj(cmd)
    #if cmd_obj is not None:
    #    cmd_obj.execute()
    #lst_moc()