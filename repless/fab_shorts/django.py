import os
#from git import *
from fabric.contrib.project import rsync_project
from ground.basic import Ask, Say, setFabricEnv, zipDirectory
from fabric.api import run, local, env, task, prompt, prefix, put



CONFIGFILE="./django-config.json"


## tasks

@task
def init_django_cms():
    """
    """
    setFabricEnv(CONFIGFILE)
    #set vals
    project_name=env.cms_project.split("/")[-1]
    project_zip=project_name+".zip"
    #copyProject
    if not exists(env.cms_project):
        run("mkdir -p {}".format(env.cms_project))
    Say.action("[+] Syncing project")
    rsync_project(
        local_dir=env.local_cms_project,
        remote_dir=env.cms_project,
        exclude=[".git"]
    )
    Say.action("[+] Updating statics and  database")
    with cd("cd {}".format(env.cms_project)):
        #make_migrations
        run("python manage.py makemigrations")
        run("python manage.py migrate")
        #collect_static
        run("python manage.py collectstatic")




@task
def get_log():
    """
    """
    pass
