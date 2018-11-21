# -*- coding:utf-8 -*-
from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class Path(FlaskForm):
    # path = StringField('日志路径')
    path = StringField('日志路径', validators=[DataRequired(),
                                               Length(min=1, max=-1, message="长度不符合规范")])


class OrderNo(FlaskForm):
    # orderNo = StringField('订单号', validators=[DataRequired()])
    orderNo = StringField('订单号')


class KeyWord(FlaskForm):
    # keywords = StringField('关键字', validators=[DataRequired()])
    keywords = StringField('关键字')
