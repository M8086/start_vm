# start_vm
Start an Azure VM by supplying the resource group name and VM name

Arguments:
```Python
Python3 start_vm.py group_name vm_name
```

Upon successful completion, the script will return a message including the VM name and the public IP address of the VM

See the following article to setup environment variables and prep your Azure environment for running scripts:
https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd#authenticate-with-token-credentials

Use the included requirements.txt to install the necessary modules from the Azure SDK
