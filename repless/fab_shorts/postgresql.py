import os
import io
import re
import sys
import json
import getpass
from fabric.contrib import files
from ground.basic import persistConfig, loadConfig, Ask, setFabricEnv
from fabric.api import run, local, env, task, prompt, put

CONFIGFILE="./postgresql-config.json"

_HBA_DEFAULT="/var/lib/pgsql9/data/pg_hba.conf.default"
            #"/var/lib/pgsql9/data/pg_hba.conf.default"
_HBA_CONFIG="/var/lib/pgsql9/data/pg_hba.conf"
_HBA_TEMPLATE="./fab_shorts/templates/postgresql_92_pg_hba.conf"

_SERVER_DEFAULT="/var/lib/pgsql9/data/postgresql.conf.default"
_SERVER_CONFIG="/var/lib/pgsql9/data/postgresql.conf"
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
    hba_content=open(_HBA_TEMPLATE).read()
    hba_content=hba_content.format(database=env.db_name, user=env.db_user)
    hba_file=io.StringIO()
    hba_file.write(hba_content)
    hba_file.seek(0)
    if not files.exists(_HBA_DEFAULT,use_sudo=True):
        run("sudo cp {} {}".format(_HBA_CONFIG,_HBA_DEFAULT))
                                  #version-hardcoded::change
    put(hba_file, _HBA_CONFIG, use_sudo=True)
    #update server_file.conf
    severConfig_content=open(_SERVER_TEMPLATE).read() #listen to all::change
    serverConfig_file=io.StringIO()
    serverConfig_file.write(severConfig_content)
    serverConfig_file.seek(0)
    if not files.exists(_SERVER_DEFAULT, use_sudo=True):
        run("sudo cp {} {}".format(_SERVER_CONFIG,_SERVER_DEFAULT))
                                        #version-hardcoded::change

    put(serverConfig_file, _SERVER_CONFIG,use_sudo=True)
    #start server
    run("sudo service postgresql start")
    #test if user exists
    msg="Do you want to add/change postgres:user\'s password?"
    changePsPassword=Ask._green(msg,default="n",validate=r"[YyNn]")
    if changePsPassword.lower() == "y":
        while 1:
            password=getpass.getpass("Please type the passowrd: ")
            confirm_password=getpass.getpass("Please [re]type the passowrd: ")
            if password == confirm_password:break
            Say.warn("Passwords don\'t match. Let\'s try again.")
        _exec("psql -t -A -c \"ALTER USER postgres WITH"\
              " PASSWORD \'{}\';\"".format(password))
    test_db=_exec("psql -t -A -c \"SELECT COUNT(*) FROM pg_database"\
                  " WHERE datname = \'{}\';\"")
    if test_db != 1:
        Say.action("[+] Creating database: {}".format(env.db_user))
        _exec("createdb {} -O {}".format(env.db_user, env.db_password))
    test_user=_exec("psql -t -A -c \"SELECT COUNT(*) FROM pg_user"\
                    " WHERE usename = \'{}\';\"".format(env.db_user))
    if test_user != "1":
        Say.action("[+] Creating user: {}".format(env.db_user))
        _exec("psql -t -A -c"\
              "\"CREATE USER {user} SUPERUSER;"\
              "ALTER USER {user} WITH PASSWORD \'{password}\';\"".format(
                                            user=env.db_user,
                                            password=env.db_password))

@task
def backup():
    """
    """
    raise NotImplemented("[-] Only a ideia so far")
