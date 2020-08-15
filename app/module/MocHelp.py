from module.MocObject import MocObject
from module.MocFactory import MocSingleton
from log.log import logger


class MocHelp(MocObject):
    def __init__(self, obj_name):
        super(MocHelp, self).__init__(obj_name)

    def pre_add_cmd_check(self, para_2_val):
        return False, "Not support this cmd..."

    def pre_mod_cmd_check(self, para_2_val):
        return False, "Not support this cmd..."

    def pre_rmv_cmd_check(self, para_2_val):
        return False, "Not support this cmd..."

    def post_lst_handle(self, query_dict_lst):
        moc_ins = MocSingleton.get_instance()
        post_handle_dict_lst = []
        moc_num = 1
        for moc_name in moc_ins.moc_object_list:
            moc_ins = MocSingleton.get_instance()
            moc_obj = moc_ins.get_moc(moc_name)
            if moc_obj is None:
                logger.error("moc name %s not in moc single ton." % moc_name)
                return []
            para_num = 1
            query_dict = {'moc%s' % moc_num: moc_name}
            para_lst_name = moc_obj.get_all_para_name()
            for para in para_lst_name:
                query_dict['para%s' % para_num] = para
                para_num += 1
            post_handle_dict_lst.append(query_dict)
            moc_num += 1
        return post_handle_dict_lst
