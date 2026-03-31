#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "keyring",
#   "python-dotenv",
# ]
# ///
# See https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file

"""secure-env.py = obtaining environment variables several ways.

A. macOS Keychain (best for local macOS tools)
B. AWS Secrets Manager (best for production / cloud)
C. Azure Keyvayult
D. GCP
E. 1Password agent
F. Akeyless?
G. HashiCorp Vault
H. Enviornment variables set by CLI calling
I. .env file last because it's unsecure to store plain text within local .env files.
J. It should be a crime to hardcode keys in source files exposed on GitHub.

   BEFORE RUNNING, on Terminal:
   # cd to a folder to receive folder (such as github-wilson):
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate
   uv add getpass keyring  subprocess --frozen

   ruff check secure-env.py
   chmod +x secure-env.py
   uv run secure-env.py -s
      # -s to save var
      # Terminal does not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""

__last_change__ = "26-03-30 v002 afplay :secure-env.py"
__status__ = "WORKS on macOS Sequoia 15.6.1"

# Stdlib modules (no import):
from getpass import getpass
import os
import subprocess
import sys
from pathlib import Path
# External modules to import from PyPI:
import argparse
import keyring
from dotenv import load_dotenv

#### Process command parameters:

# FEATURE: Add program invocation parameter -s ad PARM_SAVE_VAR to save key_name and key_value as a macOS envrionemnt variable if True. Default True.
def parse_args():
    """Parse program invocation parameters."""
    parser = argparse.ArgumentParser(description="Retrieve secrets from various secure sources.")
    parser.add_argument(
        '-s', '--save',
        dest='PARM_SAVE_VAR',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Save key_name and key_value as a macOS environment variable (default: True)'
    )
    return parser.parse_args()

def play_wav(sound_type):
   r"""Play .wav sound file from C:\\Windows\\Media\\*.wav."""
   # Using afplay program that comes with macOS.
   if not sound_type:
      print(f"sound_type {sound_type} not specified. Required.")
      return None
   match sound_type:
      case "done":
        filepath="audio/doxne.wav"
      case "error":
        filepath="audio/error.wav"
      case "warning":
        filepath="audio/warning.wav"
      case "type":
        filepath="audio/type.wav"
      case "disconnected":
        filepath="audio/disconnected.wav"
      case _:
         print("Not specified.")
         return None
   # Check if file is available:
   if not os.path.isfile(filepath):
      print(f"ERROR: Audio file {filepath} not found.")
      return None
   else:
      # Equivalent of CLI: afplay audio/done.wav
      subprocess.call(["afplay", filepath])
      return True
   

#### Utilities:

def guess_env_path() -> str | None:
   """Guess default folder same name as repo name."""
   # POLICY: Put .env files outside outside of Git repos.
   # from pathlib import Path
   repo_folder_name = Path(__file__).parent.name
   # NOT  os.path.basename(os.path.dirname(os.path.abspath(__file__)))
   #print(f"repo_folder_name=\"{repo_folder_name}\" )")
   if not repo_folder_name:
      return None
   else:
      env_filepath = "~/" + repo_folder_name + ".env"
      # Such as python-samples.env"
      print(f"env_filepath=\"{env_filepath}\" )")
      return env_filepath


#### A. macOS Keychain (best for local macOS tools):

   # POLICY: Do not print out value of secret key material!

def add_password_in_keychain(key_account, key_name, key_value):
    """Insert key value."""
   # CLI: security add-generic-password -a textere -s test -w testing
    command = f"/usr/bin/security add-generic-password -a '{key_account}' -s '{key_name}' -w '{key_value}'"
    result = subprocess.run(command, shell=True, capture_output=True)
    return result

def find_generic_password_in_keychain(key_account, key_name) -> str | None:
   """Read from macOS keychain."""
   # CLI: security find-generic-password -a textere -s test -w
   # From https://forum.rclone.org/t/read-config-password-from-macos-keychain/15324/2
   # import sys
   is_macos = sys.platform == "darwin"
   if not is_macos:
      return None
   # import subprocess  # to invoke macOS security command:
   cmd = f"/usr/bin/security find-generic-password -a '{key_account}' -s '{key_name}' -w"
      # -a {account} is optional and filters by account.
      # -s {key_name} is the service name in Keychain.
      # -w {key_value} prints only the password value.
      # {keychain}?
   result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
   if result.returncode != 0:
      return None
   return result.stdout.strip()

def get_password_from_keyring(key_name) -> str | None:
   """Get password in key_name from macOS keyring."""
   # Based on codeskipper answer at https://gist.github.com/gcollazo/9434580
   # import keyring
   key_value = keyring.get_password(key_name, key_name)
   return key_value

def get_os_variable(key_name) -> str | None:
   """Read from OS Variable."""
   # After CLI: export ANTHROPIC_API_KEY="123"
   # import os
   key_value = os.environ.get(key_name)
   if key_value:
      return key_value
   else:
      return None


def save_as_macos_env_var(key_name, key_value) -> bool:
    """Persist key_name=key_value as a macOS environment variable via launchctl."""
    result = subprocess.run(
        ["launchctl", "setenv", key_name, key_value],
        capture_output=True, text=True
    )
    return result.returncode == 0


def get_api_key(key_name, env_filepath="") -> str | None:
   """Get named key from OS variables or .env file."""
   # POLICY: Return Sentinel value "None" to force callers to explicitly acknowledge errors without try/except.
   # POLICY: Do not kill program run with sys.exit(1) within a utility function.

   # key_name="OPENWEATHER_API_KEY"  # or ANTHROPIC_API_KEY, etc.
   if not key_name:
       print(f"Error: {key_name} not provided in function call.")
       return None
   # else: use key_name provided:

   # POLICY: DO NOT echo secret API_KEY to Terminal.
   key_value = os.environ.get(key_name)
   if key_value:
       print(f"{key_name} retrieved from among OS environment variables.")
       return key_value

   # else: get from .env file:
   if not env_filepath:
      print(f"ERROR: no .env file to retrieve {key_name}.")      
   else:  # have .env:
      # from dotenv import load_dotenv
      load_dotenv(env_filepath)
      key_value = os.getenv(key_name, None)  # second arg is fallback
      if key_value:
         print(f"{key_name} retrieved from filepath {env_filepath}.")
         return key_value

   key_value = find_generic_password_in_keychain(key_account, key_name )
   if key_value:
      print(f"SUCCESS! {key_name} retrieved from keyring.")
      return key_value
   
   key_value = get_password_from_keyring(key_name)
   if key_value:
      print(f"SUCCESS! {key_name} retrieved from keyring.")
      return key_value
   
   key_value = get_password_from_keyring(key_name)
   if key_value:
      print(f"SUCCESS! {key_name} retrieved from keyring.")
      return key_value

   key_value = get_os_variable(key_name)
   if key_value:
      print(f"SUCCESS! {key_name} retrieved from env variables.")
      return key_value
   
   # POLICY: Provide manual input as a last resort to failed lookups.
   # POLICY: When asking for human input, use a loop in case of typos.
   for attempt in range(5):
      # POLICY: prompt secrets without echoing what's typed.
      # from getpass import getpass
      key_value = getpass(f"Enter {key_name} (try {attempt + 1}/5): ")
      if key_value.strip():  # Basic validation
         # TODO: Validate # chars/digits.
         break
   else:
      print("Max tries reached.")
   if key_value:
       # print(f"{key_name} input by user.")
       return key_value
   else:
       print(f"Error: {key_name} not found anywhere.")
       return None  # POLICY: Do not kill program run with sys.exit(1) within a utility function.


if __name__ == "__main__":

   args = parse_args()
   PARM_SAVE_VAR = args.PARM_SAVE_VAR

   # Set default values:
   env_filepath = guess_env_path()

   key_account = "textere"  # optional?
   key_name = "test"  # ambient-weather. = key_name
   #key_value = "my secret 123"  # the password

   # First, store a value in key if requested:
   #result = add_password_in_keychain(key_name, key_name, account, key_value)
   #print(f"result={result}")

   # my_key_name="OPENWEATHER_API_KEY"
   my_key_name="MY_ZIPCODE"
   # key_name="ANTHROPIC_API_KEY"
   # key_name="AMBIENT_APP_KEY"

   my_key_value = get_api_key(my_key_name, env_filepath)
   my_key_value_len = len(my_key_value)
   print(f"{my_key_name} is {my_key_value_len} char. Not shown.")

   if PARM_SAVE_VAR:   # True
      saved = save_as_macos_env_var(my_key_name, my_key_value)
      if saved:
         print(f"SUCCESS! {my_key_name} saved as macOS environment variable.")
      else:
         print(f"ERROR: failed to save {my_key_name} as macOS environment variable.")

   play_wav("done")

"""
# E. .env file + python-dotenv (good for local dev)
bashpip install python-dotenv
pythonfrom dotenv import load_dotenv
import os

load_dotenv()  # loads from .env file
key = os.environ.get("AMBIENT_API_KEY")
```
`.env` file:
```
# Always add .env to .gitignore.

3. AWS Secrets Manager (best for production / cloud)
# uv add install boto3
# import boto3, json

def get_secret(name):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    return json.loads(client.get_secret_value(SecretId=name)["SecretString"])

creds = get_secret("ambient-weather-keys")
api_key = creds["AMBIENT_API_KEY"]
Keys never touch disk or code — IAM roles control access.


#### 3. AWS Secrets Manager (best for production / cloud)
# uv add install boto3
# import boto3, json

# from tenacity import retry, stop_after_attempt, wait_exponential
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_secret(name):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    return json.loads(client.get_secret_value(SecretId=name)["SecretString"])

creds = get_secret("ambient-weather-keys")
api_key = creds["AMBIENT_API_KEY"]
Keys never touch disk or code — IAM roles control access.

"""