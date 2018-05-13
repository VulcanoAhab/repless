### ec2 model
@task
def create(Configuration):
    """
    """
    access_key = os.environ.get(Configuration.aws_key)
    secret_key = os.environ.get(Configuration.aws_secret)
    instance_name=Configuration.instance_name
    Ec2ByName.basic_conn(access_key, secret_key, region_name=Configuration.region_name)
    bc2=Ec2ByName(instance_name)
    if bc2.exists():
        print("[+] {} instance is on. IP:{}".format(instance_name,bc2.publicIP))
        Configuration.servers_ip.append(bc2.publicIP)
        return
    print("[+] Instance does not exist. Creating: {} ...".format(instance_name))
    if not Configuration.subnet_id:
        raise Exception("[-] Subnet is require for instance creation")
    instance=bc2.create_instance(
        ImageId=Configuration.instance_image,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SubnetId=Configuration.subnet_id,
        SecurityGroupIds=Configuration.security_groupsIDs,
        KeyName=Configuration.ssh_key_name
    )
    ec2=Ec2ByName(instance_name)
    print("[+] Waiting instance")
    count=0
    while (not ec2.exists() and not ec2.is_running()):
        time.sleep(10)
        print("[+] Waiting instance")
        count+=1
        if count == 3:
            print("[+] Fail to load instance")
            return
    Configuration.servers_ip.append(ec2.publicIP)
    #write ips to file
    fd=open(Configuration.lambda_ec2_file, "w")
    json.dump(Configuration.servers_ip, fd)
    fd.close()
    print("[+] Done creating instance EC-2. IP:{}".format(bc2.publicIP))
