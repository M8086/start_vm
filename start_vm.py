# Start a VM by resource group and name
# This script will return a success message along with the VM's public IPv4 address

import os
import sys
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

from msrestazure.azure_exceptions import CloudError

# You will want to supply the values in this function as environment variables
def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

credentials, subscription_id = get_credentials()
client = ResourceManagementClient(credentials, subscription_id)
compute = ComputeManagementClient(credentials, subscription_id)
network = NetworkManagementClient(credentials, subscription_id)

# Get and return the public IPv4 address of a VM
def get_vm_public_ip(rg_name, vm_name):
        vm = compute.virtual_machines.get(rg_name, vm_name)
        
        nic = vm.network_profile.network_interfaces[0].id
        nic_name = nic.split('/')[-1]
        nic_info = network.network_interfaces.get(rg_name, nic_name)
        
        ip = nic_info.ip_configurations[0].public_ip_address.id
        ip_name = ip.split('/')[-1]
        public_ip_info = network.public_ip_addresses.get(rg_name, ip_name)
        public_ip_address = public_ip_info.ip_address
        
        return public_ip_address

# Start a VM
def start_vm(rg_name, vm_name):
    try:
        print(f'Starting {vm_name} in resource group {rg_name}...')
        vm = compute.virtual_machines.start(rg_name, vm_name)
        vm_info = vm.result()
        vm_public_ip = get_vm_public_ip(rg_name, vm_name)
    except CloudError:
        print('Could not start the requested VM:\n{}'.format(traceback.format_exc()))
    else:
        print(f'VM {vm_name} is up @ {vm_public_ip}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: Python3 start_vm.py resource_group vm_name')
        sys.exit(-1)
    
    resource_group = sys.argv[1]
    vm_name = sys.argv[2]

    start_vm(resource_group, vm_name)