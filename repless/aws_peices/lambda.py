

@task
def create_lambda()
    """
    """
    #get zip
    zip_content=open(Configuration.lambda_zip_local,"rb").read()
    #create lambda
    lbn=LambdaByName(Configuration.lambda_name)
    lbn.set_confs(Configuration.lambda_configs)
    lbn.set_zip_content(zip_content)
    lbn.create_lambda()
    print("[+] Done creating lambda.")


### prepare lambda machine
@task
def lambda_ground():
    """ 
    """
    #connect
    #install python
    run("yum install -y python3.6")
    run("pip-3.6 install virtualenvwrapper")
    run("export HOME_ENV=~/Envs")
    run("mkdir -p ~/Envs")
    run("export PYTHON_VIRTUALENVWRAPPER=/usr/bin/python3.6")
    run("source .local/usr/bin/virtualenvwrapper.sh")
    run("mkvirtualenv {}".format(Configuration.virtual_env))
    print("[+] Done basic set up.")