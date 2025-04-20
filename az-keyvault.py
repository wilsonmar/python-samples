#!/usr/bin/env python3

"""az-keyvault.py at https://github.com/wilsonmar/python-samples/blob/main/az-keyvault.py

git commit -m "v002 + uv, pyproject.toml :az-keyvault.py"

STATUS: use_dev_credential() working on macOS Sequoia 15.3.1

by Wilson Mar, LICENSE: MIT
This creates the premissions needed in Azure, then 
creates a Key Vault and sets access policies.
Adds a secret, then read it.
Based on https://www.perplexity.ai/search/how-to-create-populate-and-use-Q4EyT9iYSSaVQtyUK5N31g#0

#### Before running this program:
1. Create an .env file defining global static variables and their secret values (Account, Subscription, Tenant ID)
2. Use your email address, phone, credit card to create an account and log into Azure Portal.
3. In "Entra Admin Center" (previously Azure Active Directory) https://entra.microsoft.com/#home
4. Get a Subscription Id and Tenant Id to place in the .env file

5. Create a new Azure AD Enterprise application. Store the Application (client) ID in your .env file.
6. Get the app's Service Principal Id, which is similar to a user account but to access resources used by apps & services.
   See https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal
7. In CLI, get a long list of info about your account from:
   az ad sp list   # For its parms: https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.applications/get-mgserviceprincipal?view=graph-powershell-1.0

    "appDisplayName": "Cortana Runtime Service",
    "appId": "81473081-50b9-469a-b9d8-303109583ecb",
    ...
       "servicePrincipalNames": [
      "81473081-50b9-469a-b9d8-303109583ecb",
      "https://cortana.ai"
    ],

?. In https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview
   Click on your app in the list.
?. Under Properties, Copy the Service Principal Object ID to .env file.
?. Define RBAC to each Service Principal

# Add /.venv/ to .gitignore (for use by uv, instead of venv)
deactivate       # out from within venv
brew install uv  # new package manager
uv --help
uv init   # for pyproject.toml & .python-version files https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
uv lock
uv sync
uv venv  # to create an environment,

uv python install 3.12
# Instead of requirements.txt:
uv add pathlib
uv add python-dotenv
uv add azure-identity  msgraph-core
uv add azure-keyvault-secrets
uv add azure-mgmt-compute
uv add azure-mgmt-keyvault
uv add azure-mgmt-network
uv add azure-mgmt-resource
uv add azure-mgmt-storage
uv add azure-storage-blob
uv pip install pytz
uv pip install requests

source .venv/bin/activate
uv run az-keyvault.py

PROTIP: Each function displays its own error messages. Function callers display expected responses.

REMEMBER on CLI after running uv run az-keyvault.py: deactivate

"""
# Built-in libraries (no pip/conda install needed):
#from zoneinfo import ZoneInfo  # For Python 3.9+ https://docs.python.org/3/library/zoneinfo.html 
from datetime import datetime, timezone
import time  # for timestamp

import base64
from contextlib import redirect_stdout
from datetime import datetime
import io
import json
import logging
import os
import pathlib
from pathlib import Path
import signal
import sys
from time import perf_counter_ns
import platform
import random
from tokenize import Number


# import external library (from outside this program):
try:
    import argparse
    from azure.mgmt.resource import ResourceManagementClient
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    import azure.functions as func
    from azure.storage.blob import BlobServiceClient
    from azure.identity import ClientSecretCredential
    #from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.mgmt.resource import ResourceManagementClient
    from msgraph.core import GraphClient
    # Microsoft Authentication Library (MSAL) for Python
    # integrates with the Microsoft identity platform. It allows you to sign in users or apps with Microsoft identities (Microsoft Entra ID, External identities, Microsoft Accounts and Azure AD B2C accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or your own APIs registered with the Microsoft identity platform. It is built using industry standard OAuth2 and OpenID Connect protocols
    # See https://github.com/AzureAD/microsoft-authentication-library-for-python?tab=readme-ov-file
    from dotenv import load_dotenv
    import pytz   # for aware comparisons
    import urllib.parse
    from pathlib import Path
    import requests
except Exception as e:
    print(f"Python module import failed: {e}")
    # pyproject.toml file exists
    print(f"Please activate your virtual environment:\n")
    print("    source .venv/bin/activate")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    exit(9)

#### Parameters from call arguments:

ENV_FILE="python-samples.env"

DELETE_RG_AFTER = True
DELETE_KV_AFTER = True


#### Utility Functions:

def get_time() -> str:
    """ Generate the current local datetime. """
    now: datetime = datetime.now()
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d}'

def print_separator():
    """ Put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")


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

class bcolors:  # ANSI escape sequences:
    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    ERROR = '\033[91m'     # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO = '\033[92m'      # [92 green
    VERBOSE = '\033[95m'   # [95 purple
    TRACE = '\033[96m'     # [96 blue/green
                 # [94 blue (bad on black background)
    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'

    RESET = '\033[0m'   # switch back to default color

# PROTIP: Global variable referenced within functions:
# values obtained from .env file can be overriden in program call arguments:
show_fail = True       # Always show
show_error = True      # Always show
show_warning = True    # -wx  Don't display warning
show_todo = True       # -td  Display TODO item for developer
show_info = True       # -qq  Display app's informational status and results for end-users
show_heading = True    # -q  Don't display step headings before attempting actions
show_verbose = True    # -v  Display technical program run conditions
show_trace = True      # -vv Display responses from API calls for debugging code
show_secrets = False   # Never show


def print_separator():
    """ A function to put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")

def print_heading(text_in):
    if show_heading:
        if str(show_dates_in_logs) == "True":
            print('\n***', get_log_datetime(), bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)
        else:
            print('\n***', bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)

def print_fail(text_in):  # when program should stop
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)

def print_error(text_in):  # when a programming error is evident
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.ERROR, "ERROR:", f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    if show_warning:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.WARNING, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.WARNING, f'{text_in}', bcolors.RESET)

def print_todo(text_in):
    if show_todo:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    if show_info:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    if show_verbose:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.VERBOSE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.VERBOSE, f'{text_in}', bcolors.RESET)

def print_trace(text_in):  # displayed as each object is created in pgm:
    if show_trace:
        if str(show_dates_in_logs) == "True":
            print('***',get_log_datetime(), bcolors.TRACE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.TRACE, f'{text_in}', bcolors.RESET)


def open_env_file(env_file) -> str:
    """Return a Boolean obtained from .env file based on key provided.
    """
    # from pathlib import Path
    # See https://wilsonmar.github.io/python-samples#run_env
    global user_home_dir_path
    user_home_dir_path = str(Path.home())
       # example: /users/john_doe

    global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error(global_env_path+" (global_env_path) not found!")
    #else:
    #    print_info(global_env_path+" (global_env_path) readable.")

    path = pathlib.Path(global_env_path)
    # Based on: pip3 install python-dotenv
    from dotenv import load_dotenv
       # See https://www.python-engineer.com/posts/dotenv-python/
       # See https://pypi.org/project/python-dotenv/
    load_dotenv(global_env_path)  # using load_dotenv

    # Wait until variables for print_trace are retrieved:
    #print_trace("env_file="+env_file)
    #print_trace("user_home_dir_path="+user_home_dir_path)


def use_dev_credential(az_acct_name) -> object:
    """
    Returns a credential object for the given account name
    for local development after CLI:
    az cloud set -n AzureCloud   // return to Public Azure.
    az login
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
    Returns a credential object after app registration
    no need for CLI az login.
    """
    try:
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        return credential
    except Exception as e:
        print(f"use_app_credential() ERROR: {e}")
        return None


# def use_interactive_credential() -> object:
# """ For Interactive/OAuth Login	Web apps, user logins	Yes (browser)
# """


def get_app_principal_id(credential, app_id, tenant_id) -> object:
    """
    From the client_id (and client_secret) when you create the service principal in the Azure Portal or via CLI. 
    You can then use this directly in your Python code:
    Use the azure-identity and msgraph-core Python packages to call the Microsoft Graph API for Azure AD operations. 
    """
    #from azure.identity import DefaultAzureCredential
    #from msgraph.core import GraphClient

    client = GraphClient(credential=credential)
    if not client:
        print(f"Cannot find GraphClient to get_app_principal_id({tenant_id})!")
        return None

    response = client.get(f'/servicePrincipals?$filter=appId eq \'{app_id}\'')
    data = response.json()
    if data.get('value'):
        principal_id = data['value'][0]['id']
        print(f"get_app_principal_id(\"{principal_id}\"")
        return principal_id
    else:
        print("Service principal not found by get_app_principal_id(App ID: {app_id})!")
        return None


# TODO: set the principal with the appropriate level of permissions (typically Directory.Read.All for these operations).


def get_func_principal_id(credential, app_id, tenant_id) -> object:
    """
    
    Get userId by decoding function's X-MS-CLIENT-PRINCIPAL header. Sometimes, properties like userPrincipalName or name might not be present, 
    depending on the identity provider or user type (like guest users). 
    In such a case, check the userDetails property, which often contains the user's email or username.
    # Extract the user's email from the claims using:  user_email = client_principal.get('userDetails')
    based on https://learn.microsoft.com/en-us/answers/questions/2243286/azure-function-app-using-python-how-to-get-the-pri
    """
    app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
    return app


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the X-MS-CLIENT-PRINCIPAL header
    client_principal_header = req.headers.get('X-MS-CLIENT-PRINCIPAL')
    logging.info(f"X-MS-CLIENT-PRINCIPAL header: {client_principal_header}")
    user_name = None

    if client_principal_header:
        try:
            # Decode the Base64-encoded header
            decoded_header = base64.b64decode(client_principal_header).decode('utf-8')
            logging.info(f"Decoded X-MS-CLIENT-PRINCIPAL: {decoded_header}")
            client_principal = json.loads(decoded_header)

            # Log the entire client principal for debugging
            logging.info(f"Client Principal: {client_principal}")

            # Extract the user's name from the claims
            user_name = client_principal.get('userPrincipalName') or client_principal.get('name')
        except Exception as e:
            logging.error(f"Error decoding client principal: {e}")

    if user_name:
        return func.HttpResponse(f"Hello, {user_name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. However, no authenticated user information was found.",
            status_code=200
        )


def create_get_resource_group(credential, resource_group_name, location, subscription_id) -> object:
    """
    Create Resource Group if the resource_group_name is not already defined.
    Return json object such as {'additional_properties': {}, 'id': '/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/az-keyvault-for-python-250413', 'name': 'az-keyvault-for-python-250413', 'type': 'Microsoft.Resources/resourceGroups', 'properties': <azure.mgmt.resource.resources.v2024_11_01.models._models_py3.ResourceGroupProperties object at 0x1075ec1a0>, 'location': 'westus', 'managed_by': None, 'tags': None}
    Equivalent to CLI: az group create -n "myResourceGroup" -l "useast2"
        --tags "department=tech" "environment=test"
    See https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-resource-group?tabs=cmd
    """
    #uv add azure-mgmt-resource
    #uv add azure-identity
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient
    try:
        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Provision the resource group:
        rg_result = resource_client.resource_groups.create_or_update(
            resource_group_name, {"location": location}
        )
        # print(f"create_get_resource_group() {str(rg_result)}")
        return rg_result  # JSON
    except Exception as e:
        print(f"create_get_resource_group() ERROR: {e}")
        return None


def delete_resource_group(credential, resource_group_name, subscription_id) -> int:
    """ Equivalent of CLI: az group delete -n PythonAzureExample-rg  --no-wait
    """
    try:
        resource_client = ResourceManagementClient(credential, subscription_id)
        if not resource_client:
            print(f"Cannot find ResourceManagementClient to delete_resource_group({resource_group_name})!")
            return False
        rp_result = resource_client.resource_groups.begin_delete(resource_group_name)
            # EX: <azure.core.polling._poller.LROPoller object at 0x1055f1550>
        # if DEBUG: print(f"delete_resource_group({resource_group_name}) for {rp_result}")
        return True
    except Exception as e:
        print(f"delete_resource_group() ERROR: {e}")
        return False


def check_keyvault(credential, keyvault_name, vault_url) -> int:
    """Check if a Key Vault exists
    See https://learn.microsoft.com/en-us/python/api/overview/azure/keyvault-secrets-readme?view=azure-python
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.keyvault.secrets import SecretClient
    #from azure.core.exceptions import HttpResponseError
    #import sys
    client = SecretClient(vault_url=vault_url, credential=credential)
    if not client:
        print(f"check_keyvault(client: \"{client}\") ...")
        return False
    else:
        print(f"check_keyvault(client: \"{client}\") List ...")

    # Try listing secrets (minimal permissions required)
    secrets = client.list_properties_of_secrets()
        # <iterator object azure.core.paging.ItemPaged at 0x106911550>
    print(f"check_keyvault(secrets: \"{secrets}\") ...")

    try:
        for secret in secrets:
            # CAUTION: Avoid printing out {secret.name} values in logs:
            print(f"check_keyvault( Vault \"{keyvault_name}\" exists with secrets.")
            break
            return True
        else:
            print("check_keyvault() Vault exists but contains no secrets.")
            return False

    except Exception as e:
        print(f"check_keyvault(secrets: \"{secrets}\") ...")
        print(f"Key Vault not recognized in check_keyvault({keyvault_name}): {e}")
        print(f"check_keyvault() failed: {e}")
        return False


def create_keyvault(credential, principal_id, tenant_id, keyvault_name, location, resc_group) -> object:
    """
    # 1. Ensure the credential is for a service principal with Key Vault Contributor or Contributor RBAC role assignments.
    # Equivalent to CLI: az keyvault create --name "{$keyvault_name}" -g "${resc_group}" --enable-rbac-authorization
    # 2. Create the Key Vault using azure-mgmt-keyvault
    """
    resource_client = ResourceManagementClient(credential, subscription_id)
    if not resource_client:
        print(f"Cannot find ResourceManagementClient to create_keyvault({keyvault_name})!")
        return None
    keyvault_client = KeyVaultManagementClient(credential, subscription_id)
    if not keyvault_client:
        print(f"Cannot find KeyVaultManagementClient to create_keyvault({keyvault_name})!")
        return None

    # CAUTION: Replace <service-principal-object-id> with your SP’s object ID.
    keyvault_client.vaults.begin_create_or_update(
        resc_group,
        keyvault_name,
        {
            "location": location,
            "properties": {
                "c": tenant_id,
                "sku": {"name": "standard", "family": "A"},
                "access_policies": [{
                    "tenant_id": tenant_id,
                    "object_id": principal_id,
                    "permissions": {"secrets": ["all"], "keys": ["all"]}
                }]
            }
        }
    ).result()
    # Replace <service-principal-object-id> with your SP’s object ID.


def delete_keyvault(credential, keyvault_name, vault_url) -> bool:
    """ Equivalent to CLI: az keyvault delete --name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())  
        if secret_client:
            secret_client.delete_secret(keyvault_name)
        return True
    except Exception as e:
        print(f"delete_keyvault() ERROR: {e}")
        return False


def populate_keyvault_secret(credential, keyvault_name, secret_name, secret_value) -> object:
    """ Equivalent to az keyvault secret set --name "{$secret_name}" --value "{$secret_value}" --vault-name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())    
        if secret_client:
            rp_secret = secret_client.set_secret(secret_name, secret_value)
        return rp_secret
    except Exception as e:
       print(f"populate_keyvault_secret() ERROR: {e}")
           # <urllib3.connection.HTTPSConnection object at 0x1054a5a90>: Failed to resolve 'az-keyvault-2504190459utc.vault.azure.net' ([Errno 8] nodename nor servname provided, or not known)
       return False


def get_keyvault_secret(credential, keyvault_name, secret_name) -> object:
    """ Equivalent to CLI: az keyvault secret show --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        if secret_client:
            rp_secret = secret_client.get_secret(secret_name)
        return rp_secret
    except Exception as e:
       print(f"get_keyvault_secret() ERROR: {e}")
       return False


def delete_keyvault_secret(credential, keyvault_name, secret_name) -> object:
    """ Equivalent to CLI: az keyvault secret delete --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        rp_secret = secret_client.delete_secret(secret_name)
        return rp_secret
    except Exception as e:
       print(f"delete_keyvault_secret() ERROR: {e}")
       return False


if __name__ == "__main__":
    # print(f"In main: {get_time()}")
    
    open_env_file(ENV_FILE)

    # TODO: Fill in values from parms, .env:
    my_acct_name = os.environ["AZURE_ACCT_NAME"]
    my_credential=use_dev_credential(my_acct_name)
    if not my_credential:
        print(f"my_credential() failed: {my_credential}")
            # <azure.identity._credentials.default.DefaultAzureCredential object at 0x106be6ba0>
        exit(9)
    else:
        my_location = os.environ["AZURE_LOCATION"]
        # Equivalent of CLI: az account list-locations --output table --query "length([])" 
        # Equivalent of CLI: az account list-locations --query "[?contains(regionalDisplayName, '(US)')]" -o table
        # Equivalent of CLI: az account list-locations -o table --query "[?contains(regionalDisplayName, '(US)')]|sort_by(@, &name)[]|length(@)"
            # Remove "|length(@)"
        print(f"my_acct_name: {my_acct_name} at location: \"{my_location}\"")

    ??? my_app_id, 
    
    my_principal_id = get_app_principal_id(my_credential, my_app_id, my_tenant_id)
    if not rp_result:
        print(f"get_app_principal_id() failed with JSON: \"{rp_result}\"")
        exit(9)
    else:
        print(f"get_app_principal_id() JSON: {rp_result}")
    # Alternative: Using Azure Function App Headers (For Authenticated Users) using Easy Auth and returns the signed-in user's principal ID.


    # Equivalent of CLI to list: az account show --query id --output tsv
    my_subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
        # Equivalent of CLI: az account show --query tenantId --output tsv
        # https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/overview
    my_tenant_id = os.environ["AZURE_TENANT_ID"]  # EntraID

    #### Create Resource Group for Azure Key Vault:
    
    my_keyvault_rg_root = os.environ["AZURE_KEYVAULT_ROOT_NAME"]
    # PROTIP: Define datestamps Timezone UTC: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)  
    my_keyvault_rg = f"{my_keyvault_rg_root}-{fts.strftime("%y%m%d%H%M%Z")}"  # EX: "...-250419" UTC %H%M%Z https://strftime.org
    print(f"my_keyvault_rg: \"{my_keyvault_rg}\"")
    rp_result = create_get_resource_group(my_credential, my_keyvault_rg, my_location, my_subscription_id)
    if not rp_result:
        print(f"create_get_resource_group() failed with JSON: \"{rp_result}\"")
        exit(9)
    else:
        print(f"create_get_resource_group() JSON: {rp_result}")
        # Equivalent of CLI: az group list -o table
        # TODO: List resource groups like https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView

    #### Check & Create Azure Key Vault:

    my_keyvault_name = my_keyvault_rg
    vault_url = f"https://{my_keyvault_name}.vault.azure.net"

    my_principal_id = os.environ["AZURE_KEYVAULT_PRINCIPAL_ID"]
    rp_result = check_keyvault(my_credential, my_keyvault_name, vault_url)
    if rp_result:
        create_keyvault(my_credential, my_principal_id, my_tenant_id, my_keyvault_name, my_location, my_keyvault_rg)

    #### List Azure Key Vaults:
    # Equivalent of Portal: List Key Vaults: https://portal.azure.com/#browse/Microsoft.KeyVault%2Fvaults
    # TODO: List costs like https://portal.azure.com/#view/HubsExtension/BrowseCosts.ReactView
    # PRICING: STANDARD SKU: $0.03 per 10,000 app restart operation, plus $3 for cert renewal, PLUS $1/HSM/month.
        # See https://www.perplexity.ai/search/what-is-the-cost-of-running-a-Fr6DTbKQSWKzpdSGv6qyiw

    
    #### Add secrets to Azure Key Vault:

    my_secret_name = os.environ["MY_SECRET_NAME"]
    my_secret_value = os.environ["MY_SECRET_PLAINTEXT"]

    rp_result = populate_keyvault_secret(my_credential, my_keyvault_name, my_secret_name, my_secret_value)

    # TODO: List secrets in Key Vault

    rp_result = get_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)
    
    # delete_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)

    #### Retrieve secrets from Azure Key Vault:

    my_client_id="???"
    # Before: Register an app in Azure and create a client secret.
    my_client_secret="???"

    #### -D to delete Key Vault created above.

    if DELETE_KV_AFTER:
        rp_result = delete_keyvault(my_credential, my_keyvault_name, vault_url)

    #### -D to delete Resource Group for Key Vault created above.

    if DELETE_RG_AFTER:
        rp_result = delete_resource_group(my_credential, my_keyvault_rg, my_subscription_id)


# END