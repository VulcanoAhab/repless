import os
import io
import re
import json
from ground.basic import Ask, Say, setFabricEnv
from fabric.api import run, local, env, task, prompt

CONFIGFILE="./python-config.json"


@task
def install_36_amix8664():
    """
    """
    #test if configFile
    setFabricEnv(CONFIGFILE)
    #install
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
