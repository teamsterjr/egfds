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

@task(pre=[clean])
def build(c, docs=False):
    print('Building: {}'.format(version))
    for file in [
        'egfds',
        'TODO',
        'requirements.txt',
        'conf/uwsgi.ini',
        'Dockerfile'
    ]:
        if os.path.isdir(file):
            shutil.copytree(file, 'build/{}'.format(file))
        else:
            shutil.copy(file, 'build/')
    os.environ['FLASK_APP']='egfds'
    os.chdir('build')
    c.run('flask assets clean')
    c.run(
        'find . -type f -name "*.py[co]" -delete;'
        'find . -type d -name "__pycache__" -delete;'
        'rm -rf instance;'
        'rm -rf egfds/static/gen;'
    )
    c.run('Docker build -t egfds:{} .'.format( version))
    c.run('Docker tag egfds:{} egfds:latest'.format(version))
    c.run('zip ../egfds-{}.zip -r * .[^.]*'.format(version))