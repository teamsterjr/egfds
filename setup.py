from setuptools import setup

version='0.2.0'

setup(
    name='EGFDS',
    long_description=__doc__,
    version=version,
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
            'invoke',
            'bumpversion'
        ]
    }
)
