# coding: utf-8
import multiprocessing
import time


def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")


if __name__ == "__main__":
    start = time.time()
    pool = multiprocessing.Pool(processes=8)
    print(time.time() - start)
    for i in range(4):
        msg = "hello %d" % i
        pool.apply_async(func, (msg,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()
    print("Mark1~ Mark1~ Mark~~11~~~~~~~~~~~~~~~~~~~~")
    start = time.time()
    pool = multiprocessing.Pool(processes=8)
    print(time.time() - start)
    for i in range(4):
        msg = "hello %d" % i
        pool.apply_async(func, (msg,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    pool.close()
    pool.join()
    print("Mark~ Mark~ Mark~~~~~22~~~~~~~~~~~~~~~~~")
    print("Sub-process(es) done.")
