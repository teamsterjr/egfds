from setuptools import setup

setup(
    name='Recommends',
    version='0.2.5',
    long_description=__doc__,
    packages=['egfds'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.0.2',
        'Werkzeug==0.14.1',
        'python-dateutil==2.7.3',
        'flask-mysqldb==0.2.0',
        'click==6.7'
        'simplejson==3.16.0'
    ]


)
