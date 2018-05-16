import os
import string
from zipfile import ZipFile
from ground.basic import Ask, Say, loadConfig, persistConfig, setFabricEnv
from fabric.api import run, local, env, task, prompt


CONFIGFILE="./django-config.json"


## tasks

@task
def deploy():
    """
    """
    setFabricEnv(CONFIGFILE)
    run("git clone  {}".format(env.repository))
