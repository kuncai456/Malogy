import os
import yaml


class Constants:
    cur_dir = os.path.join(os.path.dirname(__file__).split("common")[0], "configure")

    @classmethod
    def load_yaml_all(cls, _path="router.yml"):
        """读取文件并返回"""
        path = os.path.join(cls.cur_dir, _path)
        if not os.path.exists(path):
            return {
                "code": "",
                "msg": "目录下不存在该文件，请添加:\n{}".format(path)
            }
        else:
            with open(path, encoding='utf-8') as f:
                return [data for data in yaml.safe_load_all(f)]

    @classmethod
    def load_yaml(cls, _path="router.yml"):
        """读取文件并返回"""
        path = os.path.join(cls.cur_dir, _path)
        if not os.path.exists(path):
            return "目录下不存在该文件，请添加:\n{}".format(path)
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)
