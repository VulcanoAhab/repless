from .python import setEnv
from ground.basic import Ask, Say, loadConfig, persistConfig
from fabric.api import run, local, env, task, prompt


CONFIGFILE="./django-config.json"

@task
def deploy():
    """
    """
    setEnv()
