from flask_script import Manager
from .app import app, build, initial_data_structure

manager = Manager(app)


build = manager.command(build)
initial_data_structure = manager.command(initial_data_structure)

if __name__ == '__main__':
    manager.run()
