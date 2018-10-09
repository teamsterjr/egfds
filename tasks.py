from invoke import task
import shutil
import os
from conf.version import __version__ as version

@task
def clean(c, dist=False, docs=False, bytecode=False, extra=''):
    patterns = ['build']
    if dist:
        patterns.append('*.zip')
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))

@task
def createdblink(c):
    c.run('''
        host=postgres-egfds.cia9ex7vgyok.eu-west-2.rds.amazonaws.com
        LIVE_IP=`host $host | awk '/has address/ { print  $4 }'`
        [ ! -z $LIVE_IP ] && echo "LIVE_IP=$LIVE_IP" > script/.env
    ''')

@task
def reqs(c):
    c.run('pip freeze | grep -v "^-e" | xargs pip uninstall -y')
    c.run('pip install -e .')
    c.run('pip uninstall -y EGFDS')
    c.run('pip freeze > requirements.txt')
    c.run('pip install -e .[dev]')
    c.run('rm -r EGFDS.egg-info')

@task(pre=[clean])
def build(c, docs=False):
    print('Building: {}'.format(version))
    for file in [
        'egfds',
        'TODO',
        'requirements.txt',
        'conf/uwsgi.ini',
        'Dockerfile',
        '.ebextensions',
        'script/db/pgpass'
    ]:
        if os.path.isdir(file):
            shutil.copytree(file, 'build/{}'.format(file))
        else:
            shutil.copy(file, 'build/')
    os.environ['FLASK_APP']='egfds'
    os.chdir('build')
    c.run('mkdir -p script/db/; mv pgpass script/db')
    c.run('flask assets clean')
    c.run(
        'find . -type f -name "*.py[co]" -delete;'
        'find . -type d -name "__pycache__" -delete;'
        'rm -rf instance;'
        'rm -rf egfds/static/gen;'
    )
    c.run('Docker build -t egfds:{} .'.format( version))
    c.run('Docker tag egfds:{} egfds:latest'.format(version))
    os.chdir('../')

@task(pre=[build])
def release(c):
    c.run('zip ../egfds-{}.zip -r * .[^.]* -x \*script/\*'.format(version))

@task(pre=[build])
def localprod(c):
    os.chdir('script')
    c.run('docker-compose -f docker-compose.yml -f docker-compose.local-prod.yml up egfds')
    os.chdir('../')

@task
def startdb(c):
    os.chdir('script')
    c.run('docker-compose up -d pgs')
    os.chdir('../')

@task
def stopdb(c):
    os.chdir('script')
    c.run('docker-compose rm -s -f pgs')
    os.chdir('../')
