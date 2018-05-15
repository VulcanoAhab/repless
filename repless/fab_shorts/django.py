from ground.basic import Ask, Say, loadConfig, persistConfig, setFabricEnv
from fabric.api import run, local, env, task, prompt


CONFIGFILE="./django-config.json"

@task
def deploy():
    """
    """
    setFabricEnv(CONFIGFILE)
    local("echo $VIRTUAL_ENV")
