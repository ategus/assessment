from setuptools import setup

setup(
    name='envio',
    version='0.1',
    py_modules=['envio'],
    install_requires=[
        'Click',  
        'RPi.GPIO',
    ],
    entry_points='''
        [console_scripts]
        envio=envio:cli
    ''',
)
