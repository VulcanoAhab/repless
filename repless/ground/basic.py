import io
import os
import time
import json
from fabric.colors import *
from collections import namedtuple
from contextlib import contextmanager
from fabric.contrib.files import exists
from fabric.api import run, local, env, task, prompt

### lambda configs
class Configuration:
    """
    """

    servers_ip=[]
    aws_key=""
    aws_secret=""
    region_name=""
    vpc_id=""
    subnet_id=""
    security_groupsIDs=[]
    instance_image="ami-55ef662f" #amazon linux | lambda base
    instance_name=""
    bucket_name=""
    ssh_key_name=""
    user=""
    virtual_env=""
    python_dependencies_file="requirements.txt"
    lambda_ec2_file="/tmp/repless_lambda_ec2"
    lambda_zip_local="/tmp/lambda_ground.zip"

    @classmethod
    def set_values(cls, **kwargs):
        """
        """
        for key, value in kwargs.items():setattr(cls, key, value)

### ask's methods
class Ask:
    """
    """

    @classmethod
    def _green(cls, msg, **kwargs):
        """
        """
        return prompt(green("[INPUT] "+msg), **kwargs)

    @classmethod
    def hosts(cls):
        """
        """
        msg="Please add remote servers "\
            "separated by comma"
        hosts=cls._green(msg).split(",")
        return hosts

    @classmethod
    def user_name(cls):
        """
        """
        msg="Your[s] host[s] user name: "
        user_name=cls._green(msg)
        return user_name

    @classmethod
    def envName(cls):
        """
        """
        msg="The target virtual env name"
        vName=cls._green(msg)
        return vName

    @classmethod
    def key_filename(cls):
        """
        """
        msg="If the remote connection"\
             " requires a key file please"\
             "add the path here:"
        key_filename=cls._green(msg)
        return key_filename

    @classmethod
    def newConfig(cls):
        msg="Old config detected."\
            "Do you want to set a new one"
        wants=cls._green(msg,
                        default="n",
                        validate=r"[YynN]")
        return wants


### say methods
class Say:
    """
    """
    _yellow=lambda msg:print(yellow(msg))
    _red=lambda msg:print(red(msg))
    _blue=lambda msg:print(blue(msg))
    _white=lambda msg:print(white(msg))


    @classmethod
    def describe(cls, msg):
        """
        """
        cls._white(msg)

    @classmethod
    def action(cls, msg):
        """
        """
        cls._blue(msg)

    @classmethod
    def warn(cls, msg):
        """
        """
        cls._yellow(msg)


## from rcfile to dict
def loadConfig(configFile):
    """
    """
    if not os.path.exists(configFile):
        Say.warn("[-] No config file")
        return
    fd=open(configFile, "r")
    configs=json.load(fd)
    fd.close()
    return configs

## persist rc file
def persistConfig(configs, configFile):
    """
    """
    #rotate file
    if os.path.exists(configFile):
        os.rename(configFile, configFile+".old")
    #write new
    fd=open(configFile, "w")
    json.dump(configs, fd)
    fd.close()

## set fabric env
def setFabricEnv(CONFIGFILE):
    """
    """
    preConfig=loadConfig(CONFIGFILE)
    if preConfig:
        setNewConfig=Ask.newConfig()
    if not preConfig or setNewConfig.lower() == "y":
        configs={}
        configs["hosts"]=Ask.hosts()
        configs["key_filename"]=Ask.key_filename()
        configs["user"]=Ask.user_name()
        persistConfig(configs,CONFIGFILE)
    else:
        configs=preConfig
    for k,v in configs.items():
        env[k]=v
    msg="[+] Hosts: {}\n"\
        "[+] User: {}\n"\
        "[+] Key file: {}\n".format(env.hosts,
                                env.user,
                                env.key_filename)
    Say.describe(msg)


### connect to ec2
def connection(Configuration):
    """
    """
    if not Configuration.servers_ip:
        fd=open(Configuration.lambda_ec2_file, "r")
        hosts=json.load(fd)
        fd.close()
        if not hosts:raise Exception("[+] No remote server IPs")
    else:
        hosts=Configuration.servers_ip
    env.hosts=hosts
