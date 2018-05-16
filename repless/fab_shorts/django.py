import os
from git import *
from ground.basic import Ask, Say, setFabricEnv
from fabric.api import run, local, env, task, prompt


CONFIGFILE="./django-config.json"


## tasks

@task
def deploy():
    """
    """
    setFabricEnv(CONFIGFILE)
    #clone_or_pull()
