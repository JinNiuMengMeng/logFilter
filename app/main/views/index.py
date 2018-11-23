# -*- coding:utf-8
import os
from app.main import main
from flask import request, flash, render_template, jsonify
from app.main.feauter.readDir import FileFilter


@main.route('/')
def index():
    return render_template('logFilter.html', form_reset="", form_file="")


@main.route('/set_path', methods=['GET', 'POST'])
def set_path():
    print("接口 set_path 进程号 pid: ", os.getpid())
    params = {x: (y[0] if isinstance(y, list) else y) for x, y in request.args.items()}
    keys = params.get("key")
    if request.method == 'POST' or request.method == 'GET':
        if keys == "查看路径列表":
            res = FileFilter.get_path()
            result = res.get("result")
            message = res.get("message")
            data = res.get("data")
            return jsonify({"result": result, "message": message, "data": data})
        else:
            return jsonify({"result": False, "message": "日志路径后台已经配置, 无需填写! 可点击后面查看列表", "data": []})


@main.route('/filter_file', methods=['GET', 'POST'])
def filter_file():
    if request.method == 'POST' or request.method == 'GET':
        params = {x: (y[0] if isinstance(y, list) else y) for x, y in request.args.items()}
        orderNo = params.get("orderNo")
        key = params.get("key")
        if not orderNo:
            return jsonify({"result": False, "message": "订单号或者日期不能为空", "data": []})
        else:
            if key == "提交":
                res = FileFilter.find_file(orderNo)
                if res.get("result"):
                    flash(message=res.get("message"))
                    result_file = FileFilter.get_filter_file_list(orderNo)
                    return jsonify(result_file)
                else:
                    return jsonify(res)
            elif key == "清除当前订单号的缓存":
                result = FileFilter.empty_cache()
                return jsonify(result)
            elif key == "查看订单相关的日志列表":
                result = FileFilter.get_filter_file_list(orderNo)
                return jsonify(result)
            else:
                return jsonify({"result": False, "message": "无此选项", "data": []})


@main.route('/filter_con', methods=['GET', 'POST'])
def filter_con():
    if request.method == 'POST' or request.method == 'GET':
        params = {x: (y[0] if isinstance(y, list) else y) for x, y in request.args.items()}

        keyword = params.get("keyword")
        orderNo = params.get("order")

        key = params.get("key")
        if not keyword:
            return jsonify({"result": False, "message": "关键字不能为空", "data": ""})
        elif not orderNo:
            return jsonify({"result": False, "message": "先完成第二步的流程", "data": ""})
        else:
            keyword_list = keyword.replace(" ", '').split(',')
            if key == "提交":
                result = FileFilter.content_filter(keywords=keyword_list, order=orderNo)
                return jsonify(result)
            elif key == "过滤":
                result = FileFilter.content_filter(keyword_list, order=orderNo, awk=True)
                return jsonify(result)
            else:  # pass
                pass


"""
def set_path():
    print("接口 set_path 进程号 pid: ", os.getpid())
    if request.method == 'POST':
        if request.form["key"] == "提交":
            if not request.form["logpath"]:
                flash(message="路径不能为空")
                return render_template('logFilter.html')
            else:
                log_path_list = request.form["logpath"].replace(' ', '').split(',')
                result = FileFilter.set_path(log_path_list)
                if result.get("result") == "false":
                    flash(message=result.get("message"))
                    return render_template('logFilter.html')
                else:
                    flash(message=result.get("message"))
                    result = FileFilter.get_path()
                    form = result.get("message")
                    return render_template('logFilter.html', form=form)
        elif request.form["key"] == "查看路径列表":
            result = FileFilter.get_path()
            form = result.get("message")
            return render_template('logFilter.html', form=form)
        else:
            pass
"""
