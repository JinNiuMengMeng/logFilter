# -*- coding:utf-8 -*-
import os
from glob import glob
import datetime
import tarfile
import shutil
import time


class FileFilter:
    __path = []
    __current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    __filter_file_list = []
    __wait_filter_file = []

    @classmethod
    def set_path(cls, file_path):
        """  第一步: 设置日志路径  """
        for _path in file_path:
            if not os.path.exists(_path):
                return {"result": False, "message": "路径不存在"}
            elif _path[-1] != "/":
                _path += "/"
                cls.__path.append(_path)
            else:
                cls.__path.append(_path)
        return {"result": True, "message": "日志路径设置成功"}

    @classmethod
    def find_file(cls, orderNo):
        """  第二步: 根据订单号或者时间筛选相应文件  """
        if not cls.__path:
            return {"result": False, "message": "先设置日志路径"}

        current_time = int(datetime.datetime.now().strftime('%Y%m%d%H%M'))
        if len(orderNo) < 12 or int(orderNo[0:12]) > current_time:
            return {"result": False, "message": "orderNo 长度不正确 或者 日期 格式不正确"}
        start1 = time.time()
        orderNo_time = orderNo[0:12]
        for i in cls.__path:
            # 按照订单前面的日期(年月日时)匹配出文件
            if int(orderNo[10:12]) == 30 or int(orderNo[10:12]) == 00:
                cls.__filter_file_list += glob(pathname=r'/' + i[1:] + '*' + orderNo_time + '*')
            else:
                datatime_value = (datetime.datetime.strptime(
                    orderNo_time, '%Y%m%d%H%M') + datetime.timedelta(minutes=30)).strftime(
                    "%Y%m%d%H%M")
                if int(datatime_value[-2:]) < 30:
                    datatime_value = datatime_value[0:10] + '00'
                else:
                    datatime_value = datatime_value[0:10] + '30'
                cls.__filter_file_list += glob(pathname=r'/' + i[1:] + '*' + datatime_value + '*')
        end1 = time.time()
        print("end1 - start1:", end1 - start1)
        if cls.__filter_file_list:
            cls.__tarFile()
            end2 = time.time()
            print("end2 - end1:", end2 - end1)
            return {"result": True, "message": "文件筛选成功"}
        else:
            return {"result": False, "message": "没有该订单的信息"}

    @classmethod
    def __tarFile(cls):
        """ 解压文件 """
        for file in cls.__filter_file_list:
            with tarfile.open(file) as tar:
                names = tar.getnames()
                for name in names:
                    tar.extract(name, path=cls.__current_path + "/temp")
        cls.__grep_file(cls.__current_path + "/temp")

    @classmethod
    def __grep_file(cls, path):
        """ 找出解压后的文件路径 """
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                if i[-3:] == "log":
                    cls.__wait_filter_file.append(dirpath + "/" + i)

    @classmethod
    def content_filter(cls, args, awk=False):
        if cls.__path is None:
            return {"result": False, "message": "先设置日志路径"}
        elif cls.__filter_file_list is None:
            return {"result": False, "message": "先先输入订单号或者日期"}

        tmp = ""
        for _filter_file in cls.__wait_filter_file:
            cmd = "nl " + _filter_file
            for i in args:
                cmd += " | sed -n '/" + i + "/p'"

            if awk:
                cmd += """awk -F 'postData:' '$2!~/^$/{printf("%s%s: %s\\n", "➜  ", NR, $2)}'"""
            tmp += os.popen(cmd).read()
        if tmp:
            return {"result": True, "message": tmp.replace("\n", "\n\n").replace("\n\n\n\n", "\n\n")}
        else:
            return {"result": False, "message": "没有相关信息"}

    @classmethod
    def empty_cache(cls):
        """  更换订单号需要清空缓存  """
        shutil.rmtree(cls.__current_path + "/temp")
        os.mkdir(cls.__current_path + "/temp")
        cls.__filter_file_list = []
        cls.__wait_filter_file = []
        return {"result": True, "message": "success"}

    @classmethod
    def get_path(cls):
        """  查看日志路径  """
        if cls.__path:
            return {"result": True, "message": cls.__path}
        else:
            return {"result": False, "message": "没有设置路径"}

    @classmethod
    def get_filter_file_list(cls):
        if cls.__filter_file_list:
            return {"result": True, "message": cls.__filter_file_list}
        else:
            return {"result": False, "message": "没有相应的日志"}


if __name__ == "__main__":
    path_list = [
        "/home/ubuntu/Documents/logFile/172.20.70.50",
        "/home/ubuntu/Documents/logFile/172.20.70.51",
        "/home/ubuntu/Documents/logFile/172.20.70.52",
        "/home/ubuntu/Documents/logFile/172.20.70.53",
        "/home/ubuntu/Documents/logFile/172.20.70.54",
    ]
    fil = FileFilter.set_path(path_list)

    if FileFilter.find_file("201809051056")["result"]:
        result = FileFilter.content_filter("data", "20180905105647173720060105147425")
        FileFilter.get_filter_file_list()
        print(result.get("message"))
    # FileFilter.empty_cache()
