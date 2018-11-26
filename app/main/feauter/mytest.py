from gevent import monkey

monkey.patch_all()
import gevent
from pathlib import Path
import time

dir_list = ["/home/ubuntu/Documents/logFile/172.20.70.50/",
            "/home/ubuntu/Documents/logFile/172.20.70.51/",
            "/home/ubuntu/Documents/logFile/172.20.70.52/",
            "/home/ubuntu/Documents/logFile/172.20.70.53/",
            "/home/ubuntu/Documents/logFile/172.20.70.54/",
            "/home/ubuntu/Documents/logFile/172.20.70.55/",
            "/home/ubuntu/Documents/logFile/172.20.70.56/",
            "/home/ubuntu/Documents/logFile/172.20.70.57/",
            "/home/ubuntu/Documents/logFile/172.20.70.58/",
            "/home/ubuntu/Documents/logFile/172.20.70.59/",
            ]

myFileName2 = "catalina.out.201811190010.tar.gz"
start = time.time()


def judgeFile1(dir_path):
    myFileName1 = "iparking-app-api.201811191115.tar.gz"
    if Path(dir_path + myFileName1).exists():
        pass


def judgeFile2(dir_path):
    myFileName2 = "catalina.out.201811190010.tar.gz"
    if Path(dir_path + myFileName2).exists():
        pass


for i in range(10000):
    result = []
    for i in dir_list:
        result.append(gevent.spawn(judgeFile1, i))
        # result.append(gevent.spawn(judgeFile2, i))
    gevent.joinall(result)
print('----')
print(time.time() - start)
