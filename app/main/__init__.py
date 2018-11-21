from flask import Flask, Blueprint

main = Blueprint("main", __name__, template_folder='templates', static_folder='static')
from .views import index