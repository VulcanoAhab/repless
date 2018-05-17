import os
import io
import re
import sys
import json
from fabric.contrib import files
from ground.basic import persistConfig, loadConfig, Ask, setFabricEnv
from fabric.api import run, local, env, task, prompt

CONFIGFILE="./postgresql-config.json"

_HBA_DEFAULT="/var/lib/pgsql9/data/pg_hba.conf.default"
_HBA_CONFIG="/var/lib/pgsql9/data/pg_hba.conf"
_HBA_TEMPLATE="./fab_shorts/templates/postgresql_92_pg_hba.conf"

_SERVER_DEFAULT="/var/lib/pgsql9/data/pg_server.conf.default"
_SERVER_CONFIG="/var/lib/pgsql9/data/pg_server.conf"
_SERVER_TEMPLATE="./fab_shorts/templates/postgresql_92_pg_server.conf"

# utils
def _exec(toExec):
    """
    """
    return sudo("sudo -u postgres {}".format(toExec))


# tasks

@task
def install_amix8664():
    """
    """
    #update yum
    setFabricEnv(CONFIGFILE)
    run("sudo yum update")
    #install
    run("sudo yum -y install postgresql "\
        "postgresql-server "\
        "postgresql-devel "\
        "postgresql-contrib")
    #for testing
    #run("sudo service postgresql initdb")
    #update hba_file.conf
    hba_file=open(_HBA_TEMPLATE).read()
    hba_file=hba_file.format(database=env.db_name, user=env.db_user)
    if files.exits(_HBA_DEFAULT):
        run("sudo mv {} {}".format(_HBA_CONFIG,_HBA_DEFAULT))
                                  #version-hardcoded::change
    run("sudo echo {} > {}".format(hba_file,_HBA_CONFIG))
    #update server_file.conf
    severConfig_file=open(_SERVER_TEMPLATE).read() #listen to all::change
    if files.exits(_SERVER_DEFAULT):
        run("sudo mv {} {}".format(_SERVER_CONFIG,_SERVER_DEFAULT))
                                        #version-hardcoded::change
    run("sudo echo {} > {}".format(severConfig_file, _SERVER_CONFIG))
    #start server
    run("sudo service postgresql start")


@task
def backup():
    """
    """
    raise NotImplemented("[-] Only a ideia so far")
