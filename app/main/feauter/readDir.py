# -*- coding:utf-8 -*-
import json
import os
from glob import glob
import datetime
import tarfile
import shutil
import time
import multiprocessing
from pathlib import Path

from app.config import LogFile_Path, FileName


class FileFilter:
    __path = LogFile_Path
    __current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")

    @classmethod
    def set_path(cls, file_path):
        """  第一步: 设置日志路径  
        1. 判断路径是否存在
        2, 如果不存在返回失败, 存在的话判断末尾是否有"/", 没有的话追加
        """
        for _path in file_path:
            if not os.path.exists(_path):
                return {"result": False, "message": "路径不存在", "data": []}
            elif _path[-1] != "/":
                _path += "/"
                cls.__path.append(_path)
            else:
                cls.__path.append(_path)
        return {"result": True, "message": "日志路径设置成功", "data": []}

    @classmethod
    def find_file(cls, orderNo):
        """  第二步: 根据订单号或者时间筛选相应文件
        先判断订单号对应的文件是否存在
        不存在就查找日志路径搜索tar文件
        """
        res = cls.__judge_order(orderNo)
        if res.get("result"):
            return cls.__pool_filter_file(orderNo)
        else:
            return res

    @classmethod
    def __grep_log_file(cls, path, order):
        """ 找出解压后的文件路径 """
        key_name = order + "-log"
        result_log_dict = {}
        result_log_dict[key_name] = []

        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                if i[-3:] == "log":
                    result_log_dict[key_name].append(dirpath + "/" + i)
        return result_log_dict

    @classmethod
    def content_filter(cls, keywords, order, awk=False, fli_keyword=')]'):
        order = order[0:12]
        if cls.__path is None:
            return {"result": False, "message": "先设置日志路径", "data": ""}

        res_dict = cls.__read(order=order, file_type='-log')
        key_name = order + "-log"
        if not res_dict:
            return {"result": False, "message": "先输入订单号或者日期", "data": ""}

        tmp = ""
        print('-----------')
        for _filter_file in res_dict[key_name]:
            cmd = "nl " + _filter_file
            for i in keywords:
                cmd += " | sed -n '/" + i + "/p'"

            if awk and fli_keyword:
                cmd += """ | awk -F '""" + fli_keyword + """' '$2!~/^$/{printf("%s%s: %s\\n", "➜  ", NR, $2)}'"""
            print(cmd)
            tmp += os.popen(cmd).read()
        print('-----------')
        if tmp:
            return {"result": True, "message": "success", "data": tmp.split("\n")}
        else:
            return {"result": False, "message": "没有相关信息", "data": ""}

    @classmethod
    def empty_cache(cls):
        """  更换订单号需要清空缓存  """
        shutil.rmtree(cls.__current_path + "/temp")
        os.mkdir(cls.__current_path + "/temp")
        os.popen("sed -r -i '/-log.*/d' " + cls.__current_path + "/tempFile")
        return {"result": True, "message": "success", "data": []}

    @classmethod
    def get_path(cls):
        """  查看日志路径  """
        if cls.__path:
            return {"result": True, "message": "sucess", "data": cls.__path}
        else:
            return {"result": False, "message": "没有设置路径", "data": []}

    @classmethod
    def get_filter_file_list(cls, orderNo):
        """
        1. 先检查是否存在tar文件
        2. 如果存在tar, 再检查有没有log文件, 
        3. 如果有log文件直接返回tar文件list; 如果没有解压tar得到log后返回tar文件list
        4. 如果不存在tar, 直接返回
        """
        order = orderNo[0:12]
        res_tar_dict = cls.__read(order=order, file_type="-tar")
        key_name = order + "-tar"
        if res_tar_dict:
            if cls.__read(order=order, file_type="-log"):
                return {"result": True, "message": "success", "data": res_tar_dict[key_name]}
            else:  # 如果不存在 log
                res = cls.__get_log_list(res_tar_dict[key_name], order)  # 获取 log 文件路径
                if res:
                    cls.__write(res)
                    return {"result": True, "message": "success", "data": res_tar_dict[key_name]}
                else:
                    return {"result": False, "message": "获取 log 失败", "data": ""}
        else:
            return {"result": False, "message": "没有相关日志(注意: 先提交, 再点击查看日志列表)", "data": []}

    @classmethod
    def __judge_order(cls, order):

        if not cls.__path:
            return {"result": False, "message": "先设置日志路径", "data": []}

        current_time = int(datetime.datetime.now().strftime('%Y%m%d%H%M'))
        if len(order) < 12 or int(order[0:12]) > current_time:
            return {"result": False, "message": "order 长度不正确 或者 日期 格式不正确", "data": []}

        order = order[0:12]
        res_list = cls.__read(order=order, file_type="-log")
        if res_list:
            return {"result": False, "message": "该订单号已经被查询, 可点击后面的查询日志列表", "data": []}
        else:
            return cls.empty_cache()

    @classmethod
    def __pool_filter_file(cls, orderNo):
        order = orderNo[0:12]
        dict_key = order + '-tar'
        order_tar_dict = cls.__read(order=order, file_type='-tar')
        if not order_tar_dict:  # 如果日志中没有 order 的 tar 路径
            order_tar_dict = cls.get_tar_list(order, dict_key)  # 获取 tar 文件路径
            cls.__write(order_tar_dict)  # 将日志 tar 文件路径写入文件

        if order_tar_dict[dict_key]:
            print("tar文件个数:", len(order_tar_dict[dict_key]))
            res = cls.__get_log_list(order_tar_dict[dict_key], order)  # 获取 log 文件路径
            if res:
                cls.__write(res)  # 将日志 log 文件路径写入文件
                return {"result": True, "message": "success", "data": []}
            else:
                return {"result": False, "message": "没有找到相关 log 日志文件"}
        else:
            return {"result": False, "message": "没有找到相关 tar 日志文件"}

    @classmethod
    def get_tar_list(cls, order, dict_key):
        start = time.time()
        result_dict = {}
        result_dict[dict_key] = []
        order_number = int(order)

        order_time = order
        datetime_value = (datetime.datetime.strptime(
            order_time, '%Y%m%d%H%M') + datetime.timedelta(minutes=30)).strftime(
            "%Y%m%d%H%M")

        for path_ in cls.__path:
            if "172.20.70.50" in path_ or "172.20.70.51" in path_ or "172.20.70.52" in path_:
                if order_number > 201810231430:
                    first = 10
                    second = 40
                else:
                    first = 00
                    second = 30
                logIp = path_.split('/')[-2]
                result_dict[dict_key].extend(
                    cls.calculate_file_order(path_, logIp, order, first, second, datetime_value))
            elif "172.20.70.53" in path_ or "172.20.70.54" in path_ or "172.20.70.55" in path_:
                if order_number > 201810231430:
                    first = 15
                    second = 45
                else:
                    first = 00
                    second = 30
                logIp = path_.split('/')[-2]
                result_dict[dict_key].extend(
                    cls.calculate_file_order(path_, logIp, order, first, second, datetime_value))
            elif "172.20.70.56" in path_ or "172.20.70.57" in path_ or "172.20.70.58" in path_:
                if order_number > 201810231430:
                    first = 20
                    second = 50
                else:
                    first = 00
                    second = 30
                logIp = path_.split('/')[-2]
                result_dict[dict_key].extend(
                    cls.calculate_file_order(path_, logIp, order, first, second, datetime_value))
            else:
                first = 00
                second = 30
                logIp = path_.split('/')[-2]
                result_dict[dict_key].extend(
                    cls.calculate_file_order(path_, logIp, order, first, second, datetime_value))

        # for path_ in cls.__path:
        #     for file_name in FileName:
        #         if Path(path_ + file_name).exists():
        #             result_dict[dict_key].append(path_ + file_name)
        end = time.time()
        print('-----------')
        print("获取 tar 文件时间:", end - start)
        print('------------')
        return result_dict

    @classmethod
    def __write(cls, content):
        with open(cls.__current_path + "/tempFile", "a+", encoding="utf-8") as fd:
            fd.write(str(content) + "\n")

    @classmethod
    def __read(cls, order, file_type):
        key_name = order + file_type
        res = {}
        with open(cls.__current_path + "/tempFile", "r+", encoding="utf-8") as fd:
            line = fd.readline()
            while line:
                if key_name in line:
                    res = json.loads(line.replace("'", '"').encode("utf-8"))
                    break
                else:
                    line = fd.readline()
        return res

    @classmethod
    def __get_log_list(cls, file_list, order):
        start = time.time()
        pool = multiprocessing.Pool(processes=4)  # 解压得到 log 文件
        for file in file_list:
            pool.apply_async(cls.tarFile, (file,))
        pool.close()
        pool.join()
        end = time.time()
        res = cls.__grep_log_file(cls.__current_path + "/temp", order)
        end2 = time.time()

        print('-----------')
        print("解压时间:", end - start)
        print("搜索 log 文件时间:", end2 - end)
        print('------------')
        return res

    @classmethod
    def tarFile(cls, tar_file_path):
        """ 解压文件 """
        with tarfile.open(tar_file_path) as tar:
            names = tar.getnames()
            for name in names:
                tar.extract(name, path=cls.__current_path + "/temp")

    @classmethod
    def calculate_file_order(cls, path_, logIp, order, first, second, datetime_value):
        ip_file_list = []
        file_name_num = len(FileName[logIp])

        time_second_number = int(order[10:12])
        if time_second_number == first or time_second_number == second:
            for i in range(file_name_num):
                ip_file_list.append(path_ + FileName[logIp][i] % order)
        else:
            if int(datetime_value[-2:]) < second:
                for i in range(file_name_num):
                    ip_file_list.append(path_ + FileName[logIp][i] % (datetime_value[0:10] + str(first)))
            else:
                for i in range(file_name_num):
                    ip_file_list.append(path_ + FileName[logIp][i] % (datetime_value[0:10] + str(second)))
        return ip_file_list


"""
    @classmethod
    def get_tar_list(cls, order, dict_key):
        start = time.time()
        result = []
        result_dict = {}
        result_dict[dict_key] = []

        pool = multiprocessing.Pool(processes=30)  # 得到 tar 文件
        for i in cls.__path:
            result.append(pool.apply_async(cls.find_file_list, (i, order)))
        pool.close()
        pool.join()

        for res in result:
            result_dict[dict_key].extend(res.get())
        end = time.time()
        print('-----------')
        print("获取 tar 文件时间:", end - start)
        print('------------')
        return result_dict
        
    @classmethod
    def find_file_list(cls, i, order):
        order_time = order
        res = []
        # 按照订单前面的日期(年月日时)匹配出文件
        if int(order[10:12]) == 30 or int(order[10:12]) == 00:
            res += glob(pathname=r'/' + i[1:] + '*' + order_time + '*')
        else:
            datetime_value = (datetime.datetime.strptime(
                order_time, '%Y%m%d%H%M') + datetime.timedelta(minutes=30)).strftime(
                "%Y%m%d%H%M")
            if int(datetime_value[-2:]) < 30:
                datetime_value = datetime_value[0:10] + '00'
            else:
                datetime_value = datetime_value[0:10] + '30'
            res += glob(pathname=r'/' + i[1:] + '*' + datetime_value + '*')
        return res

"""

if __name__ == "__main__":
    FileFilter.get_tar_list("201810040822", "201810040822-tar")
