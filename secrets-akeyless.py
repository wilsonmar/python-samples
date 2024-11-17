#!/usr/bin/env python3

""" secrets-akeyless.py at https://github.com/wilsonmar/python-samples/blob/main/secrets-akeyless.py

This sample code is used to compare retrieval of secrets from various vaults:
Akeyless cloud, Azure Keyvault, HashiCorp Vault, etc.

STATUS: NOT WORKING built on macOS M2 14.5 (23F79) using Python 3.12.7.
# ImportError: cannot import name 'AkeylessClient' from 'akeyless' (/Users/johndoe/github-wilsonmar/python-samples/venv/lib/python3.12/site-packages/akeyless/__init__.py)
"v001 + new with import error :secrets-akeyless.py"

Before running this program:
# akeyless not found in conda-forge
# so in this program's folder:
python3 -m venv venv  # venv is in .gitignore
source venv/bin/activate
python3 -m pip install akeyless
# CLI Version: 1.115.0
chmod +x secrets-akeyless.py
./secrets-akeyless.py

Based on https://chatgpt.com/g/g-d3nZlpUee-akeyless-answer-assistant/c/673880b6-a8c8-8001-a8dc-fbe420c341b6
"""

from akeyless import AkeylessClient
   # FIXME: ImportError: cannot import name 'AkeylessClient' from 'akeyless' (/Users/johndoe/github-wilsonmar/python-samples/venv/lib/python3.12/site-packages/akeyless/__init__.py)

from akeyless.rest import ApiException


# Globals:
AKEYLESS_API_KEY = "AKEYLESS_API_KEY"  # from https://akeyless.com based on your account.
PATH_TO_SECRET = "path/to/your/secret"
#
# Choose an authentication method to authenticate your application to the Akeyless platform.
# Common options include:
   # API Key
   # Cloud Identity (AWS IAM, Azure AD, GCP)
   # Kubernetes authentication
   # Certificate-based authentication
   # Universal Identity

# Retrieve from .env file (so API_KEY tokens are not hard-coded into this application code.
# ???

# Initialize the Akeyless client:
client = AkeylessClient()

# Authenticate using an API Key:
api_key = AKEYLESS_API_KEY

def retrieve_akeyless_auth_toen(api_key):
    try:
        auth_token = client.auth(api_key=api_key)
        return auth_token
    except ApiException as e:
        print("*** EXCEPTION when calling AkeylessClient.auth:", e)


# Retrieve a Secret:
def retrieve_secret_from_akeyless(path_to_secret,akeyless_auth_token):
    try:
        secret_value = client.get_secret_value(name=path_to_secret, token=akeyless_auth_token)
        return secret_value
    except ApiException as e:
        print("*** Exception when calling AkeylessClient.get_secret_value:", e)


def fetch_dyanamic_akeyless_secret(path_to_secret,akeyless_auth_token) -> str:
    # Fetch Dynamic Secrets (time-bound credentials generated just in time):
    try:
        dynamic_secret = client.get_dynamic_secret_value(name=path_to_secret, token=akeyless_auth_token)
        return dynamic_secret
    except ApiException as e:
        print("Exception when calling AkeylessClient.get_dynamic_secret_value:", e)



if __name__ == "__main__":

    akeyless_auth_token = retrieve_akeyless_auth_toen(AKEYLESS_API_KEY)
    print("Auth Token:", akeyless_auth_token)

    secret_value = retrieve_secret_from_akeyless(PATH_TO_SECRET,akeyless_auth_token)

    dynamic_secret = fetch_dyanamic_akeyless_secret(PATH_TO_SECRET,akeyless_auth_token)