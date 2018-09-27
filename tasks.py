from invoke import task
import shutil
import os

@task
def clean(c, docs=False, bytecode=False, extra=''):
    patterns = ['build']
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
    shutil.copytree('egfds', 'build/egfds')
    os.chdir('build')
    c.run('flask assets clean')
    c.run(
        'find . -type f -name "*.py[co]" -delete;'
        'find . -type d -name "__pycache__" -delete'
        'rm -rf instance'
        'rm -rf egfds/static/gen'
    )