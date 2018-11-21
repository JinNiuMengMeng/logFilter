from flask_script import Manager

from app import create_app as app_create_app

app = app_create_app()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
