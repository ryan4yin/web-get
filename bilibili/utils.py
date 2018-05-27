
import os
import pickle


def dump(obj, file_name):
    """
    将指定对象，以file_nam为名，保存到本地
    """
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
    return


def load(filename):
    """
    从当前文件夹的指定文件中load对象
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def get_file_name(file_path):
    """
    从文件路径中提取出不带拓展名的文件名
    """
    # 从文件路径获取文件名 _name
    path, file_name_with_extension = os.path.split(file_path)

    # 拿到文件名前缀
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return file_name


def has_file(path, file_name):
    """
    判断指定目录下，是否存在某文件
    """
    return file_name in os.listdir(path)


