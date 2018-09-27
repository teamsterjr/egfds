from setuptools import setup

setup(
    name='EGFDS',
    version='0.2.0',
    long_description=__doc__,
    packages=['egfds'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'simplejson',
        'Flask',
        'Flask-Assets',
        'Werkzeug',
        'click',
        'flask-mysqldb',
        'python-dateutil',
        'dateparser',
        'jsmin'
    ],
    extras_require={
        'dev': [
            'pylint',
            'invoke'
        ]
    }



)
