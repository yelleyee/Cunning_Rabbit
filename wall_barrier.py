import boto3
import subprocess
from cloudflare import Cloudflare
import os
from cf_dns import set_dns
import setting


# 创建EC2资源和客户端
ec2 = boto3.resource('ec2',region_name='ap-southeast-1')
ec2_client = boto3.client('ec2',region_name='ap-southeast-1')



def test_domain_network(domain):
    try:
        output = subprocess.check_output(['ping', '-n', '1', domain], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

# 步骤 1: 分配一个新的弹性IP
def allocate_elastic_ip():
    allocation = ec2_client.allocate_address(Domain='ap-southeast-1')
    return allocation['AllocationId'], allocation['PublicIp']

# 步骤 2: 将新分配的弹性IP绑定到实例A上
def associate_elastic_ip(allocation_id, instance_id):
    association = ec2_client.associate_address(
        InstanceId=instance_id,
        AllocationId=allocation_id
    )
    return association['AssociationId']

# 步骤 3: 删除其余弹性IP
def release_unused_elastic_ips():
    addresses = ec2_client.describe_addresses()['Addresses']
    for address in addresses:
        if 'InstanceId' not in address:  # 没有被实例使用的弹性IP
            print(f"Releasing Elastic IP: {address['PublicIp']}")
            ec2_client.release_address(AllocationId=address['AllocationId'])

def main(instance_id, domain):
    if test_domain_network(domain) == True:
        print("Network is OK, no necessary to reallocate IP")
        return
    
    # 步骤 1: 分配新IP
    allocation_id, new_ip = allocate_elastic_ip()
    print(f"Allocated new Elastic IP: {new_ip}")

    # 步骤 2: 绑定到实例A
    associate_id = associate_elastic_ip(allocation_id, instance_id)
    print(f"Associated Elastic IP {new_ip} with instance {instance_id}")

    # 步骤 3: 释放其余弹性IP
    release_unused_elastic_ips()
    
    set_dns(new_ip)
    
    
    
    

if __name__ == "__main__":
    main(setting.aws_instance_id, setting.record_fullname)
