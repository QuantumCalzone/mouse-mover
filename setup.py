from setuptools import setup

APP = ['testapp.py']
DATA_FILES = ['1.gif','2.gif']
OPTIONS = {
 'iconfile':'logoapp.icns',
 'argv_emulation': True,
 'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

setup(
    name='mouse-mover',
    version='1.0.0',
    packages=[''],
    url='https://github.com/QuantumCalzone/mouse-mover',
    license='GNU General Public License v3.0',
    author='QuantumCalzone',
    author_email='QuantumCalzone@gmail.com',
    description='Allows you to slack off from Slack tracking your online status. Adapted from https://github.com/carrot69/keep-presence'
)
