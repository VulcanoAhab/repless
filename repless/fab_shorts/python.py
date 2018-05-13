import os
import io
import re
import json
from ground.basic import Ask, Say, loadConfig, persistConfig
from fabric.api import run, local, env, task, prompt

CONFIGFILE="./python-config.json"

@task
def setEnv():
    """
    """

    preConfig=loadConfig(CONFIGFILE)
    if preConfig:
        setNewConfig=Ask.newConfig()
    if not preConfig or setNewConfig.lower() == "y":
        configs={}
        configs["hosts"]=Ask.hosts()
        configs["key_filename"]=Ask.key_filename()
    else:
        configs=preConfig
    env.user="ec2-user"
    for k,v in configs.items():
        env[k]=v
    persistConfig(configs,CONFIGFILE )
    msg="[+] Hosts: {}\n"\
        "[+] User: {}\n"\
        "[+] Key file: {}\n".format(env.hosts,
                                env.user,
                                env.key_filename)
    Say.describe(msg)

@task
def install_36_amix8664():
    """
    """
    #test if configFile
    msg="[+] Starting install..."
    Say.action(msg)
    msg="[+] Hosts: {}\n"\
        "[+] User: {}\n"\
        "[+] Key file: {}\n".format(env.hosts,
                                env.user,
                                env.key_filename)
    Say.describe(msg)
    run("sudo yum update")
    run("sudo yum install python36")
    msg="[+] Install is done"
    Say.action(msg)

