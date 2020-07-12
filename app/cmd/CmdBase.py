from abc import abstractmethod
from cmd.CmdTextHandle import CmdTextHandle


class CmdBase:
    def __init__(self, cmd):
        self.cmd = CmdTextHandle.get_raw_cmd(cmd)

    @abstractmethod
    def execute(self):
        pass

