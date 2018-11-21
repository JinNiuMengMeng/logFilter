# -*- coding:utf-8
from app.main import main
from flask import request, flash, render_template
from app.main.feauter.readDir import FileFilter


@main.route('/')
def index():
    return render_template('logFilter.html', form_reset="", form_file="")


@main.route('/set_path', methods=['GET', 'POST'])
def set_path():
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


@main.route('/filter_file', methods=['GET', 'POST'])
def filter_file():
    if request.method == 'POST':
        if request.form["key"] == "提交":
            if not request.form["orderNo"]:
                flash(message="订单号或者日期不能为空")
            else:
                result = FileFilter.find_file(request.form["orderNo"])
                flash(message=result.get("message"))
                result_file = FileFilter.get_filter_file_list()
                form = result_file.get("message")
                return render_template('logFilter.html', form_file=form)
        elif request.form["key"] == "清除当前订单号的缓存":
            result = FileFilter.empty_cache()
            form = result.get("message")
            return render_template('logFilter.html', form_reset=form)
        else:  # "查看订单相关的日志列表"
            result = FileFilter.get_filter_file_list()
            form = result.get("message")
            return render_template('logFilter.html', form_file=form)


@main.route('/filter_con', methods=['GET', 'POST'])
def filter_con():
    if request.method == 'POST':
        if request.form["key"] == "提交":
            if not request.form["keyword"]:
                flash(message="关键字不能为空")
                return render_template('logFilter.html')
            else:
                keyword_list = request.form["keyword"].replace(" ", '').split(',')
                result = FileFilter.content_filter(keyword_list)
                form = result.get("message")
                return render_template('logFilter.html', form_con=form)
        elif request.form["key"] == "过滤":
            if not request.form["keyword"]:
                flash(message="关键字不能为空")
                return render_template('logFilter.html')
            else:
                keyword_list = request.form["keyword"].replace(" ", '').split(',')
                result = FileFilter.content_filter(keyword_list, awk=True)
                form = result.get("message")
                return render_template('logFilter.html', form_con=form)
        else:  # pass
            pass
