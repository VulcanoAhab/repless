"""
install repless
create a fabfile.py on the git base directory
echo "from repless.fab_shorts.smalls import *" > fabfile.py
"""

import os
import io
import re
import sys
import json
from ground.basic import persistConfig, loadConfig, Ask, setFabricEnv
from fabric.api import run, local, env, task, prompt

@task
def createConfiguration():
    """
    """
    #set vars
    configs={}
    #read values
    hosts=Ask.hosts()
    user_name=Ask.user_name()
    repo_path=prompt("Please add remote"\
                      "repository path\n").strip()
    config_name=prompt("Please give the configuration a name")
    #build config base
    #if os.path.exists(env.rcfile):rcFile2Dict(configs)

    key_file=prompt("If the remote connection"\
                    " requires a key file please"\
                    "add the path here:" ).strip()
    igsBase={
        "hosts":[h.strip() for h in hosts],
        "user":user_name,
        "repo_path":repo_path.strip(),
        "key_filename":key_file,
    }
    configs.update({
        config_name:json.dumps(igsBase)
    })
    #transform object
    #fileContent=dict2RCFormat(configs)
    ## save configs ##
    fd=open(env.rcfile, "w")
    fd.write(fileContent)
    fd.close()

@task
def showConfiguraton():
    """
    """
    ## open config file
    fd=open(env.rcfile, "r")
    fileDict=dict([  [l.strip("\n").strip()
                for l in line.split("=")]
              for line in fd.readlines()])
    fd.close()
    #format string
    pFormat="\n{}:\t{}\n•"
    pString=io.StringIO()
    pString.write("\n\n* CONFIG-START\n•")
    for key, value in fileDict.items():
        keyLine=pFormat.format(key,value)
        pString.write(keyLine)
    pString.write("\n* CONFIG-END\n\n")
    print(pString.getvalue())


@task
def pull():
    """
    """
    ## run servers pull
    run("cd %(repo_path)s; "\
        "git checkout %(repo_branch)s;"\
        " git pull origin %(repo_branch)s" % env)

@task
def clone():
    """
    """
    ## run servers clone
    run("cd %(repo_path)s; "\
        " git pull origin %(repo_url)s" % env)

@task
def clone_or_pull(CONFIGFILE):
    """
    """
    #test if repo exists
    #if:pull
    #not:clone
    pass

@task
def pushLocalAndPullRemote(CONFIGFILE):
    """
    """
    ## config settings
    setFabricEnv(CONFIGFILE)

    ## test  git
    status=local("git status", capture=True)
    if "Not a git repository" in status:
        raise Exception("[-] Not a git repository")

    if "Untracked files" in status:
        doAdd=prompt("You have untracked files."\
                     "Do you would like to add?[y|n]\n",
                    default="y")
        if doAdd.lower() == "y":
            files=prompt("List files to add or "\
                     "hit enter and add all", deafult="*")
            local("git add {}".format(files))

    #last test
    status=local("git status", capture=True)
    print("\n################## Git Status")
    print(status)
    print("#############################\n")
    if "nothing to commit, working tree clean" in status:
        doPush=prompt("No work here. Nothing to commit.\n"\
               "Still want to pull on remote servers?"\
               "[y|n]", default="y")
        if doPush.lower() == "n":return

    ## commit and push
    else:
        commitMessage=prompt("Please type your commit message:\n")
        local("git commit -am {}".format(commitMessage))
        local("git push origin master")

    doPush=prompt("All done. Pull on remote servers?"\
                  "[y|n]", default="y")
    if doPush.lower() == "n":return
    pull()
