import os
from flask_script import Manager, Server
from .app import app, build, initial_data_structure, __version__

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


build = manager.command(build)
initial_data_structure = manager.command(initial_data_structure)

@manager.command
def version():
    print("Workbench %s" % __version__)

if __name__ == '__main__':
    print("Static is server from %s" % os.path.join(os.getcwd(), 'static'))
    manager.run()
