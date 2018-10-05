from setuptools import setup

version='0.2.10'

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
        'python-dateutil',
        'dateparser',
        'jsmin',
        'psycopg2-binary'
    ],
    extras_require={
        'dev': [
            'pylint',
            'invoke',
            'awsebcli',
            'bumpversion'
        ]
    }
)
