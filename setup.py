from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='Workbench',
    version='0.1.0',
    description='Timesaver for psd2html (markup)',
    long_description=readme,
    author='Bohdan Khorolets',
    author_email='b@khorolets.com',
    url='https://github.com/khorolets/workbench',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'workbench = workbench.__init__:manager.run',
        ],
    },
    install_requires=list(filter(None, [
        'flask',
        'flask-script',
        'elizabeth',
    ])),
)
