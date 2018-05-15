import os
import io
import re
import json
from contextlib import contextmanager
from ground.basic import Ask, Say, loadConfig, persistConfig, setFabricEnv
from fabric.api import run, local, env, task, put, prefix

CONFIGFILE="./python-config.json"

@contextmanager
def loadEnv(envName):
    """
    """
    with prefix("source ~/.bash_profile"):
        with prefix("workon {}".format(envName)):
            yield

@task
def env2_python36_amix8664():
    """
    """
    #load config
    setFabricEnv(CONFIGFILE)
    #local env
    with loadEnv(env.virtual_namis):
        msg="[+] Env {} is on. Saving "\
            "requirements.txt.".format(env.virtual_namis)
        Say.action(msg)
        local("pip freeze > /tmp/requirements.txt")
    #build remote env
    msg="[+] Uploading requirements.txt"
    Say.action(msg)
    put("/tmp/requirements.txt", "/tmp/requirements.txt")
    run("pip-3.6 install virtualenvwrapper --user")
    run("echo 'export WORKON_HOME=~/Envs' >> ~/.bash_profile &&"\
        " mkdir -p $WORKON_HOME &&"\
        "echo 'export VIRTUALENVWRAPPER_PYTHON="\
        "/usr/bin/python36' >> ~/.bash_profile &&"\
        " echo 'source .local/bin/virtualenvwrapper.sh' >> ~/.bash_profile")
    #install requirements
    with prefix("source ~/.bash_profile"):
        run("mkvirtualenv {}".format(env.virtual_namis))
        with prefix("workon {}".format(env.virtual_namis)):
            run("pip install -r /tmp/requirements.txt")
            Say.describe("[+] Done duplicating the virtual "\
                         "env to remote server")
