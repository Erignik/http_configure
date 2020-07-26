from module.MocObject import build_moc
import xml.etree.ElementTree as ET
import os


class MocSingleton:
    __instance = None

    def __init__(self):
        self.__moc_object_list = {}
        self.build_moc_obj()

    def add_moc(self, moc_name, obj):
        self.__moc_object_list[moc_name.upper()] = obj

    def get_moc(self, moc_name):
        if moc_name not in self.__moc_object_list:
            return None
        return self.__moc_object_list[moc_name]

    @property
    def moc_object_list(self):
        return self.__moc_object_list

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = MocSingleton()
        return cls.__instance

    def build_moc_obj(self):
        moc_tree = ET.parse(os.path.join('conf', 'Moc.xml')).getroot()
        for moc in moc_tree:
            if 'name' not in moc.attrib or 'type' not in moc.attrib:
                continue

            moc_obj = build_moc(moc.attrib['type'], moc.attrib['name'])
            if moc_obj is None:
                continue

            for para in moc:
                is_key = para.attrib.get('key', None)
                para_name = para.attrib.get('name', None)
                para_type = para.attrib.get('type', None)
                default_value = para.attrib.get('default_value', None)
                if None not in para.attrib.values():
                    moc_obj.add_para(para_type, para_name, is_key, default_value)
            self.add_moc(moc.attrib['name'], moc_obj)
