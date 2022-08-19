#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import shutil


def all_file_path(rootpath):
    """
    function: 传入一个目录的绝对路径，返回某个目录下所有文件的绝对路径
    """
    # log_root_path = Path(rootpath)
    if not os.path.exists(rootpath):
        print("path not exist!")
        return False
    elif os.path.isfile(rootpath):
        print("path is file , expect dir!")
        return False
    else:
        all_files = []
        for root, dirs, files in os.walk(rootpath):
            for file in files:
                complete_path = os.path.join(root, file)
                all_files.append(complete_path)
        return all_files


def all_dir_path(rootpath):
    """
    function: 返回某个目录下所有子目录的路径
    """
    if not os.path.exists(rootpath):
        print("path not exist!")
        return False
    elif os.path.isfile(rootpath):
        print("path is file , expect dir!")
        return False
    else:
        all_dirs = []
        for root, dirs, files in os.walk(rootpath):
            for dir in dirs:
                complete_path = os.path.join(root, dir)
                all_dirs.append(complete_path)
        return all_dirs


def filter_file_type(filelist, filetype):
    """
    function: 搜索一个文件列表，返回特定扩展名的文件列表
    """
    selected = [file for file in filelist if str(file).endswith(filetype)]
    return selected


def recursive_delete_path(abs_path):
    """
    function: rm -rf <path>
    """
    print("want to delete : %s" % abs_path)
    if not os.path.exists(abs_path):
        print("path not exist, no need to delete.")
        return True
    elif not os.path.isdir(abs_path):
        print("this path is not a dir. delete this file.")
        os.remove(abs_path)
        return True
    else:
        shutil.rmtree(abs_path)
        if os.path.isdir(abs_path):
            print("delete dir fail")
            return False
        else:
            print("delete dir success.")
            return True

def ls_dir(abs_path:str):
    ls = os.listdir(abs_path)
    return ls


def mkdir_p(path: str, mode: int = 755):
    """
    function: 创建目录，相当于mkdir -p
    """
    print("递归创建目录: %s" % path)
    return os.makedirs(path, mode)


def copy_file(source: str, target: str):
    """
    功能： 复制文件到指定地址，不能复制目录
    source: 必须是文件路径，
    target: 可以是目录，也可以是文件地址
    """
    if not os.path.isfile(source):
        raise IsADirectoryError("源地址居然是一个目录，我们只能复制文件。")
    if not os.path.isdir(os.path.dirname(target)):
        raise NotADirectoryError("目标目录不存在，无法拷贝")
    if os.path.isdir(target):
        target = os.path.join(target, os.path.basename(source))
    else:
        try:
            shutil.copy(source, target)
            print("复制文件 %s ----> %s ，成功。" % (source, target))
            return True
        except IOError as ie:
            raise IOError("没有目标地址的写入权限，请检查用户权限，本次拷贝失败。")
        except Exception as e:
            logging.error(e)
            raise Exception("复制文件失败")


if __name__ == "__main__":
    # f=all_file_path("D:/applet/")
    # print(f)
    # a = all_file_path("d:/applet")
    # print(all_dir_path("d:/applet"))
    # print(filter_file_type(a,".zip"))
    copy_file("D:\\BaiduNetdiskDownload\\V-CAN.ctb", "F:\\haha\\haha.txt")
