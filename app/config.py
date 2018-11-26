
LogFile_Path = [
    "/LogCenter/xmetc/172.20.70.50/",
    "/LogCenter/xmetc/172.20.70.51/",
    "/LogCenter/xmetc/172.20.70.52/",
    "/LogCenter/xmetc/172.20.70.53/",
    "/LogCenter/xmetc/172.20.70.54/",
    "/LogCenter/xmetc/172.20.70.55/",
    "/LogCenter/xmetc/172.20.70.56/",
    "/LogCenter/xmetc/172.20.70.57/",
    "/LogCenter/xmetc/172.20.70.58/",
    "/LogCenter/xmetc/172.20.80.41/",
    "/LogCenter/xmetc/172.20.80.42/",
    "/LogCenter/xmetc/172.20.80.43/",
    "/LogCenter/xmetc/172.20.80.44/",
    "/LogCenter/xmetc/172.20.80.45/"
]
"""
LogFile_Path = [
    "/home/ubuntu/Documents/logFile/172.20.70.50/",
    "/home/ubuntu/Documents/logFile/172.20.70.51/",
    "/home/ubuntu/Documents/logFile/172.20.70.52/",
    "/home/ubuntu/Documents/logFile/172.20.70.53/",
    "/home/ubuntu/Documents/logFile/172.20.70.54/",
    "/home/ubuntu/Documents/logFile/172.20.70.55/",
    "/home/ubuntu/Documents/logFile/172.20.70.56/",
    "/home/ubuntu/Documents/logFile/172.20.70.57/",
    "/home/ubuntu/Documents/logFile/172.20.70.58/",
    "/home/ubuntu/Documents/logFile/172.20.70.59/"
]
"""
FileName = {
    "172.20.70.50": ["ietc-api-app.log.%s.tar.gz", "catalina.out.%s.tar.gz"],
    "172.20.70.51": ["ietc-api-app.log.%s.tar.gz", "catalina.out.%s.tar.gz"],
    "172.20.70.52": ["ietc-api-app.log.%s.tar.gz", "catalina.out.%s.tar.gz"],

    "172.20.70.53": ["iparking-app-api.%s.tar.gz", "catalina.out.%s.tar.gz"],
    "172.20.70.54": ["iparking-app-api.%s.tar.gz", "catalina.out.%s.tar.gz"],
    "172.20.70.55": ["iparking-app-api.%s.tar.gz", "catalina.out.%s.tar.gz"],

    "172.20.70.56": ["access.log.%s.tar.gz", "error.log.%s.tar.gz"],
    "172.20.70.57": ["redis.log.%s.tar.gz", "config.log.%s.tar.gz"],
    "172.20.70.58": ["catalina.out.%s.tar.gz", "ietc-api-wechat.log.%s.tar.gz", "iparking-app-api.%s.tar.gz"],

    "172.20.80.41": ["access.log.%s.tar.gz", "catalina.out.%s.tar.gz", "cloud-pay-api.log.%s.tar.gz",
                     "error.log.%s.tar.gz"],
    "172.20.80.42": ["redis.log.%s.tar.gz", ],
    "172.20.80.43": ["catalina.out.%s.tar.gz", "uniform-pay-biz.log.%s.tar.gz"],
    "172.20.80.44": ["uniform-pay-biz.log.%s.tar.gz", ],
    "172.20.80.45": ["uniform-pay-biz.log.%s.tar.gz", ],
}

if __name__ == "__main__":
    print(LogFile_Path[0].split('/')[-2])
