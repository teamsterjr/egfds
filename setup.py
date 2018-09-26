from setuptools import setup

setup(
    name='Recommends',
    version='0.2.5',
    long_description=__doc__,
    packages=['egfds'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'simplejson==3.16.0',
        'Flask==1.0.2',
        'Flask-Assets==0.12',
        'Werkzeug==0.14.1',
        'click==6.7',
        'flask-mysqldb==0.2.0',
        'python-dateutil==2.7.3',
        'dateparser==0.7.0'
    ]


)
