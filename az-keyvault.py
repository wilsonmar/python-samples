#!/usr/bin/env python3

"""az-keyvault.py at https://github.com/wilsonmar/python-samples/blob/main/az-keyvault.py

git commit -m "v001 + new :az-keyvault.py"

STATUS: working on macOS Sequoia 15.3.1

by Wilson Mar, LICENSE: MIT
This creates the premissions needed in Azure, then 
creates a Key Vault and sets access policies.
Adds a secret, then read it.
Based on https://www.perplexity.ai/search/how-to-create-populate-and-use-Q4EyT9iYSSaVQtyUK5N31g#0

Before running this:
pip install azure-identity
pip install azure-storage-blob
pip install azure-keyvault-secrets
pip install azure-mgmt-keyvault
pip install azure-mgmt-resource
"""
# Built-in libraries (no pip/conda install needed):
from datetime import datetime
from contextlib import redirect_stdout
from datetime import datetime
import io
import os
import signal
import sys
from time import perf_counter_ns
import time
import platform
import random

# import external library (from outside this program):
try:
    import argparse
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient
    from azure.identity import ClientSecretCredential
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.mgmt.resource import ResourceManagementClient

    # Based on: conda install -c conda-forge load_dotenv
    from dotenv import load_dotenv
    # After: brew install miniconda
    # Based on: conda install python-dotenv   # found!
    # conda create -n py313
    # conda activate py313
    # conda install --name py313 requestsa
    from pytz import timezone
    import urllib.parse
    import requests
except Exception as e:
    print(f"Python module import failed: {e}")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print(f"Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)

## Global variables: Colors Styles:
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CVIOLET = '\033[35m'
CBEIGE = '\033[36m'
CWHITE = '\033[37m'
GRAY = '\033[90m'

HEADING = '\033[37m'   # [37 white
FAIL = '\033[91m'      # [91 red
ERROR = '\033[91m'     # [91 red
WARNING = '\033[93m'   # [93 yellow
INFO = '\033[92m'      # [92 green
VERBOSE = '\033[95m'   # [95 purple
TRACE = '\033[96m'     # [96 blue/green
                # [94 blue (bad on black background)

BOLD = '\033[1m'       # Begin bold text
UNDERLINE = '\033[4m'  # Begin underlined text
RESET = '\033[0m'   # switch back to default color

use_env_file = True    # -env "python-samples.env"
global ENV_FILE
ENV_FILE="python-samples.env"

def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'

def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")




def use_dev_credential(az_acct_name) -> object:
    """
    Returns a credential object for the given account name
    for local development after CLI az login.
    """
    try:
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url="https://{az_acct_name}.blob.core.windows.net",
            credential=credential
        )
        return credential
    except blob_service_client.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except blob_service_client.exceptions.ConnectionError as errc:
        print("Connection Error:", errc)
    except blob_service_client.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except blob_service_client.exceptions.RequestException as err:
        print("Other Error:", err)
    return None


def use_app_credential(tenant_id, client_id, client_secret) -> object:
    """
    Returns a credential object for the given account name
    after app registration
    no need for CLI az login.
    """
    try:
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        return credential
    except Error as e:
        print(f"use_app_credential ERROR: {e}")
        return None

# Interactive/OAuth Login	Web apps, user logins	Yes (browser)

if __name__ == "__main__":
    print(f"In main: {get_time()}")
    
    # TODO: Fill in values from parms, .env:
    my_acct_name="wmar@joliet.k12.mt.us"

    my_tenant_id="???"
    my_client_id="???"
    # Before: Register an app in Azure and create a client secret.
    my_client_secret="???"

    my_credential=use_dev_credential(my_acct_name)
    print(f"my_credential: {my_credential}")
        # <azure.identity._credentials.default.DefaultAzureCredential object at 0x106be6ba0>


# creates a Key Vault and sets access policies.
# Adds a secret
# Read secret


"""
# 1. Ensure your service principal has Key Vault Contributor or Contributor RBAC roles.

# 2. Create the Key Vault using azure-mgmt-keyvault

# Authenticate
credential = DefaultAzureCredential()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
keyvault_client = KeyVaultManagementClient(credential, subscription_id)

# Create resource group
resource_group_name = "myResourceGroup"
location = "eastus"
resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})

# Create Key Vault
vault_name = "your-unique-vault-name"
keyvault_client.vaults.begin_create_or_update(
    resource_group_name,
    vault_name,
    {
        "location": location,
        "properties": {
            "tenant_id": os.environ["AZURE_TENANT_ID"],
            "sku": {"name": "standard", "family": "A"},
            "access_policies": [{
                "tenant_id": os.environ["AZURE_TENANT_ID"],
                "object_id": "<service-principal-object-id>",
                "permissions": {"secrets": ["all"], "keys": ["all"]}
            }]
        }
    }
).result()
Replace <service-principal-object-id> with your SP’s object ID.

2. Populate the Key Vault
Add secrets or keys using azure-keyvault-secrets or azure-keyvault-keys.

Secrets Example:

python
from azure.keyvault.secrets import SecretClient

# Connect to Key Vault
vault_url = f"https://{vault_name}.vault.azure.net"
secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())

# Add a secret
secret = secret_client.set_secret("mySecret", "Success!")
Uses azure-keyvault-secrets library.

Keys Example:

python
from azure.keyvault.keys import KeyClient

key_client = KeyClient(vault_url=vault_url, credential=DefaultAzureCredential())
rsa_key = key_client.create_rsa_key("myRSAKey", size=2048)
Uses azure-keyvault-keys.

3. Access Data from Key Vault
Retrieve secrets/keys in your application using Azure Identity for authentication.

Retrieve a Secret:

python
retrieved_secret = secret_client.get_secret("mySecret")
print(retrieved_secret.value)  # Output: 'Success!'
Uses DefaultAzureCredential, which supports local development (Azure CLI) and managed identities in production.

Retrieve a Key:

python
retrieved_key = key_client.get_key("myRSAKey")
print(retrieved_key.key_id)
Key Dependencies
Install required libraries:

bash
pip install azure-identity azure-keyvault-secrets azure-keyvault-keys azure-mgmt-keyvault
Permissions and Authentication
Local Development: Use az login or set environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET).

Production: Use managed identities for Azure resources (e.g., VMs, App Service).

RBAC Roles: Assign Key Vault Secrets User (for secrets) or Key Vault Crypto User (for keys) to your application’s identity.

By following these steps, you securely manage sensitive data in Azure Key Vault while adhering to least-privilege access principles.

"""